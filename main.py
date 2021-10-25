# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import requests


def check_float(input):
    try:
        val = float(input)
    except ValueError:
        print('Invalid input, please enter the correct number')
        return False
    return True


def check_integer(input):
    try:
        val = int(input)
    except ValueError:
        print("Invalid input, please enter an integer")
        return False
    return True


def forward_calculator_manual(type):
    r = 0.06
    if type == 'commodity':
        check = False

        commodity_type = input('Please enter the commodity type: ')

        check = False
        while check is False:
            price = input('Please enter the ' + commodity_type.upper() + ' price: ')
            check = check_float(price)

        check = False
        while check is False:
            time_maturity = input('Please enter the Time to Maturity (in Month): ')
            check = check_integer(time_maturity)

        check = False
        while check is False:
            storage_cost = input('Please enter the annual Storage cost: ')
            check = check_float(storage_cost)

        check = False
        while check is False:
            insurance_cost = input('Please enter the annual insurance cost: ')
            check = check_float(insurance_cost)

        return float(price) * (1 + (r * (float(time_maturity)/12))) + (float(storage_cost)*(float(time_maturity)/12)) +\
               (float(insurance_cost) + (float(time_maturity)/12))

    if type == 'stock':
        stock_ticker = input('Please enter the stock ticker: ')
        price = input('Please enter the ' + stock_ticker.upper() + ' price: ')
        time_maturity = input('Please enter the Time to Maturity (in months): ')
        stock_type = input('Is the stock ' + stock_ticker.upper() + ' accumulated or distributed? ')

        if stock_type == 'accumulated':
            return float(price) * math.pow(math.e, (r * (float(time_maturity) / 12)))

        if stock_type == 'distributed':
            dividend_type = input('Please enter dividend type (annual/semiannual/quarterly): ')

            if dividend_type == 'annual':
                yearly_dividend = input('enter the yearly dividend: ')
                dividend = float(yearly_dividend) * math.pow(math.e, -r)
                return (float(price) - dividend) * math.pow(math.e, (r * (float(time_maturity) / 12)))

            elif dividend_type == 'semiannual':
                semiannual_dividend = input('enter the semiannual dividend: ')
                dividend = float(semiannual_dividend) * math.pow(math.e, -(r*(6/12))) + float(semiannual_dividend) * \
                           math.pow(math.e, -(r*(12/12)))
                return (float(price) - dividend) * math.pow(math.e, (r * (float(time_maturity) / 12)))

            elif dividend_type == 'quarterly':
                quarterly_dividend = input('enter the quarterly dividend: ')
                dividend = float(quarterly_dividend) * (
                        math.pow(math.e, -(r * (3 / 12))) + math.pow(math.e, -(r * (6 / 12))) +
                        math.pow(math.e, -(r * (9 / 12))) + math.pow(math.e, -(r * (12 / 12))))
                return (float(price) - dividend) * math.pow(math.e, (r * (float(time_maturity) / 12)))


def forward_calculator_automatic(type):
    r = 0.06

    if type == 'commodity':
        commodity_type = input('Please enter the commodity type: ')
        commodity_symbol = input('Please enter the Commodity Symbol for ' + commodity_type + ': ')

        api_key = '3poh7715mjjvc1ho459g49gyz81hfyrs8q44u20i02cvr763wx6igf3l0z9q'
        url = f"https://metals-api.com/api/latest?access_key={api_key}&base=USD&symbols={commodity_symbol.upper()}"
        response = requests.get(url).json()
        rates = response['rates']

        price = 1/rates['XAU']
        time_maturity = input('Please enter the time to maturity (in months): ')
        storage_cost = input('Please enter the annual storage cost: ')
        insurance_cost = input('Please enter the annual insurance cost: ')
        return float(price) * (1 + (r * (float(time_maturity)/12))) + (float(storage_cost)*(float(time_maturity)/12)) +\
               (float(insurance_cost) + (float(time_maturity)/12))

    if type == 'stock':
        stock_ticker = input('Please enter the stock ticker: ')

        api_token = 'c4ub5eqad3ie1t1fq6f0'
        url = f"https://finnhub.io/api/v1/quote?symbol={stock_ticker.upper()}&token={api_token}"
        response = requests.get(url).json()

        price = response['c']
        time_maturity = input('Please enter the Time to Maturity (in months): ')
        stock_type = input('Is the stock ' + stock_ticker.upper() + ' accumulated or distributed? ')

        if stock_type == 'accumulated':
            print(price)
            return float(price) * math.pow(math.e, (r * (float(time_maturity) / 12)))

        if stock_type == 'distributed':
            dividend_type = input('Please enter dividend type (annual/semiannual/quarterly): ')

            if dividend_type == 'annual':
                yearly_dividend = input('enter the yearly dividend: ')
                dividend = float(yearly_dividend) * math.pow(math.e, -r)
                return (float(price) - dividend) * math.pow(math.e, (r * (float(time_maturity) / 12)))

            elif dividend_type == 'semiannual':
                semiannual_dividend = input('enter the semiannual dividend: ')
                dividend = float(semiannual_dividend) * math.pow(math.e, -(r * (6 / 12))) + \
                           float(semiannual_dividend) * math.pow(math.e, -(r * (12 / 12)))
                return (float(price) - dividend) * math.pow(math.e, (r * (float(time_maturity) / 12)))

            elif dividend_type == 'quarterly':
                quarterly_dividend = input('enter the quarterly dividend: ')
                dividend = float(quarterly_dividend) * (
                    math.pow(math.e, -(r * (3 / 12))) + math.pow(math.e, -(r * (6 / 12))) +
                    math.pow(math.e, -(r * (9 / 12))) + math.pow(math.e, -(r * (12 / 12))))
                return (float(price) - dividend) * math.pow(math.e, (r * (float(time_maturity) / 12)))


if __name__ == '__main__':
    stop = False

    while not stop:
        forward_type = input('Please enter the Forward Type (stock or commodity): ')
        question = input('Do you know the current price of the ' + forward_type + ' (yes/no)? ')

        if question == 'yes':
            print(
                'The price of the forward ' + forward_type.upper() + ' is ' + str(forward_calculator_manual(forward_type)))
        else:
            print('The price of the forward ' + forward_type.upper() + ' is ' + str(
                forward_calculator_automatic(forward_type)))

        con = input('Enter continue to do more calculations: ')
        if con != 'continue':
            stop = True
