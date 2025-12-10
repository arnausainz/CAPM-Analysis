import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from datetime import datetime, date

#PARÁMETROS
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "JPM", "JNJ", "NVDA", "XOM",
    "V", "PG", "UNH", "HD", "BAC", "DIS", "MA", "PYPL", "ADBE", "NFLX",
    "KO", "CSCO", "PFE", "NKE", "CRM", "MRK", "ABT", "PEP", "INTC", "T",
    "WMT", "CVX", "ORCL", "COST", "QCOM", "ACN", "AVGO", "TXN", "LLY", "MCD",
    "MDT", "NEE", "HON", "PM", "AMGN", "DHR", "IBM", "LOW", "SBUX", "BMY"
]
MARKET = "^GSPC"
START = date(2020, 1, 1)
END = date(2024, 12, 31)
RF_A = 0.02 #Tasa libre de riesgo anual
PERIOD = 252 #Días hábiles del año

def get_data(tickers, market=MARKET, start=START, end=END):

    #descargamos datos
    data = yf.download(tickers + [market], start=start, end=end, auto_adjust = True)['Close']
    
    return data

def CAPM(data, ticker, market=MARKET):

    #buscamos los retornos
    ret = data.pct_change().dropna()

    #anualizamos retornos
    daily_return = ret[ticker].mean()                 # Solo la columna de la acción
    annual_return = (1 + daily_return)**PERIOD - 1 

    #tasa libre de riesgo anual la convertimos en diaria
    rf_daily = (1 + RF_A)**(1/PERIOD) - 1
    
    #Rendimientos "Extra"
    excess_stock = ret[f'{ticker}'] - rf_daily #rendimiento extra del stock respecto a la tasa libre de riesgo
    excess_market = ret[f'{market}'] - rf_daily #rendimiento extra del mercado respecto a la tasa libre de riesgo
    
    #Calculamos Beta
    
    cov_matrix = np.cov(excess_stock, excess_market, ddof=1)
    beta = cov_matrix[0,1]/cov_matrix[1,1]
    
    #Si quiero ver la matriz de covarianza en plan df, para verla mejor.
    #cov_matrix = pd.DataFrame(cov_matrix, columns = [f'{TICKER}', f'{MARKET}'], index = [f'{TICKER}', f'{MARKET}'])
    
    #Calculamos el alpha diario
    
    alpha_daily = excess_stock.mean() - beta * (excess_market.mean())
    
    #anualizamos el alpha
    alpha_annual = (1+alpha_daily)**PERIOD -1
    
    #Prima de mercado anualizada (aprox):
    market_premium_annual = (1+excess_market.mean())**PERIOD-1
    
    #Returns requeridos según CAPM
    required_ret = RF_A + beta * market_premium_annual

    #Calculamos el sharpe ratio

    sharpe = (annual_return - RF_A) / (ret[ticker].std() * np.sqrt(PERIOD))
    
    return {"Beta": beta, "Alpha" : alpha_annual, "Market Premium" : market_premium_annual,
            "Required Return" : required_ret, "Annual Return": annual_return, "Sharpe Ratio": sharpe}

def main(tickers, market):
    
    data = get_data(tickers, market)

    results = []

    for ticker in tickers:
        res = CAPM(data, ticker, market)
        results.append((ticker,res))

    df = pd.DataFrame({t: r for t, r in results}).T
    
    return df

results = main(TICKERS, MARKET)

#Lo descargamos en un excel

with pd.ExcelWriter("Results_CAPM.xlsx", engine='xlsxwriter') as writer:
    results.to_excel(writer, sheet_name="CAPM Results", index=True)
