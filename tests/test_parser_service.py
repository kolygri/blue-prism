# Python standard library imports
import unittest
from unittest.mock import patch

# Project specific imports
import app.services.parser_service as ps

# Third-party imports
import pandas as pd


class TestParserService(unittest.TestCase):

    @patch("app.services.parser_service.sessionmaker")
    @patch("app.services.parser_service.pd.read_csv")
    @patch("app.services.parser_service.get_order_count")
    def test_upper(self,
                   order_count_mock,
                   read_csv_mock,
                   session_mock):
        order_count_mock.side_effect = [0, 1]
        data = [["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"],
                ["2021-10-02 01:11:18.891630",
                 "50f43343-e930-4f2e-91be-606bc018c872",
                 "c53fa27e-c8c2-4b77-a89a-6ed11fa87317",
                 "Cincinatti",
                 "203",
                 "19f4a11d-63ca-4127-975a-15933aaa33ff",
                 "Omaha",
                 "203",
                 "2233"]]

        read_csv_mock.return_value = pd.DataFrame(data, columns=["order_date",
                                                                 "order_id",
                                                                 "customer_id",
                                                                 "customer_location",
                                                                 "requested_amt",
                                                                 "supplier_id",
                                                                 "supplier_location",
                                                                 "supplied_amt",
                                                                 "cost"])
        ps.persist_orders(None, "filename")
        order_count_mock.return_value = 1
        self.assertEqual(ps.get_is_successful_persist(), True, "The end status of the persist operation is not correct.")


if __name__ == "__main__":
    unittest.main()
