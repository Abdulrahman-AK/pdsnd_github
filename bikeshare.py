import time
import json
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

def check_input(input_str,input_type):
    """
    check user input.
    input_str: user inpute
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        input_read=input(input_str)
        try:
            if input_read in ['new york city', 'chicago', 'washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Incorrect input, the input should be one of the following: New York City, Chicago or Washington")
                if input_type == 2:
                    print("Incorrect input, the input should be one of the following: January, February, March, April, May, June or all")
                if input_type == 3:
                    print("Incorrect input, the input should be: sunday, monday, tuesday wednesday, thursday, friday, saturday or all")
        except ValueError:
            print("Incorrect input")
    return input_read

def get_filters():
    """
  User input filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # cities
    city = check_input("Would you like to see the data for New York City, Chicago or Washington? *please use lower case only*",1)
    # months
    month = check_input("Month (January, February, March, April, May, June or all *please use lower case only*)?", 2)
    # days
    day = check_input("Day? (sunday, monday, tuesday wednesday, thursday, friday, saturday or all *please use lower case only*)", 3)
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
   loads data based on filters applied
    """
    print()
    print(" Filters applied : "
          "[ {}, {}, {}] ".format(city, month, day))
    print()
 
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print()
    print('User Stats '.center(80, '*'))
    start_time = time.time()

    # user-dtapoints
    
    if 'User Type' in df.columns:
        print()
        print(df['User Type'].value_counts())
        # print()
    # m/f
    if 'Gender' in df.columns:
        print(' Gender stats '.center(60, '-'))
        df['Gender'].replace(np.nan, 'not disclosed', inplace=True)
        print(df['Gender'].value_counts(dropna=False))
        # print()
    # DOB
    if 'Birth Year' in df.columns:
        print(' Age stats '.center(60, '-'))
        print('Earliest Birth '
              'Year '.ljust(40, ' '), int(df['Birth Year'].min()))
        print('Most recent Birth '
              'Year '.ljust(40, ' '), int(df['Birth Year'].max()))
        print('Most common Birth '
              'Year '.ljust(40, ' '), int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*150, '\n')


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    if 'Start Time' in df.columns:
        print()
        print('Most Frequent Times '
              'of Travel '.center(80, '*'))
        start_time = time.time()
        print()
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        popular_month = df['month'].mode()[0]
        print('Most common Month'.ljust(40, ' '), popular_month)
        df['day_of_week'] = df['Start Time'].dt.day_name()
        popular_day = df['day_of_week'].mode()[0]
        print('Most common day of the week'.ljust(40, ' '), popular_day)
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print('Most common Start Hour'.ljust(40, ' '), popular_hour)


        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*150, '\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print()
    print('Most Popular Stations and Trip '.center(80, '*'))
    start_time = time.time()
    print()

    if 'Start Station' in df.columns:
        print('Most commonly used Start '
              'station '.ljust(40, ' '), df['Start Station'].mode()[0])

 
    if 'End Station' in df.columns:
        print('Most commonly used End '
              'station '.ljust(40, ' '), df['End Station'].mode()[0])

  
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['route'] = df['Start Station'] + ' -> ' + df['End Station']
        print('Most frequent route '.ljust(40, ' '), df['route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*150, '\n')


def trip_duration_stats(df):
    """Stats on the trip data i.e. duration."""

    print()
    if 'Trip Duration' in df.columns:
        print(' Calculating Trip Duration '.center(80, '*'))
        start_time = time.time()
        print()
        print('Max Travel Time '.ljust(40, ' '), df['Trip Duration'].max())
        print('Min Travel Time '.ljust(40, ' '), df['Trip Duration'].min())
        # display mean travel time
        print('Avg Travel Time '.ljust(40, ' '), df['Trip Duration'].mean())
        print('Most Travel '
              'Time '.ljust(40, ' '), df['Trip Duration'].mode()[0])
        # display total travel time
        print('Total Travel Time '.ljust(40, ' '), df['Trip Duration'].sum())

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*150, '\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        user_stats(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
    
        row = 5
        raw_data = input('Would you like to see raw data? '
                         'Enter (yes / no) : ').lower()
        df['Start Time'] = df['Start Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        while raw_data == 'yes':
            # 5 rows of raw data
            print(json.dumps(df.head(row).to_dict('index'), indent=1))
            raw_data = input('Would you like to see more '
                             'raw data? Enter (yes / no) : ').lower()
            row += 5

        restart = input('\nWould you like to restart? '
                        'Enter (yes / no) : ').lower()
        
        
        if restart.lower() != 'yes':
            break 
    print('Thank you for exploring this bikeshare data, see you next time!')
            
if __name__ == "__main__":
    main()
