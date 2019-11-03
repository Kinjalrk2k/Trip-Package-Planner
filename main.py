import webbrowser
from os import system
import sys
import pandas as pd
import numpy as np
import msvcrt
from datetime import date
import math

sys.path.append('myimport') #   adding a new import path
import cli_menu, cli_blocks, cli_table

def read_data():
    ''' This function reads the data stored in the csv file into a dataframe
        Also, cleans the data from nan and zero values
        and returns the dataframe   '''

    df = pd.read_csv("data\\goibibo_com-travel_sample.csv")
    df = df.replace(np.nan, '', regex=True)
    df= df[df['hotel_star_rating'] != 0] 
    return df



def hotel_listing_cityStar(df, query_city, star_min, star_max):
    ''' This function returns a dataframe and list of hotel details
        according to the passed city name and star preferences  '''

    city_fil = df['city'] == query_city #   city filter
    star_min_fil = df['hotel_star_rating'] >= star_min  #   minimum star filter
    star_max_fil = df['hotel_star_rating'] <= star_max  # maximum star filter
    city_df = df[city_fil & (star_min_fil & star_max_fil)]  # apply all filters
    hotel_df = city_df

    #   typecasting
    city_df[['db_id', 'hotel_star_rating', 'price']] = city_df[['db_id', 'hotel_star_rating', 'price']].astype(str)
    hotel_list = list(zip(city_df['db_id'], city_df['property_name'], city_df['area'], city_df['hotel_star_rating'], city_df['price']))

    return hotel_df, hotel_list



def browser_map(lat, longi):
    ''' This function opens the default browser with a google map link
        showing the map of the passed latitude and longitude values '''

    map_url = 'https://www.google.com/maps/search/?api=1&query=' + str(lat) + ',' + str(longi)
    webbrowser.open(map_url)



def costing(hotel_sel):
    ''' This function returns flight, train and hotel costings
        by reading the data from the respective datasets    '''

    desti = hotel_sel.iloc[0]['city']   #   get destination city from the selected hotel
    
    f = open('data\\home.txt', 'r')
    source = f.readline()   #   get source city fro home location

    fldf = pd.read_csv("data\\flights.csv") #   read flight prices csv
    fldf.set_index("Unnamed: 0", inplace = True)
    fl_cost = int(fldf.at[source, desti])   #   find flight price

    trdf = pd.read_csv("data\\trains.csv")  #   read train prices csv
    trdf.set_index("Unnamed: 0", inplace = True)
    tr_cost = int(trdf.at[source, desti])   #   find train price

    hot_cost = int(hotel_sel.iloc[0]['price'])

    return hot_cost, fl_cost, tr_cost


def enter_date():
    ''' This function prompts to enter a date and returns the
        dd, mm and yyyy seperately  '''
    d1 = msvcrt.getche()
    d2 = msvcrt.getche()
    msvcrt.putwch('-')

    m1 = msvcrt.getche()
    m2 = msvcrt.getche()
    msvcrt.putwch('-')

    y1 = msvcrt.getche()
    y2 = msvcrt.getche()
    y3 = msvcrt.getche()
    y4 = msvcrt.getche()

    dd = int(d1 + d2)
    mm = int(m1 + m2)
    yyyy = int(y1 + y2 + y3 + y4)

    return dd, mm, yyyy
    


def day_diff(s_dd, s_mm, s_yyyy, e_dd, e_mm, e_yyyy):
    ''' This function calculates the difference between passed dates 
        and return the no. of days  '''
    s_date = date(s_yyyy, s_mm, s_dd)
    e_date = date(e_yyyy, e_mm, e_dd)
    diff = e_date - s_date
    return diff.days



def print_hotel_details(hotel_sel, s_date, e_date, days, ppl):
    ''' This functions prints all the hotel details  '''

    f = open('data\\home.txt', 'r')
    source = f.readline()
    f.close()
    print('HOME:', source)
    print()

    print('TRIP DETAILS:')
    print('Starts on:', s_date)
    print('Ends on:', e_date)
    print('Days:', days)
    print()

    print('HOTEL DETAILS:')
    print('Name:', hotel_sel.iloc[0]['property_name'])
    print('Type:', hotel_sel.iloc[0]['property_type'])
    print()

    print('LOCATION DETAILS: ')
    print('Adress:', hotel_sel.iloc[0]['address'])
    print('Locality:', hotel_sel.iloc[0]['locality'])
    print('Area:', hotel_sel.iloc[0]['area'])
    print('Province:', hotel_sel.iloc[0]['province'])
    print('City:', hotel_sel.iloc[0]['city'])
    print('State:', hotel_sel.iloc[0]['state'])
    print()

    print('ABOUT HOTEL:')
    print('Description:', hotel_sel.iloc[0]['hotel_description'])
    print('Star Rating:', hotel_sel.iloc[0]['hotel_star_rating'])
    print()

    fac_list = hotel_sel.iloc[0]['hotel_facilities'].split('|')
    fac_list += hotel_sel.iloc[0]['additional_info'].split('|')
    print('FACILITIES:')
    cli_blocks.print_in_blocks(fac_list, 4)
    print()

    poi_list = hotel_sel.iloc[0]['point_of_interest'].split('|')
    print('POINTS OF INTEREST:')
    cli_blocks.print_in_blocks(poi_list, 5)
    print()

    hot_cost, fl_cost, tr_cost = costing(hotel_sel)
    fl_cost *= ppl
    fl_cost *= 2
    tr_cost *= ppl
    tr_cost *= 2
    tot_hot_cost = hot_cost * days * math.ceil(ppl/2)
    misc_cost = hotel_sel.iloc[0]['misc_cost'] * days * ppl

    print('COSTING:')
    cost_tab = [['Hotel Price(per night)', 'Net Hotel Price', 'Travel by', 'Travel Cost', 'Miscellaneous', 'Total']]
    cost_tab.append([str(hot_cost), str(tot_hot_cost), 'Train', str(tr_cost), str(misc_cost), str(tot_hot_cost + tr_cost + misc_cost)])
    cost_tab.append([str(hot_cost), str(tot_hot_cost), 'Flight', str(fl_cost), str(misc_cost), str(tot_hot_cost + fl_cost + misc_cost)])
    cli_table.table_printer(cost_tab)
    print()
    


def tour():
    ''' This function plans the tour    '''

    df = read_data()
    state_list = list(df['state'].unique())
    state_p = cli_menu.menu_creator(state_list, 'Where you want to visit?\nList of states in India')

    state_fil = df['state'] == state_list[state_p]
    state_df = df[state_fil]

    system('cls')
    city_list = list(state_df['city'].unique())
    city_p = cli_menu.menu_creator(city_list, 'Be a more specific\nList of cities in ' + state_list[state_p])

    system('cls')
    print('Enter Tourists details:')
    try:
        adults = int(input('Enter the number of Adults: '))
    except ValueError:
        adults = 2
    try:
        children = int(input('Enter the number of children: '))
    except ValueError:
        children = 0
    tot_ppl = adults + (0.5*children)

    system('cls')
    try:
        print('Enter tour starting date (in DD-MM-YYYY fashion)')
        s_dd, s_mm, s_yyyy = enter_date()
        print('\n\nEnter tour ending date (in DD-MM-YYYY fashion)')
        e_dd, e_mm, e_yyyy = enter_date()
        days = day_diff(s_dd, s_mm, s_yyyy, e_dd, e_mm, e_yyyy)
    except ValueError:
        print("\n\nInvalid dates or date format entered!")
        system('pause')
        return

    s_date = str(s_dd).zfill(2) + '-' + str(s_mm).zfill(2) + '-' + str(s_yyyy)
    e_date = str(e_dd).zfill(2) + '-' + str(e_mm).zfill(2) + '-' + str(e_yyyy)

    system('cls')
    try:
        min_star = int(input('Enter minumum budget type hotel (1*, 2*, ... , 5*): '))
    except ValueError:
        min_star = 1

    try:
        max_star = int(input('Enter maximum budget type hotel (1*, 2*, ... , 5*): '))
    except ValueError:
        max_star = 5

    hotel_df, hotel_list = hotel_listing_cityStar(df, city_list[city_p], min_star, max_star)
    hotel_list.insert(0, ['id', 'Hotel Name', 'Area', 'Hotel Star Rating', 'Price (per night)'])
    hotel_list = list(map(list, hotel_list))

    try:
        system('cls')
        hotel_p = cli_table.point_to_table(hotel_list, 'List of hotels in ' + city_list[city_p])    #   selecting hotel
        
    except IndexError:
        print("No hotels found under your query")
        system('pause')
        return

    db_id = int(hotel_list[hotel_p+1][0])

    system('cls')
    hotel_sel = df.loc[df['db_id'] == db_id]    #   locating selected hotel
    print_hotel_details(hotel_sel, s_date, e_date, days, tot_ppl)

    try:
        map_p = input('Press M to open the hotel location in Google maps: ')
    except ValueError:
        map_p = 'x'
    if map_p.lower() == 'm':
        lat = hotel_sel.iloc[0]['latitude']
        longi = hotel_sel.iloc[0]['longitude']
        browser_map(lat, longi)

    try:
        rep_p = input('Press R to generate a report in text file: ')    #   save the report in text file
    except ValueError:
        rep_p = 'x'
    if rep_p.lower() == 'r':
        sys.stdout = open('Report.txt', 'w')    #   changing stdout to a file
        print_hotel_details(hotel_sel, s_date, e_date, days, tot_ppl)
        sys.stdout = sys.__stdout__ #changing stdout back to console
        system('report.txt')




# main
system('color F0')
while True:
    system('cls')
    main_menu = ['Set Home Location', 'Plan a Tour', 'About', 'Exit']
    main_p = cli_menu.menu_creator(main_menu, 'Trip Planner\nMain menu')

    system('cls')
    if main_p == 0: #   setting the home location
        df = read_data()
        state_list = list(df['state'].unique()) #   list the names of unique states
        state_p = cli_menu.menu_creator(state_list, 'Select HOME state') #   listng states

        state_fil = df['state'] == state_list[state_p]
        state_df = df[state_fil]    #   filter df to selected state

        system('cls')
        city_list = list(state_df['city'].unique()) # list uniue city in the filtered df
        city_p = cli_menu.menu_creator(city_list, 'Select HOME city in ' + state_list[state_p])  #   lisitng cities

        f = open('data\\home.txt', 'w') #   home location saved here
        f.write(str(city_list[city_p]))
        f.close()

    elif main_p == 1:   #   plan the tour
        tour()

    elif main_p == 2:   #   team details
        print("ABOUT THE PROJECT:\n")
        print('This project is done by the students of Group 8 from CSE2H')

        stud_table = [['Roll No.', 'Enrolment No.', 'Student name']]
        stud_table.append(['29', '12018009019439', 'KINJAL RAYKARMAKAR'])
        stud_table.append(['30', '12018009019562', 'MAINAK BHOWMICK'])
        stud_table.append(['31', '12018009019010', 'MAUSHOM MAJUMDAR'])
        stud_table.append(['32', '12018009019506', 'MD. UZAIFA'])

        cli_table.table_printer(stud_table)
        
        system('pause')

    elif main_p == 3:   #   quit
        sys.exit()