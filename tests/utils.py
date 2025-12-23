"""Test utils."""

from dataclasses import dataclass


@dataclass
class ParametrizedTests:
    """Util class to help on the generation on test data."""

    params: tuple
    tests: dict[str, tuple]

    def build(self) -> dict:
        """Build the the test data."""
        test_names = []
        test_data = []
        for tn, td in self.tests.items():
            test_names.append(tn)
            test_data.append(td)

        return {
            "argnames": self.params,
            "argvalues": test_data,
            "ids": test_names,
        }
