import pandas as pd
import datetime
import time
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    
    while True:
        # first loop to ask for city
        citycode = input("\nPlease Select a City:\nType 1 for Chicago City\nType 2 for Washington City\nType 3 for New York City\n\nThe Selected Code is: ")
        citydict = {1: "chicago", 2: "washington", 3: "new york city"}
        if not citydict.get(int(citycode)) == None:
            city = citydict.get(int(citycode))
            break
        else: print("\nYou need to enter a valid input")
    
    while True:
        #Second Loop to Ask for the filter
        filterinput = input("\nHow would you like to filter the data?\nType 1 for by month\nType 2 for by weekday\nType 3 for both\nType 4 for none\nThe Selected Code is: ") 

        if filterinput =="1":
            #internal loop to select the month
            while True:
                day = "all"
                month = input("\nPlease Enter the name of the Month: ").capitalize() 
                if (month in {"January", "Febraury", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"}):
                    break
                else: print("\nPlease Enter a Valid Month Name ex: January")
            break
        elif filterinput =="2":
            #internal loop to select the Day of Week
            while True:
                month = "all"
                day = input("\nPlease Enter the name of the Day: ").capitalize() 
                if (day in {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}):
                    break
                else: print("\nPlease Enter a Valid Day Name ex: Sunday")
            break
        elif filterinput =="3":
            #Two internal loops to select the Day of Week and Month
                
            while True:
                #internal loop to select the month
                month = input("\nPlease Enter the name of the Month: ").capitalize() 
                if (month in {"January", "Febraury", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"}):
                    break
                else: print("\nPlease Enter a Valid Month Name ex: January")
                
            while True:
                #internal loop to select the Day of Week
                day = input("\nPlease Enter the name of the Day: ").capitalize() 
                if (day in {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}):
                    break
                else: print("Please Enter a Valid Day Name ex: Sunday")   
            break        
        elif filterinput =="4":
            month = "all" 
            day = "all"
            break
            
        else:
            print("\nError, Please Enter a Valid Code")
    return(city,month,day)
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    print("\n............ Opening and Filtering Data, Please Wait")
    start = time.time()
        # 1- load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))

        # 2- convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

        # 3- extract hour, month and day of week from Start Time to create new columns
    df['hour'] = pd.DatetimeIndex(df['Start Time']).day
    df['month'] = pd.DatetimeIndex(df['Start Time']).strftime("%B")
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).strftime('%A')
    
    
        # 5- filter by month and day if applicable
    if not month == 'all' and not day == 'all': 
        df = df[(df['month'] == month) & (df['day_of_week'] == day)]
    elif not  month == 'all':
        df = df[(df['month'] == month)]
    elif not day == 'all': 
        df = df[(df['day_of_week'] == day)]

        # 7- create a new col for total trip
    df['total_trip'] = "From " + df['Start Station'] + " to " + df['End Station']
        # 8- return the computed values
    end = time.time()
    print("Filtering ecexution took ",end - start," seconds")
    return (df)    
def time_stats(df):
    #1 - find the most common hour, month, and day
    '''
       Computes Popular times of travel.

    Args:
        (df) Filtered Data Frame
    Returns:
        1- most common month
        2- most common day of week
        3- most common hour of day
    '''
    print("\n............ Computing the Most Common Time, Please Wait")
    start = time.time()
    popular_hour = df['hour'].value_counts().idxmax()
    popular_month = df['month'].value_counts().idxmax()
    popular_day = df['day_of_week'].value_counts().idxmax() 
    print("\nThe most popular hour in the filtered data is ", popular_hour)
    print("The most popular Month in the filtered data is ", popular_month)
    print("The most popular Day in the filtered data is ", popular_day)
    end = time.time()
    print("Analyzing Most Common Time Statistics took ", end - start, " seconds")
def station_stats(df):
    #2 Popular stations and trip
    """
       Computes stations and trip.

    Args:
       (df) Filtered Data Frame
    Returns:
        1- most common start station
        2- most common end station
        3- most common trip from start to end (i.e., most frequent combination of start station and end station)
    """
    print("\n............ Computing the Most Common Time, Please Wait")
    start = time.time()

    popular_start = df['Start Station'].value_counts().idxmax()
    popular_end = df['End Station'].value_counts().idxmax()
    popular_route = df['total_trip'].value_counts().idxmax()
    print("\nMost Popular Start Station is ", popular_start)
    print("Most Popular End Station is ", popular_end)
    print("Most Popular End Route is ", popular_route)
    end = time.time()
    print("Analyzing Most Common Stations Statistics took ", end - start, " seconds")
def trip_duration_stats(df):
    """
 Computes stations and trip.
    Args:
       (df) Filtered Data Frame
    Returns:
        1- total travel time
        2- average travel time
    """
    print("\n............ Analyzing Trip Duration Statistics, Please Wait")
    start= time.time()
    df['Trip duration'] = df['End Time'] - df['Start Time']
    total_time = df['Trip duration'].sum()
    Average_time = df['Trip duration'].mean()
    print("\nThe Total Durations of all Trips is: ", total_time)
    print("The Average Trip Duration is: ", Average_time)
    end = time.time()
    print("Analyzing Trip Duration Statistics took ", end - start, " seconds") 
def user_stats(df):
    #4 print statistics related to users
    """
    "
       Computes stations related to users.

    Args:
       (df) Filtered Data Frame
    Returns:
        1- counts of each user type
        2- counts of each gender (only available for NYC and Chicago)
        3- earliest, most recent, most common year of birth (only available for NYC and Chicago)

    """
    print("\n............ Analyzing User Statistics, Please Wait")
    start= time.time()
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print("\nThe Counts for each user type is as the following:\n",user_types)


    # print  counts of gender
    try:
        user_genders = df['Gender'].value_counts()
        print("\nThe Counts for each user gender is as the following:\n", user_genders)
    except: print("\nUnfortunately, there is no Gender Data for the selected City")


    
    # print  earlierst birth year
    try:

        min_birthyear = df['Birth Year'].min()
        print("\nThe earliest birth year is ", int(min_birthyear))
        # print  latest birth year
        max_birthyear = df['Birth Year'].max()
        print("\nThe most recent birth year is ", int(max_birthyear))
        # print  most common birth year
        common_birthyear = df['Birth Year'].value_counts().idxmax()
        print("\nThe most common birth year is ", int(common_birthyear))   
    except: print("\nUnfortunately, there is no birth year Data for the selected City")
    end = time.time()
    print("Analyzing User's Statistics took ", end - start, " seconds")
def display_data(df):
    print(df.iloc[0:5])
    min = 0
    max = 5
    while True:
        cont = input("Do you want to load five more rows?? (Yes/No): ")
        if cont.capitalize() == "Yes" :
            min+=5
            max+=5
            print(df.iloc[min:max])
        elif cont.capitalize() == "No" :
            break
        else: print("Please Enter a Valid Answer")  
def main():
    #Code to Start the program   
    while True:
        #Start the User Interface
        inputs = get_filters()
        city = inputs[0]
        month = inputs[1]
        day=inputs[2]
        
        #load and filter the data
        df = load_data(city,month,day)
        try:
            #Start the program functions one by one
            while True:
                mode = input("\nPlease Select a Mode:\nType 1 displaying the filtered Data\nType 2 for calculating statistics\nThe Selected Code is: ")
                if mode == "1" :
                    display_data(df)
                    break
                if mode == "2" :
                    time_stats(df)
                    station_stats(df)
                    trip_duration_stats(df)
                    user_stats(df)
                    break
                else: print("Please insert a valid input")
        except: print("Unfortunately there is no data for the filtered Day and Month")
        #ask the user if he want to restart
        while True:
            Quit_question = input("Do you Want to Make Another Computation (Yes/No): ").capitalize()
            if (Quit_question in {"Yes", "No"}) == False: print("Please Enter a Valid Answer")
            else: break
        if Quit_question == "No": break 
main()   


