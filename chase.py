import urllib
import utils
from bs4 import BeautifulSoup

url = "https://applynow.chase.com/FlexAppWeb/pricing.do?card=FNPN&page_type=appterms"
r = urllib.urlopen(url)
soup = BeautifulSoup(r, "lxml")
chase_dict = []
texts = [tag.get_text().strip().encode("utf-8") for tag in soup.findAll('p')]

purchase_apr_text = texts[3]
purchase_apr_nums = utils.extract_nums(purchase_apr_text)

bt_apr_text = texts[5]
bt_apr_nums = utils.extract_nums(bt_apr_text)

ca_apr_text = texts[7]
ca_apr_nums = utils.extract_nums(ca_apr_text)

pay_int_text = texts[9]
pay_int_earliest = utils.find_time_periods(pay_int_text)[0]

min_charge_text = texts[11]

tips_text = texts[13]

prime_rate_text = texts[33]
prime_rate_nums = utils.extract_nums(prime_rate_text)

chase_dict.append({
    'interest_rates_and_interest_charges': {
        'purchase_apr': {
            'low_amount': purchase_apr_nums[0],
            'high_amount': purchase_apr_nums[1],
            'text': purchase_apr_text
        },
        'balance_transfer_apr': {
            'low_amount': bt_apr_nums[0],
            'high_amount': bt_apr_nums[1],
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
            'text': min_charge_text
        },
        'tips': {
            'text': tips_text
        },
        'prime_rate': {
            'amount': prime_rate_nums[0],
            'date_updated': {
                'month': prime_rate_nums[1],
                'day': prime_rate_nums[2],
                'year': prime_rate_nums[3]
            },
            'text': prime_rate_text
        }
    }
})

annual_fee_text = texts[16]
annual_fee_nums = utils.extract_nums(annual_fee_text)

bt_fee_text = texts[19]
bt_fee_nums = utils.extract_nums(bt_fee_text)

cash_fee_text = texts[21]
cash_fee_nums = utils.extract_nums(cash_fee_text)

foreign_fee_text = texts[23]

late_fee_text = texts[26]
late_fee_nums = utils.extract_nums(late_fee_text)

return_fee_text = texts[28]
return_fee_nums = utils.extract_nums(return_fee_text)

return_check_text = texts[30]

chase_dict.append({
    'fees': {
        'annual_membership_fee': {
            'intro_amount': annual_fee_nums[0],
            'normal_amount': annual_fee_nums[1],
            'text': annual_fee_text
        },
        'transaction_fees': {
            'balance_transfers': {
                'dollar_amount': bt_fee_nums[0],
                'percentage': bt_fee_nums[1],
                'text': bt_fee_text
            },
            'cash_advances': {
                'dollar_amount': cash_fee_nums[0],
                'percentage': cash_fee_nums[1],
                'text': cash_fee_text
            },
            'foreign': {
                'text': foreign_fee_text
            }
        },
        'penalty_fees': {
            'late_payment': {
                'low_range': {
                    'upper_balance': late_fee_nums[1],
                    'maximum_fee': late_fee_nums[0]
                },
                'middle_range': {
                    'lower_balance': late_fee_nums[3],
                    'upper_balance': late_fee_nums[4],
                    'maximum_fee': late_fee_nums[2]
                },
                'high_range': {
                    'lower_balance': late_fee_nums[6],
                    'maximum_fee': late_fee_nums[5]
                },
                'text': late_fee_text
            },
            'return_payment': {
                'maximum_fee': return_fee_nums[0],
                'text': return_fee_text
            },
            'return_check': {
                'text': return_check_text
            }
        }
    }
})
