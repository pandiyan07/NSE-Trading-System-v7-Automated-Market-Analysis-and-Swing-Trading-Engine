
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
    print ('\n\n',repr(e))
    print ('There is NO INTERNET CONNECTION...!!')
    sys.exit(1)


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
        print ('\n\nSTARTING TO FETCH YFINANCE DATA AT = ',curr_time.strftime("%H:%M:%S"))
        
        SCHEDULE_INITIATOR(chunk_size,num_processor_cores,eqList,y,event,lock,processes,n,jg_stock_quote,Stock,yfd_dict,period_for_2m,period_for_5m,trading_system_start_time)
        
        ct = datetime.now()
        print ('YFINANCE DATA FETCHING ENDED AT = ',ct.strftime("%H:%M:%S"))
        time_diff = ct - curr_time
        time_diff = time_diff.total_seconds()
        print(f'It took = {time_diff} seconds to fetch the YAHOO FINANCE data')
        print ('\n\n')

        
        # print ('*'*150)
        # print ('*'*150)
        #time.sleep(time_left)       
        sys.exit(1)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    print ('\n\nthe code has started to run.......')
    
    #   Disable the below line before enabling the live server just before the market time
    trading_system_start_time = datetime.now()
    
    if trading_system_start_time < datetime.now():
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

