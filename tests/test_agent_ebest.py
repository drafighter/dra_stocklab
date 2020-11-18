import inspect
import unittest
from stocklab.agent.ebest import EBest


class TestEBest(unittest.TestCase):

    def setUp(self):
        self.ebest = EBest("DEMO")
        self.ebest.login()

    def test_get_code_list(self):
        print(inspect.stack()[0][3])
        result = self.ebest.get_code_list("KOSPI")
        assert result is not None
        print(len(result))

    def tearDown(self):
        self.ebest.logout()
