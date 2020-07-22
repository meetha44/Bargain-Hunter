# Bargain-Hunter
A simple algorithm to look through companies and pick out stocks that meet the criteria. The criteria was inspired by Benjamin Graham's 'The Intelligent Investor' (https://www.e-reading-lib.com/bookreader.php/133361/The_Intelligent_Investor.pdf page 362 and page 399).

The criteria includes:
1) Long term debt less than 110% current assets.
2) Current assets at least 1.5x current liabilities
3) P/E ratio <= 15
4) Current price no more than 1.5x book value per share
5) Earnings increase of 10% over 4 years

The algorithm loops through a csv file taken from https://old.nasdaq.com/screening/company-list.aspx to retrieve symbols used in the search since the Yahoo Finance API does not contain an API function to return all symbols/tickers available on the API.
This algorithm aims to find large and financially stable companies whose stock price is currently undervalued (due to a bear market, or a temporary factor such as bad news that has affected a stock's price dramatically)
