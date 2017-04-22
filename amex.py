import urllib
import json
import utils
from bs4 import BeautifulSoup

url = 'https://www.americanexpress.com/us/credit-cards/personal-card-application/terms/blue-credit-card/25330-10-0/?print#FeeTable'
r = urllib.urlopen(url)
soup = BeautifulSoup(r, "lxml")
amex_dict = []

# Returns text from html object with matching ID
def getText(s, soup):
	obj = soup.find(class_ = s)
	return obj.get_text().strip()

purchase_apr_text = getText('purchaseaprval', soup)

bt_apr_text = getText('btrateval', soup)
bt_apr_period = utils.findTimePeriods(bt_apr_text)[0]

cash_apr_text = getText('cashrateval', soup)

penalty_apr_text = getText('penaltyrateval', soup)
penalty_apr_min = utils.findTimePeriods(penalty_apr_text)[0]
penalty_apr_review = utils.findTimePeriods(penalty_apr_text)[1]

pay_int_text = getText('payintval', soup)
pay_int_earliest = utils.findTimePeriods(pay_int_text)[0]

tips_text = getText('tipsval', soup)

amex_dict.append({
	'interest_rates_and_interest_charges': {
		'purchase_apr': { 
			'amounts': utils.extractFloats(purchase_apr_text),
			'text': purchase_apr_text
		},
		'balance_transfer_apr': { 
			'amounts': utils.extractFloats(bt_apr_text),
			'period': {'unit': bt_apr_period[0], 'amount': bt_apr_period[1]},
			'text': bt_apr_text
		},
		'cash_advance_apr': {
			'amount': utils.extractFloats(cash_apr_text)[0],
			'text': cash_apr_text
		},
		'penalty_apr': {
			'amount': utils.extractFloats(cash_apr_text)[0],
			'mininum_term': {'unit': penalty_apr_min[0], 'amount': penalty_apr_min[1]},
			'review_period': {'unit': penalty_apr_review[0], 'amount': penalty_apr_review[1],
			'text': penalty_apr_text}
		},
		'due_date': {
			'earliest': {'unit': pay_int_earliest[0], 'amount': pay_int_earliest[1]},
			'text': pay_int_text  
		},
		'tips': {
			'text': tips_text
		}
	}
})

annual_fee_text = getText('annualfeeval', soup)
annual_fee_nums = utils.extractNums(annual_fee_text)

bt_fee_text = getText('balancetransfer', soup)
bt_fee_nums = utils.extractNums(bt_fee_text)

cash_fee_text = getText('cashadvance', soup)
cash_fee_nums = utils.extractNums(cash_fee_text)

foreign_fee_text = getText('foreigntransaction', soup)
foreign_fee_nums = utils.extractNums(foreign_fee_text)

late_fee_text = getText('latepayment', soup)
late_fee_nums = utils.extractNums(late_fee_text)

return_fee_text = getText('returnedpayment', soup)
return_fee_nums = utils.extractNums(return_fee_text)

overlimit_text = soup.findAll(class_ = 'returnedpayment', limit = 2)[1].get_text().strip()

amex_dict.append({
	'fees': {
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
				'maximum_amount' : late_fee_nums[0],
				'text': late_fee_text
			},
			'return_payment': {
				'maximum_amount' : return_fee_nums[0],
				'text': return_fee_nums
			},
			'overlimit': {
				'text': overlimit_text
			}
		}
	}
})




