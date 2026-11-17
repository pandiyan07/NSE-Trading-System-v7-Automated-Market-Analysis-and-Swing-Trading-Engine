import time
import yfinance as yf
from datetime import datetime
import multiprocessing


current_process = multiprocessing.current_process()
process_name = current_process.name
event = multiprocessing.Event()


def JUGAAD_DATA(n,lock,jg_stock_quote,eq,Stock,l):
    
    def FETCHER(n,eq,l):
        l+=1
        try:
            jg_data = n.stock_quote(eq.replace(".NS", ""))
            return jg_data
        except Exception as e:
            
            print ('\n\n\n\n\n\n',repr(e))
            print ('\n\n\n\n\n\nERROR = Couldnt reach the NSE server for the STOCK QUOTE,\nSo retrying again to fetch the data..........\n\n\n\n\n\n')
            if l < 5:
                FETCHER(n,eq,l)
    
    jg_data = FETCHER(n,eq,l)
    jg_required_data = []
    
    try:
        with lock:
            Stock.append(jg_data['info']['symbol'])
            jg_required_data.append(jg_data['priceInfo']['lowerCP'])
            jg_required_data.append(jg_data['priceInfo']['upperCP'])
            jg_required_data.append(jg_data['priceInfo']['lastPrice'])
            jg_required_data.append(jg_data['priceInfo']['intraDayHighLow']['min'])
            jg_required_data.append(jg_data['priceInfo']['intraDayHighLow']['max'])
            jg_stock_quote.update({jg_data['info']['symbol']:jg_required_data})
    except Exception as e:
        print ('\n\n',repr(e))
        print (f' ERROR = The Stock {eq.replace(".NS", "")} data is not available.....!!')
        print ('So appending all the fetched values as 0')
        print ('\n\n')
        with lock:
            Stock.append(eq.replace(".NS", ""))
            jg_required_data.append(0)
            jg_required_data.append(0)
            jg_required_data.append(0)
            jg_required_data.append(0)
            jg_required_data.append(0)
            jg_stock_quote.update({eq.replace(".NS", ""):jg_required_data})


def DATA_FETCHER(per,inte,event,eqList):
    yf_all_stocks_data = yf.download(eqList, group_by='Ticker', period=per, interval=inte)
    event.set() #1
    return yf_all_stocks_data


def SCHEDULE_TASK(y,yfd_dict,lock,period_for_2m,period_for_5m,
                trading_system_start_time,event,eqList,n,
                jg_stock_quote,Stock,start,end,process_name):
    
    if period_for_2m == 'before':
        period_interval_2m = {
            1 : ["2d",'2m'],
        }
    
    if period_for_2m == 'after':
        period_interval_2m = {
            1 : ["1d",'2m'],
        }
    
    if period_for_5m == 'before':
        period_interval_5m = {
            2 : ["2d",'5m'],
        }
    
    if period_for_5m == 'after':
        period_interval_5m = {
            2 : ["1d",'5m'],
        }
    print(f'{process_name} = {start} and {end}')

    while True:
        #   Enable the below line every morning before the market starts
        #current_time = datetime.now()
        current_time = trading_system_start_time
        if current_time >= trading_system_start_time:
            #   JUGAAD FETCHING
            for i in range(start, end):
                print (eqList[i],process_name)
                l = 0
                print('=')
                JUGAAD_DATA(n,lock,jg_stock_quote,eqList[i],Stock,l)
            
            #   YF DATA FETCHING
            minor_eqList = []
            for eq in eqList[start:end]:
                minor_eqList.append(eq)
            
            print ('minor_eqList = ',minor_eqList)
            print ('y = ',y)
            if y == 1:
                pi_2m = period_interval_2m[y]
                yf_all_stocks_data = DATA_FETCHER(pi_2m[0],pi_2m[1],event,minor_eqList) 
                with lock:
                    yfd_dict.update({pi_2m[1]:yf_all_stocks_data})
                '''
            if y == 2:
                pi_5m = period_interval_5m[y]
                yf_all_stocks_data = DATA_FETCHER(pi_5m[0],pi_5m[1],event,minor_eqList)
                with lock:
                    yfd_dict.update({pi_5m[1]:yf_all_stocks_data})
            
            if y == 3:
                yf_all_stocks_data = DATA_FETCHER('1d','1d',event,eqList)
                with lock:
                    yfd_dict.update({'1d':yf_all_stocks_data})
            '''
            event.wait()    #1
            break
        print(current_time,' =======>>> ',trading_system_start_time)
        time.sleep(5)


def SCHEDULE_INITIATOR(chunk_size,num_processor_cores,eqList,y,event,lock,processes,n,jg_stock_quote,
                    Stock,yfd_dict,period_for_2m,period_for_5m,trading_system_start_time):
    print ('num_processor_cores = ',num_processor_cores)
    for i in range(num_processor_cores):
        start = i * chunk_size
        end = start + chunk_size if i < num_processor_cores - 1 else len(eqList)
        y+=1
        
        data_fetching_process = multiprocessing.Process(
            target=SCHEDULE_TASK,                        ############## SCHEDULER.py file
            args=(y,yfd_dict,lock,period_for_2m,period_for_5m,trading_system_start_time,
                event,eqList,n,jg_stock_quote,Stock,start,end,process_name))
        processes.append(data_fetching_process)
        data_fetching_process.start()
            
    for process in processes:
        process.join()
    

if __name__ == "__main__":
    print ('\n\n\nTrading_system_v6.py has the MAIN() function file. So Execute that file.....!!!\n\n\n')