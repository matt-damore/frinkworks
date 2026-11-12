import frinkworks


def test_package_import():
    """Verify that the FrinkWorks package is importable."""

    assert frinkworks.__file__ is not None  # True = test passes
