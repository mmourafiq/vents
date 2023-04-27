from vents import settings


def pytest_configure():
    settings.create_app()
