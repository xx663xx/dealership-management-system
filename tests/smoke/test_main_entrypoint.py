import importlib
import unittest
from unittest.mock import patch


class MainEntrypointSmokeTests(unittest.TestCase):
    def test_importing_main_does_not_start_gui(self):
        module = importlib.import_module("main")

        self.assertTrue(callable(module.main))

    def test_main_delegates_to_application_window(self):
        module = importlib.import_module("main")

        with patch.object(module, "run_app") as run_app:
            module.main()

        run_app.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
