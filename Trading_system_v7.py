#   python "d:/Trading/Python/Code/Trading system v7.py"
#   Trading system v7 - 

'''

4) Just like the Swing trading, calculate the stocks which has a suddenly risen in volume by looking for stocks which has
volume 2 times more than the day average using the 2 minute candle data
.
The program should consider '"last 3 day trading day"' & today's volume for getting the average value and check for the 2min candle times
where the volume shoots up more than 2 times
.
So that you can find the stocks which has continous buying
.
We need to create a table where  stock with maximum number of time the average value should be sroted in descending order
. 
download 2 minutes data of last 3d in the first iteration then from 2nd iteration onwards download only the current day
data only and add the previous data that was downloaded early 




############   Disable the RSI_CALCULATING function and download only 1 day data only, to avoid traffic


3)  print the latest/last/recently updated, The top sorted BREAKOUT STOCKS are :- datafrme table with the rank score,
to a excel sheet with all the entire rows mentioned in it (and not just the first 20rows) and rename the file to today's date & week day



4)  put the JUGAAD_DATA() function in the scheduler task file, downloading it in asynchronous 
way with 4 processes
.
the scheduler should have 4 processes each running on each core
.
first the scheduler should start downloading the jugaad data in ASYNCHRONOUS WAY 
.
Then the yfinance data should be downloaded by dividing it among all the 4 processes
.
Then the yfinance library should append the downloaded dataframe downloades
.
Ask GEMINI how to append 2 multicolumn dataframes into 1 single dataframe table
.
check and verify if the data downloaded is fetched properly and appended properly using 10 stocks
.
.
.
.
let the ychange extracted data first DOWNLOAD & PROCESS & PRINT its output
and then let the jugaad_data data start its fetching
.
.
.
.
shift the last for loop in main function to the PRINTER FILE.py
.
.
.
.
Just like yfinance has = STARTING TO FETCH =  10:04:34
also mention the FETCHING ENDED = time as well
and then include the start and end fetching for the jugaad data as well
.
.
.
.
the yfinance data download should happen every 1 minute only
( In Flask the data should refresh every 30 seconds or else it can extend 1 minute due to network traffic)
.
but at the same time simultaneously let the JUGAAD DATA download only at the start of once every "five 1 minute iterations" 
and also display the below data once every 5 minutes -
- upper & lower circuit 
- OBV data
- ADVANCE & DECLINE stocks
.


1)  Create a separate table which has max number of ranking iterations in the ranking system and
print the descending sorted table

2)      create 4 tables sorted with top 10 stocks with 
-       highest postive pchange
-       lowest negative pchange
-       ascending sorted average rsi value 
-       descending sorted average rsi value
-       OBV

11)     Along with the above OBV, also print the top 10 high & low average RSI value tables below them

2)      Trade especially after 10am using the OBV & Average RSI table 
'''


from SCHEDULER import *
from APPENDER import *
from PRINTER import *


from jugaad_data.nse import NSELive
import multiprocessing
import time
import sys
from datetime import datetime

current_process = multiprocessing.current_process()
process_name = current_process.name
event = multiprocessing.Event()

try:
    n = NSELive()
except Exception as e:
    print ('\n\n\n\n\n\n',repr(e))
    print ('There is NO INTERNET CONNECTION dude...!!\n\n\n\n\n\n')
    sys.exit(1)

'''
eqList = ["ABB.NS", "ACC.NS","APLAPOLLO.NS", "AUBANK.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "UNITDSPR.NS",
"ADANIPOWER.NS", "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", 
"ASIANPAINT.NS", "ASTRAL.NS", "AUROPHARMA.NS", "DMART.NS", "AXISBANK.NS", "BSE.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", 
"BAJAJHLDNG.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "MAHABANK.NS", "BERGEPAINT.NS", "BDL.NS"]
'''

eqList = ["INFY.NS", "AUBANK.NS","ITC.NS","WIPRO.NS","TCS.NS", 'HDFCBANK.NS','ICICIBANK.NS','BHARTIARTL.NS', 'SBIN.NS', "HEROMOTOCO.NS", "SBIN.NS", "AXISBANK.NS"]

'''
eqList = ["ABB.NS", "ACC.NS","APLAPOLLO.NS", "AUBANK.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "UNITDSPR.NS",
"ADANIPOWER.NS", "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", 
"ASIANPAINT.NS", "ASTRAL.NS", "AUROPHARMA.NS", "DMART.NS", "AXISBANK.NS", "BSE.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", 
"BAJAJHLDNG.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "MAHABANK.NS", "BERGEPAINT.NS", "BDL.NS",  
"BHARATFORG.NS", "BHEL.NS", "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BOSCHLTD.NS", "BRITANNIA.NS", "CGPOWER.NS", "CANBK.NS", "CHOLAFIN.NS", 
"CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "CUMMINSIND.NS", "DLF.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", 
"DELHIVERY.NS", "DIVISLAB.NS", "DIXON.NS", "LALPATHLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS", "NYKAA.NS", "FEDERALBNK.NS", 
"FACT.NS", "FORTIS.NS", "GAIL.NS", "GMRINFRA.NS", "GLAND.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRASIM.NS", "GUJGASLTD.NS", "HCLTECH.NS", 
"HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HAVELLS.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HAL.NS", "HINDPETRO.NS", "HINDUNILVR.NS", 
"ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDBI.NS", "IDFCFIRSTB.NS", "ITC.NS", "INDIANB.NS", "INDHOTEL.NS", "IOC.NS", "SIEMENS.NS",
"IRFC.NS", "IGL.NS", "INDUSTOWER.NS", "INDUSINDBK.NS", "NAUKRI.NS", "INFY.NS", "INDIGO.NS", "IPCALAB.NS","JSWENERGY.NS", "JSWINFRA.NS",
"JSWSTEEL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "JUBLFOOD.NS", "KPITTECH.NS", "KALYANKJIL.NS","BEL.NS","IRCTC.NS","PNB.NS","M&MFIN.NS",
"KOTAKBANK.NS", "LTF.NS", "LTTS.NS", "LICHSGFIN.NS", "LTIM.NS", "LT.NS", "LAURUSLABS.NS", "LICI.NS", "LUPIN.NS", "MRF.NS", "LODHA.NS", 
"M&M.NS", "MANKIND.NS", "MARICO.NS", "MARUTI.NS", "MFSL.NS", "MAXHEALTH.NS", "MPHASIS.NS", "NHPC.NS", "NMDC.NS", "NTPC.NS",
"NESTLEIND.NS", "OBEROIRLTY.NS", "ONGC.NS", "OIL.NS", "PAYTM.NS", "OFSS.NS", "POLICYBZR.NS", "PIIND.NS", "PAGEIND.NS", "PATANJALI.NS",
"PERSISTENT.NS", "PETRONET.NS", "PIDILITIND.NS", "PEL.NS", "POLYCAB.NS", "POONAWALLA.NS", "PFC.NS", "POWERGRID.NS", "PRESTIGE.NS", 
"RECLTD.NS", "RVNL.NS", "RELIANCE.NS", "SBICARD.NS", "SBILIFE.NS", "SJVN.NS", "SRF.NS", "MOTHERSON.NS", "SHREECEM.NS", "SHRIRAMFIN.NS", 
"SONACOMS.NS", "SBIN.NS", "SAIL.NS", "SUNPHARMA.NS", "SUNTV.NS", "SUPREMEIND.NS", "SUZLON.NS", "SYNGENE.NS", "TVSMOTOR.NS", "TATACHEM.NS",
"TATACOMM.NS", "TCS.NS", "TATACONSUM.NS", "TATAELXSI.NS", "TATAMTRDVR.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TATATECH.NS",
"TECHM.NS", "TITAN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TIINDIA.NS", "UPL.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "ZYDUSLIFE.NS",
"VBL.NS", "VEDL.NS", "IDEA.NS", "VOLTAS.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS", "ZOMATO.NS", "MAZDOCK.NS"]

'''

# RUN THIS CODE FROM THE START OF THE MARKET AT - 9:19:30am
#   Enable this daily morning in    ====>    SCHEDULER python file in while loop of SCHEDULE_TASK() function
#   Also disbale the trading_system_start_time variable current time assignment in the below given Main function
target_start_hour, target_start_minute, target_start_second = 9, 16, 40 
trading_system_start_time = datetime.now().replace(hour=target_start_hour, minute=target_start_minute, second=target_start_second)


def THE_MAIN(j,Stock,pChange,total_traded_volume,last_three_volume,twenty_ma,up_and_low_circuit,orb,ten_min_bo_dict,five_min_bo_dict,two_min_RSI_avg,five_min_RSI_avg,
            breakout,bopp,yfd_dict,lock,final_ORB_dict,ten_min_bo,five_min_bo,processes,final_pchange_output_dict,final_breakout_dict,
            final_upper_lower_circuit_dict,jg_stock_quote,ranking_iter,ranking_dict):
    while True:
        # use this start_time for automating the server to run from 9:16:40
        start_time = datetime.now()
        #start_time = start_time.replace(hour=9, minute=16, second=0, microsecond=0)
        j += 1
        
        target_change_hour, target_change_minute, target_change_second = 9, 45, 0
        period_change_time_1 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        target_change_hour, target_change_minute, target_change_second = 11, 00, 0
        period_change_time_2 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        current_time = datetime.now()
        
        if current_time <= period_change_time_1:
            period_for_2m = 'before'
        else:
            period_for_2m = 'after'
        
        if current_time <= period_change_time_2:
            period_for_5m = 'before'
        else:
            period_for_5m = 'after'
        
        
        i=0
        y=0
        num_processor_cores = multiprocessing.cpu_count()
        chunk_size = len(eqList) // num_processor_cores
        
        curr_time = datetime.now()
        print ('\n\n\n\n\n\n\nSTARTING TO FETCH YFINANCE DATA AT = ',curr_time.strftime("%H:%M:%S"))
        
        SCHEDULE_INITIATOR(chunk_size,num_processor_cores,eqList,y,event,lock,processes,n,jg_stock_quote,
                    Stock,yfd_dict,period_for_2m,period_for_5m,trading_system_start_time)
        
        ct = datetime.now()
        print ('YFINANCE DATA FETCHING ENDED AT = ',ct.strftime("%H:%M:%S"))
        time_diff = ct - curr_time
        time_diff = time_diff.total_seconds()
        print(f'It took = {time_diff} seconds to fetch the YAHOO FINANCE data')
        print ('\n\n')

        '''
        i=0
        
        for i in range(num_processor_cores):            
            start = i * chunk_size
            end = start + chunk_size if i < num_processor_cores - 1 else len(eqList)
            
            data_processing_process = multiprocessing.Process(
                target=DATA_PROCESSOR,                         ##############  APPENDER.py file
                args=(start,end,yfd_dict,period_for_5m,two_min_RSI_avg, five_min_RSI_avg,
                total_traded_volume, pChange, lock, breakout, bopp,twenty_ma,up_and_low_circuit,orb,
                last_three_volume,eqList,event,jg_stock_quote,ten_min_bo,five_min_bo))
            processes.append(data_processing_process)
            data_processing_process.start()

        for process in processes:
            process.join()
        
        border_line = []
        for i in range(len(Stock)):
            border_line.append('|')


        def JUGAAD_DATA(n,l):
            l+=1
            try:
                nifty200 = n.live_index("NIFTY 200")
            except Exception as e:
                print ('\n\n\n\n\n\n',repr(e))
                print ('\n\n\n\n\n\nERROR = Couldnt reach the NSE server for the LIVE INDEX data,\nSo retrying again to fetch the data..........\n\n\n\n\n\n')
                if l < 5:
                    JUGAAD_DATA(n,l)
            return nifty200
        l=0
        nifty200 = JUGAAD_DATA(n,l)
        advances = int(nifty200['advance']['advances'])
        declines = int(nifty200['advance']['declines'])
        unchanged = int(nifty200['advance']['unchanged'])
        
        final_upper_lower_circuit_dict.update({'Stock': list(Stock)})
        final_upper_lower_circuit_dict.update({'Circuit level': list(up_and_low_circuit)})
        
        final_pchange_output_dict.update({'pChange': list(pChange)})
        #final_pchange_output_dict.update({'Avg RSI(14) 2m': list(two_min_RSI_avg)})
        # final_pchange_output_dict.update({'RSI(14) 5m': list(five_min_RSI_avg)})
        # If you want to print the above column, remove the commenting on RSI average calucator function in Appender.py file in Data_processor() function
        final_pchange_output_dict.update({'Stock': list(Stock)})
        final_pchange_output_dict.update({'BO price percentage': list(bopp)})
        final_pchange_output_dict.update({'Last 3 Volume changes': list(last_three_volume)})
        final_pchange_output_dict.update({'Volume 20 Moving Avg': list(twenty_ma)})
        final_pchange_output_dict.update({'Total Volume': list(total_traded_volume)})
        
        #final_breakout_dict.update({'Avg 2mRSI': list(two_min_RSI_avg)})
        final_breakout_dict.update({'pChange': list(pChange)})
        final_breakout_dict.update({'|': list(border_line)})
        # final_breakout_dict.update({'RSI(14) 5m': list(five_min_RSI_avg)})
                # If you want to print the above column, remove the commenting on
                # RSI average calucator function in Appender.py file in Data_processor() function
        #final_breakout_dict.update({'Total Volume': list(total_traded_volume)})
        #final_breakout_dict.update({'Volume 20 Moving Avg': list(twenty_ma)})
        #final_breakout_dict.update({'Last 3 Volume changes': list(last_three_volume)})
                # When you uncomment these above lines of volume columns, also uncomment
                # the ["Total Volume"] line in the DATAFRAME_GENERATOR() function
        final_breakout_dict.update({'BO Trend': list(breakout)})
        final_breakout_dict.update({'-': list(border_line)})
        final_breakout_dict.update({'Stock': list(Stock)})
        final_breakout_dict.update({'=': list(border_line)})
        final_breakout_dict.update({'ORB %': list(orb)})
        final_breakout_dict.update({'*': list(border_line)})
        final_breakout_dict.update({'BO price percentage': list(bopp)})
        final_breakout_dict.update({'+': list(border_line)})
        
        
        final_ORB_dict.update({'Stock': list(Stock)})
        final_ORB_dict.update({'|': list(border_line)})
        #final_ORB_dict.update({'Avg 2mRSI': list(two_min_RSI_avg)})
        final_ORB_dict.update({'-': list(border_line)})
        final_ORB_dict.update({'BO Trend': list(breakout)})
        final_ORB_dict.update({'=': list(border_line)})
        final_ORB_dict.update({'BO price percentage': list(bopp)})
        final_ORB_dict.update({'+': list(border_line)})
        final_ORB_dict.update({'ORB %': list(orb)})
        
        
        ten_min_bo_dict.update({'Stock': list(Stock)})
        ten_min_bo_dict.update({'10min BO': list(ten_min_bo)})
        
        
        five_min_bo_dict.update({'Stock': list(Stock)})
        five_min_bo_dict.update({'5min BO': list(five_min_bo)})
        
        
        
        df_generating_process = multiprocessing.Process(
                target=DATAFRAME_GENERATOR,             #############  PRINTER.py file
                args=(advances,declines,unchanged,j,final_pchange_output_dict,final_breakout_dict,final_upper_lower_circuit_dict,
                    jg_stock_quote,ranking_iter,ranking_dict,eqList,final_ORB_dict,ten_min_bo_dict,five_min_bo_dict))
        df_generating_process.start()
        df_generating_process.join()
        
        
        
        
        
        
        for i in range(len(eqList)):
            yf_all_stocks_data = yfd_dict['5m']
            yf_data = yf_all_stocks_data[(eqList[i])]
            
            strong_bullish_stocks = []
            bullish_pchg = []
            strong_bearish_stocks = []
            bearish_pchg = []
            
            if period_for_5m == 'before': 
                todays_data = yf_data[yf_data.index.date == pd.to_datetime('today').date()]  
                todays_open_data = list(todays_data['Open'])
                day_open = todays_open_data[-1]
            
            if period_for_5m == 'after': 
                todays_open_data = list(yf_data['Open'])
                day_open = todays_open_data[-1]
            
            jg_stock_data = jg_stock_quote[eqList[i].replace(".NS", "")]
            
            a = day_open/100 * 80
            
            if day_open >= jg_stock_data[3]:
                if a >=jg_stock_data[3]:
                    strong_bullish_stocks.append(eqList[i].replace(".NS", ""))
                    bullish_pchg.append(pChange[i])

            if day_open <= jg_stock_data[4]:
                if a >=jg_stock_data[3]:
                    strong_bearish_stocks.append(eqList[i].replace(".NS", ""))
                    bullish_pchg.append(pChange[i])
            
        print('\nTodays strong BULLISH stocks are :-')
        for i in range(len(strong_bullish_stocks)):
            print (f'{strong_bullish_stocks[i]} ({bullish_pchg[i]})')
        print('Todays strong BEARISH stocks are :-')
        for i in range(len(strong_bearish_stocks)):
            print (f'{strong_bearish_stocks[i]} ({bearish_pchg[i]})')
        
        
        
        
        
        Stock = manager.list()
        pChange = manager.list()
        total_traded_volume = manager.list()
        twenty_ma = manager.list()
        last_three_volume = manager.list()
        ten_min_bo = manager.list()
        five_min_bo = manager.list()
        two_min_RSI_avg = manager.list()
        five_min_RSI_avg = manager.list()
        
        breakout = manager.list()
        bopp = manager.list()
        yfd_dict = manager.dict()
        jg_stock_quote = manager.dict()
        up_and_low_circuit = manager.list()
        orb = manager.list()
        
        
        processes = []
        final_pchange_output_dict = {}
        final_breakout_dict = {}
        final_upper_lower_circuit_dict = {}
        final_ORB_dict = {}
        ten_min_bo_dict = {}
        five_min_bo_dict = {}

        current_time = datetime.now()
        # Calculate the time difference between now and the start time
        
        time_difference = current_time - start_time
        time_difference = time_difference.total_seconds()
        
        if 150 > time_difference:
            time_left = 150 - time_difference
            print (f'\nIt took {time_difference} seconds to run & complete the {ranking_iter.value - 1}th iteration of this program')
        else:
            time_left = 1
            print (f'\nIt took {time_difference} seconds to run & complete the {ranking_iter.value - 1}th iteration of this program\nAs it has crossed 2 minutes, so rerunning this program just after the next {time_left} seconds............')
        '''
        # print ('*'*150)
        # print ('*'*150)
        #time.sleep(time_left)       
        sys.exit(1)


























#   The Scheduler is only downlading using MainProcess only, check the download time using 1 and 4 processes in 
#   the for loop





























if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    print ('\n\nthe code has started to run.......')
    
    #   Disable the below line before enabling the live server just before the market time
    trading_system_start_time = datetime.now()
    
    if trading_system_start_time < datetime.now():
        print (f"Adangomma, the specified time {trading_system_start_time} has already passed daa....!!")
        print ("exiting the program !!")
        sys.exit(1)


    orb = manager.list()
    bopp = manager.list()
    Stock = manager.list()
    pChange = manager.list()
    breakout = manager.list()
    twenty_ma = manager.list()
    ten_min_bo = manager.list()
    five_min_bo = manager.list()
    two_min_RSI_avg = manager.list()
    five_min_RSI_avg = manager.list()
    last_three_volume = manager.list()
    up_and_low_circuit = manager.list()
    total_traded_volume = manager.list()
    
    yfd_dict = manager.dict()
    ranking_dict = manager.dict()
    jg_stock_quote = manager.dict()
    
    lock = manager.Lock()
    
    ranking_iter = manager.Value('i', 1)
    
    processes = []
    final_pchange_output_dict = {}
    final_breakout_dict = {}
    final_ORB_dict = {}
    final_upper_lower_circuit_dict = {}
    ten_min_bo_dict = {}
    five_min_bo_dict = {}

    j = 0
    
    THE_MAIN(j,Stock,pChange,total_traded_volume,last_three_volume,twenty_ma,up_and_low_circuit,orb,ten_min_bo_dict,five_min_bo_dict,
        two_min_RSI_avg,five_min_RSI_avg,breakout,bopp,yfd_dict,lock,final_ORB_dict,ten_min_bo,five_min_bo,
        processes,final_pchange_output_dict,final_breakout_dict,final_upper_lower_circuit_dict,jg_stock_quote,ranking_iter,ranking_dict)

