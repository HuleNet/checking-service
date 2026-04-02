from pytest import raises, mark

from checking_service.domain.enums.language import Language
from checking_service.infrastructure.runners.docker_runner import DockerRunner
from checking_service.infrastructure.infrastructure_errors import RunnerTimeoutError, RunnerMemoryOutError


@mark.asyncio
async def test_success_runner_python():
    runner = DockerRunner()
    code = """
a = int(input())
b = int(input())
print(a + b)
"""
    result = await runner.run(
        code=code,
        language=Language.python,
        input_data="2\n3",
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == "5"
    assert result.stderr == ""
    assert result.execution_time_sec > 0.0


@mark.asyncio
async def test_timeout_runner():
    runner = DockerRunner()
    code = """
a = input()
while True:
    print(a)    
"""

    with raises(RunnerTimeoutError) as exc:
        await runner.run(
            code=code,
            language=Language.python,
            input_data="Hello",
        )
        
        
@mark.asyncio
async def test_memory_out_runner():
    runner = DockerRunner()
    code = """
data = []
while True:
    data.append("ERROR" * 10000000)
"""

    with raises(RunnerMemoryOutError) as exc:
        await runner.run(
            code=code,
            language=Language.python,
            input_data="",
        )