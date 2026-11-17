import pandas as pd
from datetime import datetime
import warnings
from pandas.errors import SettingWithCopyWarning

holidays = {
'Bakri Eid' : '17-6-2024',
'Moharram' : '17-7-2024',	
'Independence Day/ Parsi New Year' : '15-8-2024',
'Eid-e-Milad' : '16-9-2024',
'Mahatma Gandhi Jayanti' : '02-10-2024',
'Diwali-Laxmi Pujan' : '01-11-2024',
'Guru Nanak Jayanti' : '15-11-2024',
'Christmas' : '25-12-2024'
}

# Function to check if today is a holiday and if not, find the next two upcoming holidays
def CHECK_HOLIDAY(holidays):
    
    today = datetime.today().date()

    
    holidays_dates = [(name, datetime.strptime(date, '%d-%m-%Y').date()) for name, date in holidays.items()]

    # Check if today is a holiday
    for name, holiday_date in holidays_dates:
        if today == holiday_date:
            print(f"Today is {name}.")
            return

    # If today is not a holiday, sort the holidays by date
    holidays_dates.sort(key=lambda x: x[1])

    # Find the next two upcoming holidays
    upcoming_holidays = [holiday for holiday in holidays_dates if holiday[1] > today]

    if len(upcoming_holidays) >= 2:
        next_two_holidays = upcoming_holidays[:2]
        print("\nToday the Stock market is OPEN, its NOT a GOVERNMENT HOLIDAY.")
        print("The next two upcoming GOVERNMENT HOLIDAYS are :-")
        for holiday in next_two_holidays:
            print(f"{holiday[0]} on {holiday[1].strftime('%d-%m-%Y')}")
    else:
        print("WARNING :- There are less than two upcoming holidays left.")
        print(f"{holiday[0]} on {holiday[1].strftime('%d-%m-%Y')}")


def COMMON_STOCKS(sorted_FO_BO_df,sorted_FO_pchg_df):
    sorted_BO_eqList = sorted_FO_BO_df['Stock'].tolist()
    sorted_pchg_eqList = sorted_FO_pchg_df['Stock'].tolist()
    commn_eq = []
    for eq in sorted_BO_eqList:
        for st in sorted_pchg_eqList:
            if eq == st:
                commn_eq.append(eq)
    
    common_df = sorted_FO_BO_df[sorted_FO_BO_df["Stock"].isin(commn_eq)]
    
    if len(common_df) != 0:
        print (common_df)
    else:
        print ('NO STOCKS ARE COMMON AMONG BOTH THE TABLES\n')


def CONSISTENCY_RANKING(fo_bo_sorted_df,ranking_iter,ranking_dict,eqList):
    stocks = list(fo_bo_sorted_df['Stock'])
    
    if ranking_iter.value == 1:
        for eq in eqList:
            ranking_dict.update({eq.replace(".NS", ""):[0,0]})
    
    if ranking_iter.value > 0:
        st_rank = 10
        for s in stocks:
            b = ranking_dict[s]
            if st_rank > 0:
                b[0] += st_rank
                b[1] += 1
                ranking_dict[s] = b
            else:
                b[1] += 1
                ranking_dict[s] = b
            st_rank -= 1

    ranking_iter.value += 1
    ranking_list = []
    for s in stocks:
        for dict_key,dict_value in ranking_dict.items():
            if s == dict_key:
                a = f'{dict_value[0]} ({dict_value[1]})'
                ranking_list.append(a)
    
    return ranking_list
    


def OUTPUT_PRINTER(j,advances,declines,unchanged,pos_sorted_final_output_pchange_dataframe,sorted_five_min_bo_df,
                neg_sorted_final_output_pchange_dataframe,sorted_breakout_dataframe,final_upper_lower_circuit_dataframe,
                jg_stock_quote,ranking_iter,ranking_dict,eqList,sorted_ORB_dataframe,sorted_ten_min_bo_df):
    print ('Iteration number - ',ranking_iter.value)
    
    CHECK_HOLIDAY(holidays)
    
    output_printing_time = datetime.now()
    print ('\nOUTPUT FOR THE TIME = ',output_printing_time.strftime("%H:%M:%S"))
    
    
    print(f"\nNIFTY 200 current status -\nAdvances :- {advances}\nDeclines :- {declines}\nUnchanged :- {unchanged}\n")
    
    
    '''    UPPER CIRCUIT & LOWER CIRCUIT STOCKS FINDER      '''
    print ("\nThe STOCKS CLOSE TO THEIR UPPER & LOWER CIRCUIT are :-\n")
    print (final_upper_lower_circuit_dataframe)

    
    '''    HIGHEST AND LOWEST PCHANGE STOCKS      '''
    print ("\nHIGHEST pCHANGE value STOCKS :-\n")
    print (pos_sorted_final_output_pchange_dataframe)
    print ("\nLOWEST pCHANGE value STOCKS :-\n")
    print (neg_sorted_final_output_pchange_dataframe)
    
    '''    ORB DATAFRAME      '''
    print ("\nThe top sorted ORB STOCKS are :-\n")
    print(sorted_ORB_dataframe)
    
    '''    BREAKOUT STOCKS      '''
    warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)       #Supresses the SettingWithCopyWarning
    if sorted_breakout_dataframe.empty:
        print ('\nCURRENTLY THERE ARE NO BREAKOUT STOCKS\n\n\n')
    else:
        return_ranking_list = CONSISTENCY_RANKING(sorted_breakout_dataframe,ranking_iter,ranking_dict,eqList)
        sorted_breakout_dataframe['Rank score'] = return_ranking_list
        print ('='*70)
        print ("\nThe top sorted BREAKOUT STOCKS are :-\n")
        print (sorted_breakout_dataframe)
        print ('='*83)
    
    '''    10min BO      '''
    print ("\nThe top sorted 10min BREAKOUT STOCKS are :-\n")
    print ('10min BO ')
    print (sorted_ten_min_bo_df)
    print ('='*45)
    
    '''    5min BO      '''
    print ("\nThe top sorted 5min BREAKOUT STOCKS are :-\n")
    print ('5min BO ')
    print (sorted_five_min_bo_df)
    print ('='*45)
    
    

    '''    COMMON STOCKS      ''' 
    print ('\n\n===> THE COMMON STOCKS IN BOTH THE pCHANGE & 15min BO TABLES ARE = ')
    COMMON_STOCKS(sorted_breakout_dataframe.iloc[:20],pos_sorted_final_output_pchange_dataframe.iloc[:20])
    print ('\n===> THE COMMON STOCKS IN BOTH THE pCHANGE & 10min BO TABLES ARE = ')
    COMMON_STOCKS(sorted_ten_min_bo_df.iloc[:20],pos_sorted_final_output_pchange_dataframe.iloc[:20])
    print ('\n===> THE COMMON STOCKS IN BOTH THE pCHANGE & 5min BO TABLES ARE = ')
    COMMON_STOCKS(sorted_five_min_bo_df.iloc[:20],pos_sorted_final_output_pchange_dataframe.iloc[:20])


def DATAFRAME_GENERATOR(advances,declines,unchanged,j,final_pchange_output_dict,final_breakout_dict,final_upper_lower_circuit_dict,
                        jg_stock_quote,ranking_iter,ranking_dict,eqList,final_ORB_dict,ten_min_bo_dict,five_min_bo_dict):
    
    try:
        final_output_pchange_dataframe = pd.DataFrame(final_pchange_output_dict)
        final_output_breakout_dataframe = pd.DataFrame(final_breakout_dict)
        final_upper_lower_circuit_dataframe = pd.DataFrame(final_upper_lower_circuit_dict)
        final_ORB_dataframe = pd.DataFrame(final_ORB_dict)
    except Exception as e:
        print ('\n\n\n',repr(e),'\n\n\n')
    
    '''    UPPER AND LOWER CIRCUIT PERCENTAGE     '''
    final_upper_lower_circuit_dataframe = final_upper_lower_circuit_dataframe.sort_values(by='Circuit level', ascending=True)
    final_upper_lower_circuit_dataframe = final_upper_lower_circuit_dataframe.iloc[:3]
    final_upper_lower_circuit_dataframe['Circuit level'] = [f"{cl} %" for cl in final_upper_lower_circuit_dataframe['Circuit level']]
    
    '''    POSITIVE pCHANGE     '''
    pos_sorted_final_output_pchange_dataframe = final_output_pchange_dataframe.sort_values(by='pChange', ascending=False)
    pos_sorted_final_output_pchange_dataframe = pos_sorted_final_output_pchange_dataframe[(pos_sorted_final_output_pchange_dataframe["Total Volume"] >= 200000)]
    pos_sorted_final_output_pchange_dataframe = pos_sorted_final_output_pchange_dataframe.iloc[:5]
    pos_sorted_final_output_pchange_dataframe['Total Volume'] = [f"{vol:,}" for vol in pos_sorted_final_output_pchange_dataframe['Total Volume']]
    pos_sorted_final_output_pchange_dataframe['pChange'] = [f"{pchg} %" for pchg in pos_sorted_final_output_pchange_dataframe['pChange']]
    pos_sorted_final_output_pchange_dataframe = pos_sorted_final_output_pchange_dataframe.reset_index(drop=True)
    pos_sorted_final_output_pchange_dataframe = pos_sorted_final_output_pchange_dataframe.set_index('pChange')
    
    '''    NEGATIVE pCHANGE     '''
    neg_sorted_final_output_pchange_dataframe = final_output_pchange_dataframe.sort_values(by='pChange', ascending=True)
    neg_sorted_final_output_pchange_dataframe = neg_sorted_final_output_pchange_dataframe[(neg_sorted_final_output_pchange_dataframe["Total Volume"] >= 200000)]
    neg_sorted_final_output_pchange_dataframe = neg_sorted_final_output_pchange_dataframe.iloc[:5]
    neg_sorted_final_output_pchange_dataframe['Total Volume'] = [f"{vol:,}" for vol in neg_sorted_final_output_pchange_dataframe['Total Volume']]
    neg_sorted_final_output_pchange_dataframe['pChange'] = [f"{pchg} %" for pchg in neg_sorted_final_output_pchange_dataframe['pChange']]
    neg_sorted_final_output_pchange_dataframe = neg_sorted_final_output_pchange_dataframe.reset_index(drop=True)
    neg_sorted_final_output_pchange_dataframe = neg_sorted_final_output_pchange_dataframe.set_index('pChange')
    
    '''    BREAKOUT    '''
    trending_final_output_breakout_dataframe = final_output_breakout_dataframe[(final_output_breakout_dataframe["BO Trend"] == '+') | (final_output_breakout_dataframe["BO Trend"] == 'BEARISH')]
    sorted_breakout_dataframe = trending_final_output_breakout_dataframe.sort_values(by='BO price percentage', ascending=False)
    #sorted_breakout_dataframe = sorted_breakout_dataframe[(sorted_breakout_dataframe["Total Volume"] >= 200000)]
    sorted_breakout_dataframe = sorted_breakout_dataframe.iloc[:10]
    #sorted_breakout_dataframe['Total Volume'] = [f"{vol:,}" for vol in sorted_breakout_dataframe['Total Volume']]
    sorted_breakout_dataframe['BO price percentage'] = [f"{perc}% BO" for perc in sorted_breakout_dataframe['BO price percentage']]
    sorted_breakout_dataframe['ORB %'] = [f"{perc} %" for perc in sorted_breakout_dataframe['ORB %']]
    sorted_breakout_dataframe = sorted_breakout_dataframe.reset_index(drop=True)
    sorted_breakout_dataframe = sorted_breakout_dataframe.set_index('pChange')
    
    '''    ORB    '''
    sorted_ORB_dataframe = final_ORB_dataframe.sort_values(by='ORB %', ascending=True)
    sorted_ORB_dataframe = sorted_ORB_dataframe.iloc[:10]
    sorted_ORB_dataframe['ORB %'] = [f"{perc} %" for perc in sorted_ORB_dataframe['ORB %']]
    sorted_ORB_dataframe['BO price percentage'] = [f"{perc}% BO" for perc in sorted_ORB_dataframe['BO price percentage']]
    sorted_ORB_dataframe = sorted_ORB_dataframe.reset_index(drop=True)
    sorted_ORB_dataframe = sorted_ORB_dataframe.set_index('Stock')
    
    '''    10min BO      '''
    ten_min_bo_df = pd.DataFrame(ten_min_bo_dict)
    sorted_ten_min_bo_df = ten_min_bo_df.sort_values(by='10min BO', ascending=False)
    sorted_ten_min_bo_df = sorted_ten_min_bo_df.iloc[:5]
    sorted_ten_min_bo_df['10min BO'] = [f"{perc}%" for perc in sorted_ten_min_bo_df['10min BO']]
    
    '''    5min BO      '''
    five_min_bo_df = pd.DataFrame(five_min_bo_dict)
    sorted_five_min_bo_df = five_min_bo_df.sort_values(by='5min BO', ascending=False)
    sorted_five_min_bo_df = sorted_five_min_bo_df.iloc[:5]
    sorted_five_min_bo_df['5min BO'] = [f"{perc}%" for perc in sorted_five_min_bo_df['5min BO']]
    
    '''    PRINTING THE FINAL OUTPUT    '''
    
    OUTPUT_PRINTER(j,advances,declines,unchanged,pos_sorted_final_output_pchange_dataframe,sorted_five_min_bo_df,
                neg_sorted_final_output_pchange_dataframe,sorted_breakout_dataframe,final_upper_lower_circuit_dataframe,
                jg_stock_quote,ranking_iter,ranking_dict,eqList,sorted_ORB_dataframe,sorted_ten_min_bo_df)



if __name__ == "__main__":
    print ('\n\n\nTrading_system_v6.py has the MAIN() function file. So Execute that file.....!!!\n\n\n')