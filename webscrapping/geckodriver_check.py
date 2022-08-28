from references.paths import geckodriver_reference


class MissingGeckodriverException(Exception):
    pass


def __existing_geckodriver() -> bool:
    ref = geckodriver_reference()
    return ref.exists()


def check_geckodriver() -> None:
    existing = __existing_geckodriver()
    if not existing:
        raise MissingGeckodriverException(f"Error: could not find geckodriver.exe file at [{geckodriver_reference()}]")