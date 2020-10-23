import yfinance as yf
import pandas as pd
import csv
import math
import traceback
from multiprocessing import Process, current_process, Pool

# Earnings increase of at least 33% over 10 years using 3 year averages - 10% over 4 years since the API only contains the most recent 4 years
# Current price no more than 1.5x book value per share
# P/E ratio <= 15
# Long term debt no more than 110% current assets
# Current assets 1.5x current liabilities 

def download_data(ticker):

	try:
		company = yf.Ticker(ticker)
		company_info = company.info
		return company
	except:
		return

if __name__ == "__main__":
	all_tickers = []
	symbol_array = []
	failed_search = []


	with open('companylist.csv') as file:
		reader = csv.reader(file)

		ticker_data = iter(reader) # skip the first value since it is the header
		next(ticker_data)

		# loops throught the csv file and adds all the company tickers/symbols to a list
		for row in ticker_data:
			all_tickers.append(row[0])

	# creates a pool of workers to which jobs can be submitted. By default the number of workers are the number of cores available on the CPU of the machine
	p = Pool()

	# maps the "all_tickers" list to the "download_data" function and executes the function in parallel manner. The "results" variable is an array containing an object for each company within the CSV file
	results = p.map(download_data, all_tickers)

	# these lines of code ensure the data has been downloaded before any other code is executed
	p.close()
	p.join()

	# once the data has been downloaded, this loop iterates through the results list which contain an object for each company in the csv file. The object contains all the financial data required to make the necessary checks
	for company in results:

		try:

			if company:
				company_info = company.info

				company_balance_sheet = company.balance_sheet
				company_earnings = company.earnings

				if company_balance_sheet.empty or company_earnings.empty:
					continue # if balance sheets or earnings reports are not available, skip the search

				column_date = company.balance_sheet.columns[0] # latest date on balance sheet to take data from
				current_assets = company.balance_sheet.at['Total Current Assets', column_date]

				try: # previous close price can be under 'previousClose' or 'regularMarketPrice' in company_info
					current_price = company_info['previousClose']
				except:
					current_price = company_info['regularMarketPrice']

				if current_price < 10:
					continue


				try:
					long_term_debt = company.balance_sheet.at['Long Term Debt', column_date]
					if math.isnan(long_term_debt):
						long_term_debt = 0

				except:
					long_term_debt = 0

				if long_term_debt < (current_assets * 1.1):
	 				current_liabilities = company.balance_sheet.at['Total Current Liabilities', column_date]

	 				if current_liabilities < (1.5 * current_assets):

	 					try:
	 						pe_ratio = company_info['trailingPE'] # check if P/E ratio is available, assign pe_ratio 0 if it is not
	 					except:
	 						pe_ratio = 0

	 					if pe_ratio <= 15:

	 						try: # previous close price can be under 'previousClose' or 'regularMarketPrice' in company_info
	 							current_price = company_info['previousClose']
	 						except:
	 							current_price = company_info['regularMarketPrice']

	 						try:
	 							book_value = company_info['bookValue']
	 							if type(book_value) != float: # book_value can be "None" in the company_info object
	 								book_value = 0
	 						except:
	 							book_value = 0

	 						if current_price < (book_value*1.5):
	 							earnings_first = company.earnings.iat[0, 1]
	 							earnings_last = company.earnings.iat[len(company.earnings)-1, 1]

	 							if earnings_last >= earnings_first*1.1:
	 								symbol_array.append(company_info['symbol'])

		except Exception as e:
			print(traceback.format_exc()) # code to point out any errors in the main try statement
			failed_search.append(company_info["symbol"])
			print(f"{company_info['symbol']} failed to search")
			print(e)
				
	print('Failed searches:')
	for failure in failed_search:
		print(failure)

	print('Potential Investments:')
	for symbol in symbol_array:
		print(symbol)
