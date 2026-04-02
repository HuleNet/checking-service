from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from asyncio import to_thread
from time import monotonic

from docker import from_env
from docker.errors import APIError
from requests.exceptions import ReadTimeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError

from checking_service.domain.enums.language import Language
from checking_service.application.ports.runner import Runner, RunResult
from checking_service.infrastructure.config.settings import get_settings
from checking_service.infrastructure.infrastructure_errors import (
    RunnerExecutionError,
    RunnerMemoryOutError,
    RunnerTimeoutError,
)


@dataclass(frozen=True)
class LanguageSpec:
    files: dict[str, str]
    docker_image: str
    command: list[str]
    workdir: str = "/app"


class DockerRunner(Runner):
    def __init__(self) -> None:
        self._client = from_env()
        self._time_limit_sec = get_settings().execution_time_limit_sec
        self._memory_limit_mb = get_settings().execution_memory_limit_mb

    async def run(self, code: str, language: Language, input_data: str) -> RunResult:
        return await to_thread(self._run_sync, code, language, input_data)

    def _run_sync(self, code: str, language: Language, input_data: str) -> RunResult:
        if language == Language.python:
            spec = self._get_python_spec(code=code)
        else:
            raise RunnerExecutionError(
                "Unsupported language", context={"language": language.value}
            )

        container = None

        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            for filename, content in spec.files.items():
                (tmp_path / filename).write_text(content)

            stdout = ""
            stderr = ""
            exit_code = -1
            execution_time_sec = 0.0

            try:
                container = self._client.containers.run(
                    image=spec.docker_image,
                    command=spec.command,
                    stdin_open=True,
                    tty=False,
                    detach=True,
                    working_dir=spec.workdir,
                    volumes={str(tmp_path): {"bind": spec.workdir, "mode": "rw"}},
                    network_disabled=True,
                    mem_limit=f"{self._memory_limit_mb}m",
                    security_opt=["no-new-privileges"],
                    read_only=True,
                    pids_limit=64,
                    cpu_period=100000,
                    cpu_quota=50000,
                )
                sock = container.attach_socket(
                    params={
                        "stdin": 1,
                        "stream": 1,
                    }
                )
                input_bytes = (input_data + "\n").encode()

                if hasattr(sock, "sendall"):
                    sock.sendall(input_bytes)
                    sock.close()
                elif hasattr(sock, "send"):
                    sock.send(input_bytes)
                    sock.close()
                else:
                    raw = getattr(sock, "_sock", None)

                    if raw:
                        raw.sendall(input_bytes)
                        raw.close()
                    else:
                        raise RunnerExecutionError(
                            "Unsupported socket type",
                            context={"type": str(type(sock))},
                        )

                start = monotonic()
                result = container.wait(timeout=self._time_limit_sec)
                end = monotonic()

                try:
                    exit_code = result["StatusCode"]

                except KeyError:
                    raise RunnerExecutionError(
                        "Missing exit code",
                        context={"result": result},
                    )

                if result.get("OOMKilled") or exit_code == 137:
                    raise RunnerMemoryOutError(
                        "Docker execution memory out",
                        context={"memory_out": self._memory_limit_mb},
                    )

                stdout_bytes = container.logs(stdout=True, stderr=False)
                stderr_bytes = container.logs(stdout=False, stderr=True)
                stdout = (stdout_bytes.decode() if stdout_bytes else "")[:5000]
                stderr = (stderr_bytes.decode() if stderr_bytes else "")[:5000]
                execution_time_sec = end - start

            except APIError as exc:
                raise RunnerExecutionError(
                    "Docker execution failed",
                    context={"details": str(exc)},
                )
            except (ReadTimeout, ReadTimeoutError, ConnectionError):
                if container:
                    try:
                        container.kill()
                    except Exception:
                        pass

                raise RunnerTimeoutError(
                    "Docker execution timeout",
                    context={"timeout": self._time_limit_sec},
                )
            finally:
                if container:
                    try:
                        container.remove(force=True)
                    except Exception:
                        pass

        return RunResult(
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            execution_time_sec=execution_time_sec,
        )

    def _get_python_spec(self, code: str) -> LanguageSpec:
        return LanguageSpec(
            files={"solution.py": code},
            docker_image="python:3.12-alpine",
            command=["python", "solution.py"],
        )
