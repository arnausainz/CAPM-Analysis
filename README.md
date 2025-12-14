# CAPM-Analysis

This project implements the Capital Asset Pricing Model (CAPM) using real market data. 

Its objective is to calculate the Systematic Risk (Beta) and the Theoretical Required Return for x US stocks relative to the S&P 500 benchmark. This automated tool is fundamental for Valuation and Risk teams, providing a key metric for asset pricing and market risk management.

1.- The script’s primary goal is to assess the risk and required compensation for each asset by answering two fundamental questions for each stock:
Systematic Risk (beta): How sensitive is the stock’s return to overall market movements?
Required Return: What is the minimum theoretical return this stock should offer to compensate for its calculated Beta?

2.- Methodology: Excess Returns and Beta CalculationThe core analysis is performed within the CAPM function, which runs for each of the 50 stocks:

Data Preparation: The script downloads historical closing prices and calculates Daily Percentage Returns for both the individual stock and the market benchmark (^GSPC).
Excess Returns Calculation: This is the critical CAPM step.The Annual Risk-Free Rate (RF_A) is converted into a daily rate (rf_daily).Excess Returns (stock and market) are calculated by subtracting this daily risk-free rate from the daily returns. This isolates the returns purely attributable to risk exposure.
Beta Calculation: Beta is derived from the linear relationship between the asset’s excess returns and the market’s excess returns.

3.- Key Results and Performance Metrics

The function outputs several key metrics for financial analysis:

Required Return (required_ret): The theoretical expected return for the asset, calculated using the CAPM formula, based on its sensitivity (Beta) to the market premium.
Annual Return (annual_return): The stock's real average annualized return observed during the period.
Alpha: Measures the stock’s abnormal performance (return achieved above what CAPM predicted).
Sharpe Ratio: Measures risk-adjusted return (excess return divided by the total volatility), providing an efficiency metric for the stock’s historical performance.

4.- Execution and Final Delivery

The main function iterates the CAPM model across all x tickers.The results are organized into a concise Pandas DataFrame containing all the calculated metrics (Beta, Alpha, Required Return, Sharpe Ratio).The final output is an Excel file (Results_CAPM.xlsx), which serves as a professional report detailing the systematic risk and valuation metrics for every analyzed stock.

In summary, this code showcases the ability to apply a foundational financial model (CAPM) to mass market data, providing risk and valuation insights essential for decision-making in a financial institution.
