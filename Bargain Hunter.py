import yfinance as yf
import pandas as pd
import openpyxl
import csv
import math
import traceback

# Earnings increase of at least 33% over 10 years using 3 year averages - 10% over 4 years since the API only contains the most recent 4 years
# Current price no more than 1.5x book value per share
# P/E ratio <= 15
# Long term debt no more than 110% current assets
# Current assets 1.5x current liabilities 

print('Started')

symbol_array = []

failed_search = []

with open('companylist.csv') as file:
	reader = csv.reader(file)

	ticker_data = iter(reader) # skip the first value since it is the header
	next(ticker_data)

	for row in ticker_data:
		ticker = row[0]
		print('Searching: ', ticker)

		try:
			try:
				company = yf.Ticker(ticker)
				company_info = company.info 
			except:
				print('Not a company')
				continue # skip the ticker since it is not a company or the API doesn't have any information about the security

			company_balance_sheet = company.balance_sheet
			company_earnings = company.earnings

			if company_balance_sheet.empty or company_earnings.empty: # HEREEEEE
				continue

			column_date = company.balance_sheet.columns[0] # latest date on balance sheet to take data from

			current_assets = company.balance_sheet.at['Total Current Assets', column_date]
			
			try:
				long_term_debt = company.balance_sheet.at['Long Term Debt', column_date]
				if math.isnan(long_term_debt):
					long_term_debt = 0
			except:
				long_term_debt=0

			if long_term_debt < (current_assets * 1.1):
				
				current_liabilities = company.balance_sheet.at['Total Current Liabilities', column_date]
				
				if current_liabilities < (1.5 * current_assets):

					try:
						pe_ratio = company_info['trailingPE'] # check if P/E ratio is available
					except:
						pe_ratio = 0


					if pe_ratio < 15:

						try:
							current_price = company_info['previousClose']
						except:
							current_price = company_info['regularMarketPrice']

						try:	
							book_value = company_info['bookValue']
						except:
							book_value = 0
						
						if type(book_value) != float or current_price < (book_value*1.5):
							earnings_first = company.earnings.iat[0, 1]
							earnings_last = company.earnings.iat[len(company.earnings)-1, 1] # ERROR HERE TOO HOE might not be that many entries boiiiii

							if earnings_last >= earnings_first*1.1:
								symbol_array.append(company_info['symbol'])

							else:
								print('Step 5 fail. Earnings growth too low')

						else:
							print('Step 4 fail. Current price too high')

					else:
						print('Step 3 fail. P/E ratio too high')

				else:
					print('Step 2 fail. Current liabilities too high')

			else:
				print('Step 1 fail. Long term debt too high')

		except Exception as e:
			print(traceback.format_exc()) # code to point out any errors in the main try statement
			failed_search.append(ticker)
			print(ticker, ' failed to search.')
			print(e)

print('Failed searches:')
for failure in failed_search:
	print(failure)

print('Potential Investments:')

for symbol in symbol_array:
	print(symbol)
