import pandas as pd
import sys



def RSI_14_AVERAGE_CALCULATOR(yf_cp_list,event):
    i=1
    rsi_avg = []
    avg_iteration = len(yf_cp_list) - 13
    
    for i in range(0,avg_iteration):
        if len(yf_cp_list) >= 15:  
            price_diffs = [yf_cp_list[i] - yf_cp_list[i - 1] for i in range(i, i+14)]
            #  price_diffs = [yf_cp_list[i] - yf_cp_list[i - 1] for i in range(1, len(yf_cp_list))]
        else:
            print ("WARNING :- NUMBER OF PRICES ARE LESS THAN 14 DATA POINTS...!!\n")
            print ('The length of close price list is = \n',len(yf_cp_list))
            print ('\n\n\n\n\n\n So thats why exiting the program................. \n\n\n\n\n\n')
            sys.exit(1)
        gains = []
        losses = []
        for diff in price_diffs:
            if diff > 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(-diff)
        avg_gain = sum(gains) / 14
        avg_loss = sum(losses) / 14
        
        if avg_loss != 0:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            rsi = rsi
        else:
            rsi = 100
        
        
        rsi_avg.append(rsi)

    event.set() #3
    average = sum(rsi_avg)/avg_iteration
    return round(average,1)


def ONE_CANDLE_PRICE_BREAKOUT(zero_candle_cp,zero_candle_op,event):
    
    if zero_candle_cp > zero_candle_op:
        percentage = ((zero_candle_cp-zero_candle_op)/zero_candle_cp)*100
    else:
        percentage = ((zero_candle_op-zero_candle_cp)/zero_candle_op)*100
    event.set()    #11
    return percentage


def TWO_CANDLE_PRICE_BREAKOUT(zero_candle_cp,last_candle_cp,zero_candle_op,last_candle_op,event):
    percentage = 0
    
    '''    BULLISH BREAKOUT     '''
    if zero_candle_cp > last_candle_cp:
        if last_candle_op < zero_candle_op: 
            percentage = 100 - ((last_candle_op/zero_candle_cp)*100)
    
    '''    BEARISH BREAKOUT     '''
    if zero_candle_cp < last_candle_cp:
        if last_candle_op > zero_candle_op:                               
            percentage = 100 - ((zero_candle_cp/last_candle_op)*100)
    
    event.set()    #11
    return percentage


def THREE_CANDLE_PRICE_BREAKOUT(yf_all_stocks_data,i,event,eqList):
    BO_status = 'nil'
    percentage_3c = 0
    yf_cp_list = yf_all_stocks_data[(eqList[i], 'Close')].tolist() 
    yf_op_list = yf_all_stocks_data[(eqList[i], 'Open')].tolist()
    zero_candle_cp = yf_cp_list[2] 
    last_candle_cp = yf_cp_list[1] 
    second_last_candle_cp = yf_cp_list[0] 
    
    zero_candle_op = yf_op_list[2]
    last_candle_op = yf_op_list[1]
    second_last_candle_op = yf_op_list[0]
    
    percentage_2c = TWO_CANDLE_PRICE_BREAKOUT(zero_candle_cp,last_candle_cp,zero_candle_op,last_candle_op,event)
    event.wait()    #11
        
    percentage_1c = ONE_CANDLE_PRICE_BREAKOUT(zero_candle_cp,zero_candle_op,event)
    event.wait()    #12
    
    '''    BULLISH BREAKOUT     '''
    if zero_candle_cp > last_candle_cp > second_last_candle_cp:   
        if second_last_candle_op < last_candle_op < zero_candle_op:                              
            percentage_3c = 100 - ((second_last_candle_op/zero_candle_cp)*100)
            BO_status = '+'

    '''    BEARISH BREAKOUT     '''
    if zero_candle_cp < last_candle_cp < second_last_candle_cp:   
        if second_last_candle_op > last_candle_op > zero_candle_op:                               
            percentage_3c = 100 - ((zero_candle_cp/second_last_candle_op)*100)
            BO_status = 'BEARISH'

    event.set()    #5
    return BO_status,round(percentage_3c,1),round(percentage_2c,1),round(percentage_1c,1)

def TWENTY_MA_CALCULATOR(volume_list,curr_vol):
    volume_list = volume_list[-20:]
    ma = sum(volume_list)/20
    
    if curr_vol > 0:
        if curr_vol < ma:
            percentage_difference = ((curr_vol-ma)/ma)*100
            return f'{round(percentage_difference,1)}% less than 20MA'
        else:
            percentage_difference = ((curr_vol-ma)/curr_vol)*100
            return f'{round(percentage_difference,1)}% MORE than 20MA'
    else:
        return f'{curr_vol} (NO VOLUME AVAILABLE CURRENTLY)'
    
    
def THREE_CANDLE_VOLUME_BREAKOUT(yfd_dict,i,event,period_for_5m,BO_status,eqList):
    yf_all_stocks_data = yfd_dict['5m']
    yf_data = yf_all_stocks_data[(eqList[i])]
    
    '''
    This below block of code will find the total volume of this particular stock
    '''
    
    if period_for_5m == 'before': 
        todays_data = yf_data[yf_data.index.date == pd.to_datetime('today').date()]  
        todays_data = list(todays_data['Volume'])
        ttv = sum(todays_data)
        
    if period_for_5m == 'after': 
        todays_data = list(yf_data['Volume'])
        ttv = sum(todays_data)
    
    tma = TWENTY_MA_CALCULATOR(todays_data,todays_data[-1])
    
    yf_all_stocks_data = yfd_dict['5m'].iloc[-4:]
    yf_vol_list = yf_all_stocks_data[(eqList[i], 'Volume')].tolist()
    a = 3
    b = ['fvd','svd','tvd']
    volume_change = {}
    
    '''
    This below block of code will find the DIFFERENCE IN VOLUME only when
    the last 3 CLOSING PRICES of that same stock is in a BULLISH or BEARISH trend
    '''
    
    if BO_status in ('+','BEARISH'):
        for v in range(0,3):
            curr_vol = yf_vol_list[a]
            prev_vol = yf_vol_list[a-1] 
            if curr_vol == 0:
                curr_vol = 1
            perc = ((curr_vol-prev_vol)/curr_vol)*100
            volume_change.update({b[v]:round(perc,1)})
            a-=1
    
    event.set()    #7
    return volume_change,ttv,tma

def pCHANGE_CALCULATOR(yf_all_stocks_data,eqList,i,event):
    # This function calculates the pchange of a given stock from today's opening price
    # to avoid the gapup/gapdown price differences
    yf_data = yf_all_stocks_data[(eqList[i])]
    todays_data = yf_data[yf_data.index.date == pd.to_datetime('today').date()]
    #todays_data = yf_data[yf_data.index.date == pd.to_datetime('2024-06-07').date()]
    
    today_open = todays_data["Open"].tolist()
    today_open = today_open[0]
    today_close = todays_data["Close"].tolist()
    today_close = today_close[-1]
    

    if today_open < today_close:
        percentage_change = ((today_close - today_open) / today_close) * 100
    else:
        percentage_change = ((today_close - today_open) / today_open) * 100
    
    event.set()    #8
    return round(percentage_change,1)


def UPPER_AND_LOWER_CIRCUIT(jsd,event):
    lcp = float(jsd[0])
    ucp = float(jsd[1])
    curr_price = float(jsd[2])
    if curr_price > 0:
        uc_cp_diff = ucp - curr_price
        lc_cp_diff = curr_price - lcp
        if uc_cp_diff < lc_cp_diff:
            percentage_diff = ((ucp - curr_price)/ucp) * 100
        else:
            percentage_diff = ((curr_price - lcp)/curr_price) * 100
    else:
        percentage_diff = 100
    
    event.set()    #9
    return round(percentage_diff,1)


def ORB(jsd,event):
    curr_price = float(jsd[2])
    idLow = float(jsd[3])
    idHigh = float(jsd[4])
    if curr_price > 0:
        a = curr_price - idLow 
        b = idHigh - idLow
        c = ((b-a)/b)*100
        if c > 50:
            orb = round(100 - c,1)     #f'{100 - c:.1f}'  # BULLISH ORB
        else:
            orb = round(c,1)     #f'{c:.1f}'      # BEARISH ORB
    else:
        orb = 100
    
    event.set()    #10
    return orb


def DATA_PROCESSOR(start, end, yfd_dict, period_for_5m,two_min_RSI_avg, five_min_RSI_avg,
    total_traded_volume, pChange, lock, breakout, bopp,twenty_ma,up_and_low_circuit,orb,
    last_three_volume,eqList,event,jg_stock_quote,ten_min_bo,five_min_bo):
    for i in range(start, end):
        
        '''    AVERAGE RSI(14) COLUMN   '''
        '''
        for key,value in yfd_dict.items():
            yf_cp_list = value[(eqList[i], 'Close')].tolist()
            rsi = RSI_14_AVERAGE_CALCULATOR(yf_cp_list,event)
            event.wait()    #3
            with lock:
                if key == '2m':
                    two_min_RSI_avg.append(rsi)
                ################# release this column of the comment once you include the 5min data average RSI caluclation column
                if key == '5m':
                    five_min_RSI_avg.append(rsi)
        '''    
        
        
        '''    PRICE BREAKOUT COLUMN    '''
        yf_all_stocks_data = yfd_dict['5m'].iloc[-3:]
        BO_status,percentage_3c,percentage_2c,percentage_1c = THREE_CANDLE_PRICE_BREAKOUT(yf_all_stocks_data,i,event,eqList)
        event.wait()    #5
        
        jugaad_stock_data = jg_stock_quote[eqList[i].replace(".NS", "")]
        
        '''    UPPER AND LOWER CIRCUIT PERCENTAGE    '''
        circuit_perc = UPPER_AND_LOWER_CIRCUIT(jugaad_stock_data,event)
        event.wait()    #9
        
        '''    ORB    '''
        orb_perc = ORB(jugaad_stock_data,event)
        event.wait()    #10
        
        '''    VOLUME COLUMN    '''
        volume_change,ttv,tma = THREE_CANDLE_VOLUME_BREAKOUT(yfd_dict,i,event,period_for_5m,BO_status,eqList)
        event.wait()    #7
        if BO_status in ('+', 'BEARISH'):
            v = f'{volume_change['tvd']}% -> {volume_change['svd']}% -> {volume_change['fvd']}%'
        else:
            v = 0
        
        '''    pCHANGE CALCULATOR    '''
        pChg = pCHANGE_CALCULATOR(yfd_dict['5m'],eqList,i,event)
        event.wait()    #8
    
        with lock:
            pChange.append(pChg)
            breakout.append(BO_status)
            bopp.append(percentage_3c)
            ten_min_bo.append(percentage_2c)
            five_min_bo.append(percentage_1c)
            total_traded_volume.append(ttv)
            twenty_ma.append(tma)
            up_and_low_circuit.append(circuit_perc)
            orb.append(orb_perc)
            last_three_volume.append(v)


if __name__ == "__main__":
    print ('\n\n\nTrading_system_v6.py has the MAIN() function file. So Execute that file.....!!!\n\n\n')