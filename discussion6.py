import unittest
import os


def load_csv(f):
    '''
    Params: 
        f, name or path or CSV file: string

    Returns:
        nested dict structure from csv
        outer keys are (str) years, values are dicts
        inner keys are (str) months, values are (str) integers
    
    Note: Don't strip or otherwise modify strings. Don't change datatypes from strings. 
    '''
    d = {}
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)

    with open(full_path, 'r') as daily_visitors:
        lines = daily_visitors.read().splitlines() # reads and splits each line
    
    header = lines[0].split(',') # gets the header and splits it by comma
    years = header[1:] # makes a list of the years
    
    for y in years:
        d[y] = {} # makes a new dict for each year
    
    for line in lines[1:]:
        parts = line.split(',')
        month_str = parts[0]
        value_str = parts[1:]

        for y, val_str in zip(years, value_str): # Should zip the year with the current value of the month its on
            d[y][month_str] = int(val_str) 

    return d

def get_annual_max(d):
    '''
    Params:
        d, dict created by load_csv above

    Returns:
        list of tuples, each with 3 items: year (str), month (str), and max (int) 
        max is the maximum value for a month in that year, month is the corresponding month

    Note: Don't strip or otherwise modify strings. Do not change datatypes except where necessary.
        You'll have to change vals to int to compare them. 
    '''
    max_list = [] # final return
    
    for year, month_dict in d.items(): # keys are year and values are each dictionary that contains year by month
        best_value = None
        best_month = None

        for month, val in month_dict.items(): # keys are month and values are the visitors by month
            if best_value is None or val > best_value:
                best_month = month
                best_value = val
    
        max_list.append((year, best_month, best_value)) # this makes the tuple for each year, had to do it at the end because tuples are immutable
    print(max_list)
    return max_list


def get_month_avg(d):
    '''
    Params: 
        d, dict created by load_csv above

    Returns:
        dict where keys are years and vals are floats rounded to nearest whole num or int
        vals are the average vals for months in the year

    Note: Don't strip or otherwise modify strings. Do not change datatypes except where necessary. 
        You'll have to make the vals int or float here and round the avg to pass tests.
    '''
    avg = {}
    adder = 0
    for year, month_dict in d.items():
        for key, value in month_dict.items():
            adder += value
        avg[year] = round(adder / 12)

        adder = 0
    print(avg)
    return avg

class dis7_test(unittest.TestCase):
    '''
    you should not change these test cases!
    '''
    def setUp(self):
        self.flight_dict = load_csv('daily_visitors.csv')
        self.max_tup_list = get_annual_max(self.flight_dict)
        self.month_avg_dict = get_month_avg(self.flight_dict)

    def test_load_csv(self):
        self.assertIsInstance(self.flight_dict['2021'], dict)
        self.assertEqual(self.flight_dict['2020']['JUN'], '435')

    def test_get_annual_max(self):
        self.assertEqual(self.max_tup_list[2], ('2022', 'AUG', 628))

    def test_month_avg_list(self):
        self.assertAlmostEqual(self.month_avg_dict['2020'], 398, 0)

def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()
