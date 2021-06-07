
import unittest

class Test_BudgetPY(unittest.TestCase):
    dict = {
        '0_format': [
            'date',
            'location data',
            'float amount',
            'identifier',
            'category'],
        'debt': [],
        'deposits': [],
        'fast_food': [
            ['01/28/21', 'CHICK-FIL-A', -14.99, 'CHICK-FIL-A', 'fast_food'],
            ['03/15/21','BOJANGLES 5555 ELIZABETH CITY NY',-12.99,'BOJANGLES','fast_food']],
        'food': [
            ['01/22/21', 'FOOD LION', -200, 'FOOD LION', 'food'],
            ['02/21/21', 'HARRIS_TEETER', -250, 'HARRIS', 'food'],
            ['03/15/21', 'FARM_FRESH', -150, 'FRESH', 'food']],
        'fun': [],
        'gas': [
            ['03/22/21','SHELL OIL 2423423423423 LUCY, PA',-28,'SHELL','gas']],
        'home': [
            ['01/24/21', 'HOME_DEPOT', -57, 'HOME', 'home'],
            ['01/12/21', 'LOWES', -100, 'LOWES', 'home'],
            ['02/14/21', 'TRUE_VALUE', -60, 'TRUE', 'home']],
        'income': [],
        'interest': [],
        'medical': [],
        'pets': [],
        'restaurants': [],
        'savings': [],
        'transportation': [],
        'utilities': [
            ['03/18/21','DENVER SANITATION 489-4698-06456 CO', -80,'SANITATION','gas']]
            }
        
    # def test_dictionary():
    #     input_values = [2,3]
    #     output = []

    #     def mock_input(s):
    #         output.append(s)
    #         return input_values.pop(0)
    #     app.input = mock_input
    #     app.print = lambda s : output.append(s)
    
    # app.main()
    # assert output == []
