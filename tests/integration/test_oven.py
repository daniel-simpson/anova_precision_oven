import unittest

from tests.integration import OVEN_IP, OVEN_PASSWORD

from anova_precision_oven import (
    AnovaPrecisionOven,
)

class TestOven(unittest.TestCase):
    def setUp(self) -> None:
            self.oven = AnovaPrecisionOven()
            self.oven.login(OVEN_PASSWORD)

    def tearDown(self) -> None:
        self.oven.close()
    
    def test_login(self) -> None:
         # Intentionally left blank