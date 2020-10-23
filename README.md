# Bargain-Hunter
A simple algorithm to look through companies and pick out stocks that meet the criteria. The criteria was inspired by Benjamin Graham's 'The Intelligent Investor' (https://www.e-reading-lib.com/bookreader.php/133361/The_Intelligent_Investor.pdf page 362 and page 399).

The criteria includes:
1) Long term debt less than 1.1x current assets.
2) Current assets at least 1.5x current liabilities
3) P/E ratio <= 15
4) Current price no more than 1.5x book value per share
5) Minimum earnings increase of 10% over 4 years

The algorithm loops through a csv file taken from https://old.nasdaq.com/screening/company-list.aspx to retrieve symbols used in the search since the Yahoo Finance API does not contain a request function to return all symbols/tickers available on the API.
This algorithm aims to find large and financially stable companies whose stock price is currently undervalued (due to a bear market, or a temporary factor such as bad news that has affected a stock's price dramatically)

After using this algorithm, I realised the largest bottleneck was waiting for data to be retrieved from the API. To reduce this bottleneck, I implemented parallel processing which includes downloading multiple pieces of information concurrently. This has substantially improved the time efficiency of the algorithm.

Instructions on how to run the code:
1. Download the CSV file along with either the "Bargain Hunter.py" or "Bargain HunterV2.py" files. Store the files together in one folder.
2. Install the dependencies:
  -Install the yfinance module for the Yahoo Finance API (type "pip install yfinance --upgrade --no-cache-dir" into the terminal)
  -Install pandas (by typing "pip install pandas" into the terminal)
3. Open "Bargain Hunter" or "Bargain HunterV2" in a Python IDE and press run.
4. Wait for the 
