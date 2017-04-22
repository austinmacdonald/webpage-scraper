import urllib
import utils
from bs4 import BeautifulSoup

url = "https://www.wellsfargo.com/credit-cards/cash-back-college-card/terms"
r = urllib.urlopen(url)
soup = BeautifulSoup(r, "lxml")
wells_fargo_dict = {'name': 'Wells Fargo College Card'}
texts = [tag.get_text().strip() for tag in soup.findAll('td')]

purchase_apr_text = texts[0]
purchase_apr_nums = utils.extract_floats(purchase_apr_text)
purchase_intro_term = utils.find_time_periods(purchase_apr_text)[0]

bt_apr_text = texts[1]
bt_apr_nums = utils.extract_floats(bt_apr_text)
bt_intro_term = utils.find_time_periods(bt_apr_text)[0]

ca_apr_text = texts[2]
ca_apr_nums = utils.extract_nums(ca_apr_text)

pay_int_text = texts[3]
pay_int_earliest = utils.find_time_periods(pay_int_text)[0]

min_charge_text = texts[4]
min_charge_nums = utils.extract_nums(min_charge_text)

tips_text = texts[5]

wells_fargo_dict['interest_rates_and_interest_charges'] = {
    'purchase_apr': {
        'introductory_apr': {
            'term': {'units': purchase_intro_term[0], 'amount': purchase_intro_term[1]},
            'low_amount': purchase_apr_nums[0],
            'high_amount': purchase_apr_nums[0]
        },
        'normal_apr': {
            'low_amount': purchase_apr_nums[1],
            'high_amount': purchase_apr_nums[2]
        },
        'text': purchase_apr_text
    },
    'balance_transfer_apr': {
        'introductory_apr': {
            'term': {'units': bt_intro_term[0], 'amount': bt_intro_term[1]},
            'low_amount': bt_apr_nums[0],
            'high_amount': bt_apr_nums[0]
        },
        'normal_apr': {
            'low_amount': bt_apr_nums[1],
            'high_amount': bt_apr_nums[2]
        },
        'text': bt_apr_text
    },
    'cash_advance_apr': {
        'amount': ca_apr_nums[0],
        'text': ca_apr_text
    },
    'due_date': {
        'earliest': {'unit': pay_int_earliest[0], 'amount': pay_int_earliest[1]},
        'text': pay_int_text
    },
    'minimum_interest_charge': {
        'text': min_charge_text,
        'amount': min_charge_nums[0]
    },
    'tips': {
        'text': tips_text
    }
}


annual_fee_text = texts[6]

bt_fee_text = texts[8]
bt_fee_nums = utils.extract_nums(bt_fee_text)
bt_intro_term = utils.find_time_periods(bt_fee_text)[0]

cash_fee_text = texts[9]
cash_fee_nums = utils.extract_nums(cash_fee_text)

overdraft_fee_text = texts[10]
overdraft_fee_nums = utils.extract_nums(overdraft_fee_text)

foreign_fee_text = texts[11]
foreign_fee_nums = utils.extract_nums(foreign_fee_text)

late_fee_text = texts[13]
late_fee_nums = utils.extract_nums(late_fee_text)

return_fee_text = texts[14]
return_fee_nums = utils.extract_nums(return_fee_text)

wells_fargo_dict['fees'] = {
    'annual_membership_fee': {
        'text': annual_fee_text
    },
    'transaction_fees': {
        'balance_transfers': {
            'introductory_fee': {
                'dollar_amount': bt_fee_nums[0],
                'percentage': bt_fee_nums[1],
                'term': {'unit': bt_intro_term[0], 'amount': bt_intro_term[1]}
            },
            'normal_fee': {
                'dollar_amount': bt_fee_nums[4],
                'percentage': bt_fee_nums[3]
            },
            'text': bt_fee_text
        },
        'cash_advances': {
            'dollar_amount': cash_fee_nums[0],
            'percentage': cash_fee_nums[1],
            'text': cash_fee_text
        },
        'overdraft': {
            'lower_range': {
                'dollar_amount': overdraft_fee_nums[0],
                'upper_advances': overdraft_fee_nums[1]
            },
            'upper_range': {
                'dollar_amount': overdraft_fee_nums[2],
                'lower_advances': overdraft_fee_nums[3]
            },
            'text': overdraft_fee_text
        },
        'foreign': {
            'percentage': foreign_fee_nums[0],
            'text': foreign_fee_text
        }
    },
    'penalty_fees': {
        'late_payment': {
            'maximum_fee': late_fee_nums[0],
            'text': late_fee_text
        },
        'return_payment': {
            'maximum_fee': return_fee_nums[0],
            'text': return_fee_text
        }
    }
}
