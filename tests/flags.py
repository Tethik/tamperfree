import pytest

inconsiderate = pytest.mark.skipif(
    not pytest.config.getoption("--inconsiderate"),
    reason="need --inconsiderate option to run"
)

slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)
