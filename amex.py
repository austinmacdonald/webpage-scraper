import urllib
import utils
from bs4 import BeautifulSoup

url = 'https://www.americanexpress.com/us/credit-cards/personal-card-application/terms/' \
      'blue-credit-card/25330-10-0/?print#FeeTable '
r = urllib.urlopen(url)
soup = BeautifulSoup(r, "lxml")
amex_dict = {'name': 'Amex Blue'}


# Returns text from html object with matching class C
def get_text(c):
    obj = soup.find(class_=c)
    return obj.get_text().strip()


purchase_apr_text = get_text('purchaseaprval')
purchase_apr_amts = utils.extract_floats(purchase_apr_text)

bt_apr_text = get_text('btrateval')
bt_apr_amts = utils.extract_floats(bt_apr_text)
bt_apr_period = utils.find_time_periods(bt_apr_text)[0]

cash_apr_text = get_text('cashrateval')

penalty_apr_text = get_text('penaltyrateval')
penalty_apr_min = utils.find_time_periods(penalty_apr_text)[0]
penalty_apr_review = utils.find_time_periods(penalty_apr_text)[1]

pay_int_text = get_text('payintval')
pay_int_earliest = utils.find_time_periods(pay_int_text)[0]

tips_text = get_text('tipsval')

amex_dict['interest_rates_and_interest_charges'] = {
    'purchase_apr': {
        'low_amount': purchase_apr_amts[0],
        'middle_amount': purchase_apr_amts[1],
        'high_amount': purchase_apr_amts[2],
        'text': purchase_apr_text
    },
    'balance_transfer_apr': {
        'low_amount': bt_apr_amts[0],
        'middle_amount': bt_apr_amts[1],
        'high_amount': bt_apr_amts[2],
        'period': {'unit': bt_apr_period[0], 'amount': bt_apr_period[1]},
        'text': bt_apr_text
    },
    'cash_advance_apr': {
        'amount': utils.extract_floats(cash_apr_text)[0],
        'text': cash_apr_text
    },
    'penalty_apr': {
        'amount': utils.extract_floats(penalty_apr_text)[0],
        'minimum_term': {'unit': penalty_apr_min[0], 'amount': penalty_apr_min[1]},
        'review_period': {'unit': penalty_apr_review[0], 'amount': penalty_apr_review[1]},
        'text': penalty_apr_text
    },
    'due_date': {
        'earliest': {'unit': pay_int_earliest[0], 'amount': pay_int_earliest[1]},
        'text': pay_int_text
    },
    'tips': {
        'text': tips_text
    }
}

annual_fee_text = get_text('annualfeeval')
annual_fee_nums = utils.extract_nums(annual_fee_text)

bt_fee_text = get_text('balancetransfer')
bt_fee_nums = utils.extract_nums(bt_fee_text)

cash_fee_text = get_text('cashadvance')
cash_fee_nums = utils.extract_nums(cash_fee_text)

foreign_fee_text = get_text('foreigntransaction')
foreign_fee_nums = utils.extract_nums(foreign_fee_text)

late_fee_text = get_text('latepayment')
late_fee_nums = utils.extract_nums(late_fee_text)

return_fee_text = get_text('returnedpayment')
return_fee_nums = utils.extract_nums(return_fee_text)

overlimit_text = soup.findAll(class_='returnedpayment', limit=2)[1].get_text().strip()

amex_dict['fees'] = {
    'annual_membership_fee': {
        'amount': annual_fee_nums[0],
        'text': annual_fee_text
    },
    'transaction_fees': {
        'balance_transfer': {
            'dollar_amount': bt_fee_nums[0],
            'percentage': bt_fee_nums[1],
            'text': bt_fee_text
        },
        'cash_advance': {
            'dollar_amount': cash_fee_nums[0],
            'percentage': cash_fee_nums[1],
            'text': cash_fee_text
        },
        'foreign_transaction': {
            'percentage': foreign_fee_nums[0],
            'text': foreign_fee_text
        }
    },
    'penalty_fees': {
        'late_payment': {
            'maximum_amount': late_fee_nums[0],
            'text': late_fee_text
        },
        'return_payment': {
            'maximum_amount': return_fee_nums[0],
            'text': return_fee_text
        },
        'overlimit': {
            'text': overlimit_text
        }
    }
}
