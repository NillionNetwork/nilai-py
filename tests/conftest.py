import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-e2e",
        action="store_true",
        default=False,
        help="Run end-to-end tests (requires a live server and API_KEY env var)",
    )


def pytest_collection_modifyitems(config, items):
    """Skip e2e tests unless the --run-e2e flag is provided."""
    if not config.getoption("--run-e2e"):
        skip_e2e = pytest.mark.skip(
            reason="E2E tests require a live server. Run with: pytest --run-e2e"
        )
        for item in items:
            if "e2e" in str(item.fspath):
                item.add_marker(skip_e2e)
