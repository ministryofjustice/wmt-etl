''' Configuration for pytest'''
import pytest

def pytest_addoption(parser):
    '''Add specific option for integration tests'''
    parser.addoption("--integration", action="store_true", help="Run integration tests")

def pytest_runtest_setup(item):
    '''Ignore tests which have been marked integration, unless the required arg is specified'''
    if 'integration' in item.keywords:
        if not item.config.getoption("--integration"):
            pytest.skip("Requires --integration option to run")
