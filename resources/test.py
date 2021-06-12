import unittest
from unittest import TestCase
from unittest import mock
import budget


class DictCreateTests(TestCase):
    @mock.patch("budget.py.input", create=True)
    def testdictCreateSimple(self, mocked_input):
        mocked_input.side_effect = [
            "csv",  # testing dirty csv
            "format",  # testing the if formatted, right now it needs the word format to fix a dirty csv
            "data/training.csv",  # filename
            "y",  # rename columns
            "date2, date, transaction, account, amount, balance",  # col names
            "y",  # DOES ORIGINAL COLUMN DATA NEED TO BE INSERTED INTO DF? Y/N
            "y",  # REMOVE COLUMNS? Y/N
            "date2, account, balance",  # COLUMNS TO REMOVE::
            "onl",  # CHOOSE CATEGORY:::
            "home",  # CHOOSE CATEGORY:::
            "util",  # CHOOSE CATEGORY:::
            "gas",  # CHOOSE CATEGORY:::
            "take_away",  # CHOOSE CATEGORY:::
            "y",  # PRINT OUT DICT Y/N
            "n",  # ADD TO DATABASE? Y/N
            "n",  # SAVE NEW DATAFRAME TO CSV? Y/N
        ]
        # result = dictCreate(1)
        self.assertEqual(result, {"Albert Einstein": [42.81]})

        data_frame_example = """
                    date                             transaction float amount identifier   category
            0 2021-05-19               7-ELEVEN 41522 SUFFOLK VA        -6.24   7-eleven        gas
            1 2021-05-23      THE HOME DEPOT #4622 CHESAPEAKE VA       -47.47       home       home
            2 2021-05-24  AMZN Mktp US*2R1SG06J1 Amzn.com/billWA       -20.13       amzn     online
            3 2021-05-20  DOORDASH*RAJPUT INDIAN WWW.DOORDASH.CA       -34.31   doordash  take_away
            4 2021-05-21                SPECTRUM 855-707-7328 MO       -54.99   spectrum    utility"""

        printed_dict = {
            "0_format": [
                "date",
                "transaction",
                "float amount",
                "identifier",
                "category",
            ],
            "debt": [],
            "deposit": [],
            "entertainment": [],
            "gas": [
                [
                    Timestamp("2021-05-19 00:00:00"),
                    "7-ELEVEN 41522 SUFFOLK VA",
                    -6.24,
                    "7-eleven",
                    "gas",
                ]
            ],
            "groceries": [],
            "home": [
                [
                    Timestamp("2021-05-23 00:00:00"),
                    "THE HOME DEPOT #4622 CHESAPEAKE VA",
                    -47.47,
                    "home",
                    "home",
                ]
            ],
            "income": [],
            "interest": [],
            "medical": [],
            "online": [
                [
                    Timestamp("2021-05-24 00:00:00"),
                    "AMZN Mktp US*2R1SG06J1 Amzn.com/billWA",
                    -20.13,
                    "amzn",
                    "online",
                ]
            ],
            "other": [],
            "pet": [],
            "restaurant": [],
            "savings": [],
            "take_away": [
                [
                    Timestamp("2021-05-20 00:00:00"),
                    "DOORDASH*RAJPUT INDIAN WWW.DOORDASH.CA",
                    -34.31,
                    "doordash",
                    "take_away",
                ]
            ],
            "transportation": [],
            "utility": [
                [
                    Timestamp("2021-05-21 00:00:00"),
                    "SPECTRUM 855-707-7328 MO",
                    -54.99,
                    "spectrum",
                    "utility",
                ]
            ],
            "work": [],
        }


# class Test_BudgetPY(unittest.TestCase):
#     dict = {
#         '0_format': [
#             'date',
#             'location data',
#             'float amount',
#             'identifier',
#             'category'],
#         'debt': [],
#         'deposits': [],
#         'fast_food': [
#             ['01/28/21', 'CHICK-FIL-A', -14.99, 'CHICK-FIL-A', 'fast_food'],
#             ['03/15/21','BOJANGLES 5555 ELIZABETH CITY NY',-12.99,'BOJANGLES','fast_food']],
#         'food': [
#             ['01/22/21', 'FOOD LION', -200, 'FOOD LION', 'food'],
#             ['02/21/21', 'HARRIS_TEETER', -250, 'HARRIS', 'food'],
#             ['03/15/21', 'FARM_FRESH', -150, 'FRESH', 'food']],
#         'fun': [],
#         'gas': [
#             ['03/22/21','SHELL OIL 2423423423423 LUCY, PA',-28,'SHELL','gas']],
#         'home': [
#             ['01/24/21', 'HOME_DEPOT', -57, 'HOME', 'home'],
#             ['01/12/21', 'LOWES', -100, 'LOWES', 'home'],
#             ['02/14/21', 'TRUE_VALUE', -60, 'TRUE', 'home']],
#         'income': [],
#         'interest': [],
#         'medical': [],
#         'pets': [],
#         'restaurants': [],
#         'savings': [],
#         'transportation': [],
#         'utilities': [
#             ['03/18/21','DENVER SANITATION 489-4698-06456 CO', -80,'SANITATION','gas']]
#             }
