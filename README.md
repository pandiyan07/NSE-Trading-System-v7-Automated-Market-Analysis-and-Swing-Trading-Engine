# Project Title

**NSE Trading System v7 - Automated Market Analysis & Swing Trading Engine**

## Table of Contents

-   About The Project
-   Built With
-   Key Features
-   Getting Started
-   Technologies Used (Prerequisites)
-   Installation
-   Usage
-   Project Structure
-   How It Works
-   Main Python Functions
-   Output
-   Future Enhancements
-   License Description
-   Disclaimer

## About The Project

Built on - June 2024

This project is a modular Python-based trading system that automates
Indian stock market analysis using Yahoo Finance, NSELive and NSELib. It
combines scheduled data collection, multi-process execution, technical
indicator calculations, breakout detection, ORB analysis, circuit
analysis, price-change analysis, ranking, and report generation to
identify high-probability swing and positional trading opportunities.

### Built With

-   Python 3
-   pandas
-   yfinance
-   nselib
-   jugaad-data
-   multiprocessing
-   datetime
-   NumPy

### Key Features

-   Automated market scheduler
-   Multiprocessing architecture
-   Live NSE data collection
-   Historical OHLCV download
-   RSI calculations
-   ORB analysis
-   20 Moving Average analysis
-   One, Two and Three-candle breakout detection
-   Three-candle volume breakout detection
-   Percentage price change calculation
-   Upper/Lower circuit detection
-   Stock consistency ranking
-   Consolidated report generation

## Getting Started

### Technologies Used (Prerequisites)

-   Python 3.10+
-   pip
-   Internet connection
-   NSE data access

Install dependencies:

``` bash
pip install pandas numpy yfinance nselib jugaad-data
```

### Installation

``` bash
git clone https://github.com/pandiyan07/NSE-Trading-System-v7-Automated-Market-Analysis-and-Swing-Trading-Engine.git
cd NSE-Trading-System-v7-Automated-Market-Analysis-and-Swing-Trading-Engine
pip install -r requirements.txt
python Trading_system_v7.py
```

## Usage

Execute the main application to automatically schedule data collection,
analyze all configured stocks, compute technical metrics, rank
candidates and print consolidated trading reports.

## Project Structure

``` text
Trading_system_v7.py      # Main controller and multiprocessing coordinator
APPENDER.py               # Technical indicators and stock analysis engine
SCHEDULER.py              # Data scheduling and live data collection
PRINTER.py                # Ranking, filtering and report generation
```

## How It Works

1.  Initialize configuration and multiprocessing.
2.  Schedule market data collection.
3.  Download live and historical market data.
4.  Process each stock independently.
5.  Calculate RSI and moving averages.
6.  Detect price and volume breakouts.
7.  Calculate ORB percentage.
8.  Detect upper/lower circuits.
9.  Calculate percentage price change.
10. Rank qualifying stocks.
11. Merge all worker results.
12. Generate consolidated output tables.

## Main Python Functions

  -----------------------------------------------------------------------
  Function                            Description
  ----------------------------------- -----------------------------------
  `THE_MAIN()`                        Main orchestration function
                                      controlling the complete trading
                                      workflow.

  `JUGAAD_DATA()`                     Retrieves live NSE stock
                                      information.

  `DATA_FETCHER()`                    Downloads and prepares market data.

  `SCHEDULE_TASK()`                   Executes scheduled market scans.

  `SCHEDULE_INITIATOR()`              Starts the scheduling engine.

  `RSI_14_AVERAGE_CALCULATOR()`       Calculates 14-period RSI.

  `TWENTY_MA_CALCULATOR()`            Computes 20-period Moving Average.

  `ONE_CANDLE_PRICE_BREAKOUT()`       Detects single-candle breakout
                                      patterns.

  `TWO_CANDLE_PRICE_BREAKOUT()`       Detects two-candle breakout
                                      patterns.

  `THREE_CANDLE_PRICE_BREAKOUT()`     Detects three-candle breakout
                                      patterns.

  `THREE_CANDLE_VOLUME_BREAKOUT()`    Detects abnormal three-candle
                                      volume breakouts.

  `pCHANGE_CALCULATOR()`              Calculates percentage price change.

  `UPPER_AND_LOWER_CIRCUIT()`         Detects stocks near exchange
                                      circuit limits.

  `ORB()`                             Calculates Open Range Breakout
                                      metrics.

  `DATA_PROCESSOR()`                  Aggregates indicator calculations
                                      for each stock.

  `COMMON_STOCKS()`                   Finds stocks satisfying multiple
                                      conditions.

  `CONSISTENCY_RANKING()`             Produces stock rankings based on
                                      strategy metrics.

  `OUTPUT_PRINTER()`                  Displays formatted reports.

  `DATAFRAME_GENERATOR()`             Builds final Pandas DataFrames.
  -----------------------------------------------------------------------

## Output

-   Ranked stock tables
-   Breakout candidates
-   ORB rankings
-   RSI and Moving Average analysis
-   Volume breakout results
-   Consolidated trading report

## Future Enhancements

-   TradingView alerts
-   Excel/PDF exports
-   Web dashboard
-   Broker API integration
-   Order execution
-   Backtesting module

## License Description

Recommended License: MIT License.

Permission is granted to use, modify, distribute and commercialize the
software while preserving the copyright notice.

## Disclaimer

This software is intended for educational and research purposes only. It
does not provide financial advice or guarantee trading performance.
Always validate strategies before deploying them in live markets.
