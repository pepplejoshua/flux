import pytest

def pytest_addoption(parser):
    parser.addoption('--exp', default='5', help='Pass your expected result')
    parser.addoption('--ln', default='5 * 1', help='Pass an expression to evaluate')

@pytest.fixture
def exp(request):
    return request.config.getoption('--exp')

@pytest.fixture
def ln(request):
    return request.config.getoption('--ln')