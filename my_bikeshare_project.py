import time
import pandas as pd
import numpy as np
import statistics
import datetime

CITY_DATA = {'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv'}

def get_filters():
   """
   Asks user to specify a city, month, and day to analyze.

   Returns:
       (str) city - name of the city to analyze
       (str) month - name of the month to filter by, or "all" to apply no month filter
       (str) day - name of the day of week to filter by, or "all" to apply no day filter
   """
   print('\nHello! Let\'s explore some US bikeshare data!')
   # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
   print('-'*40)
   print('You can press "q" to exit the program at anytime!')
   print('-'*40)

   valid_cities = ["new york city", "chicago", "washington"]
   valid_response = False
   while valid_response == False:
       print("\nPlease enter the city you wish to display!")
       city_entered = input("\nEnter either 'New York City', 'Chicago' or 'Washington'.  ").lower()
       if city_entered in valid_cities:
           print('\nYou selected: ', city_entered.title())
           valid_response = True
       elif city_entered == 'q':
           quit()
       else:
           print("\nYou have entered an invalid entry. Please try again.")
           print('-'*40)

   # get user input for month (all, january, february, ... , june)
   valid_response = False
   valid_months_numbers = [0, 1, 2, 3, 4, 5, 6]
   valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
   valid_dates = dict(zip( valid_months_numbers, valid_months))
   print('-'*40)

   while valid_response == False:
       try:
           print('\nMonths available are from Jan - June. For Jan, enter 1. For Feb, enter 2 etc.')
           print('Or, enter 0 to retrieve data from all months')
           month = int(input('\nPlease enter a month number: '))
           if month in valid_dates:
               print('\nYou have selected to receive data from the month(s): ', valid_dates[month].title())
               valid_response = True
           elif month == 'q':
               quit()
           else:
               print('\nInvald Input, only values 0-6 are accepted!')
               print('-'*40)
       except:
           print('\nInvald Input! Input should be a number, please try again!')
           print('-'*40)



   # get user input for day of week (all, monday, tuesday, ... sunday)
   valid_response = False
   valid_days_numbers = [0, 1, 2, 3, 4, 5, 6, 7]
   valid_days_text = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
   valid_days = dict(zip( valid_days_numbers, valid_days_text))
   print('-'*40)

   while valid_response == False:
       try:
           print('\nPlease enter between 1-7 for each day of the week. For example, 1 = monday, 2 = tuesday etc')
           print('Or, enter 0 to retrieve data from all days of the week.')
           day = int(input('\nPlease enter a day number: '))
           if day in valid_days:
               print('\nYou have selected to receive data from the day(s): ', valid_days[day].title())
               print('-'*40)
               valid_response = True
           elif day == 'q':
               quit()
           else:
               print('\nInvald Input, selected. Only numbers 0-7 are accepted!')
               print('-'*40)
       except:
           print('\nInvald Input! Input should be a number, please try again!')
           print('-'*40)

   print('-'*40)
   print('\nYour selections are:')
   print('City:', city_entered.title(), '\nMonth(s):', valid_dates[month].title(),
   '\nDay(s):', valid_days[day].title())
   print('-'*40)

   city = city_entered
   month = valid_dates[month]
   day = valid_days[day]

   valid_response = False
   while valid_response == False:
       correct_input = input('\nAre these options correct? Please enter either Y/N. ').lower()
       if correct_input == "y":
           return city, month, day
           valid_response = True
           break
       elif correct_input == "n":
           print('-'*40)
           print('Reloading Options')
           print('-'*40)
           get_filters()
       elif correct_input == 'q':
           quit()
       else:
           print('\nPlease only enter "Y" for yes or "N" for no.')





def load_data(city, month, day):

   """Load the input data that the user has entered in to the dataframe.

   INPUT:
   city: str: The city the user decided to filter by.
   month: str: The month the user decided to filter by. 'all' will be entered if not filter.
   day: str: The day the user decided to filter by. 'all' will be entered if not filter.

   OUTPUT:
   The dataframe (df) will be updated to only display information filtered by the users input
   """

   df = pd.read_csv(CITY_DATA[city])
   df['Start Time'] = pd.to_datetime(df['Start Time'])
   df['month'] = df['Start Time'].dt.month
   df['day'] = df['Start Time'].dt.weekday_name
   df['hour'] = df['Start Time'].dt.hour
   df.fillna('Other')
   print('-'*40)
   print('-'*40)
   print('-'*40)


   if month != 'all':
       # use the index of the months list to get the corresponding int
       months = ['january', 'february', 'march', 'april', 'may', 'june']
       month = months.index(month) + 1

       df = df[df['month'] == month]


   if day != 'all':
       # filter by day of week to create the new dataframe
       df = df[df['day'] == day.title()]


   return df

# Function to check the filters that will be used when retreiving data (months/days etc)
def month_filter_check(df):

   """Check to see if the user has decided to filter by month

   INPUT:
   dataframe

   OUTPUT:
   A variable that holds whether the month has or has not been filtered.
   """
   month_filtered = True
   x = len(set(df['month']))
   if x != 1:
       month_filtered = False
   return month_filtered
# Function to check the filters that will be used when retreiving data (months/days etc)
def day_filter_check(df):
   """Check to see if the user has decided to filter by day.

   INPUT:
   dataframe

   OUTPUT:
   A variable that holds whether the month has or has not been filtered.
   """
   day_filtered = True
   y = len(set(df['day']))
   if y != 1:
       day_filtered = False
   return day_filtered

def filter_display(month_filtered, day_filtered, month, day):
   """Select the correct output display to the user.

   INPUT:
   month_filtered - True or False
   day_filtered - True or False
   month - User selected month.
   day - User selected day.
   OUTPUT:
   prints the correct display to the user, informing them on whether the data has been filtered and if so, how.
   """
   if month_filtered == False:
       if day_filtered == False:
           print('\nOver the entire period of data:')
       else:
           print('\nOver the entire period of data, but only during the weekday of',
           day.title())
   else:
       if day_filtered == False:
           print('\nFor the month of', month.title(), 'and for all weekdays:')
       else:
           print('\nFor the month of', month.title(), 'but only on the weekday of', day.title())


def time_stats(df):
   """Displays statistics on the most frequent times of travel."""

   print('\nCalculating The Most Frequent Times of Travel...\n')
   start_time = time.time()

   popular_month = df['month'].mode()[0]
   popular_day = df['day'].mode()[0]
   popular_hour  = df['hour'].mode()[0]

   if month_filter_check(df) == False:
       months = ['january', 'february', 'march', 'april', 'may', 'june']
       popular_month = months[(popular_month - 1)]
       print('The most popular month is:', popular_month.title())

   if day_filter_check(df) == False:
       print('The most popular day is:', popular_day)

   popular_hour = str(popular_hour)
   popular_hour = popular_hour + ':00'
   print('The most popular hour is:', popular_hour)

   print("\nThis took %s seconds." % (time.time() - start_time))
   print('-' * 40)


def station_stats(df,  month_filtered, day_filtered):
   """Displays statistics on the most popular stations and trip."""

   print('\nCalculating The Most Popular Stations and Trip...\n')
   start_time = time.time()

   # display most commonly used start station

   start_station_count = df.groupby(['Start Station']).size()
   popular_start_station = start_station_count.idxmax()
   print('The most common start station is:', popular_start_station)

   end_station_count = df.groupby(['End Station']).size()
   popular_end_station = end_station_count.idxmax()
   print('The most common end station is:', popular_start_station)

   popular_combination_count = df.groupby(['Start Station', 'End Station']).size()
   popular_combination = popular_combination_count.idxmax()
   popular_combination = '\nEnd: '.join(popular_combination)

   print('The most popular trip is: \nStart:', popular_combination)





   print("\nThis took %s seconds." % (time.time() - start_time))
   print('-' * 40)


def trip_duration_stats(df, month_filtered, day_filtered):
   """Displays statistics on the total and average trip duration."""

   print('\nCalculating Trip Duration...\n')
   start_time = time.time()

   total_travel_time = int(df['Trip Duration'].sum())
   mean_travel_time =  int(df['Trip Duration'].mean())
   total_travel_time_formatted = str(datetime.timedelta(seconds=total_travel_time))
   mean_travel_time_formatted = str(datetime.timedelta(seconds=mean_travel_time))

   print('The total travel time is:',
   total_travel_time_formatted)
   print('The mean travel time, in the format of hh:mm:ss is:',
   mean_travel_time_formatted)

   print("\nThis took %s seconds." % (time.time() - start_time))
   print('-' * 40)


def user_stats(df, month_filtered, day_filtered):
   """Displays statistics on bikeshare users."""

   print('\nCalculating User Stats...\n')
   start_time = time.time()

   user_type = df.groupby(['User Type']).size()
   print(user_type.to_string())

   if 'Gender' in df:
       print()
       gender_type = df.groupby(['Gender']).size()
       print(gender_type.to_string())

   if 'Birth Year' in df:
       print()
       earliest_birth = df['Birth Year'].min()
       print('Earliest DOB:', int(earliest_birth))
       recent_birth = df['Birth Year'].max()
       print('Most recent DOB:', int(recent_birth))
       common_birth = df.groupby(['Birth Year']).size()
       print('Most common DOB:', int(common_birth.idxmax()))



   # Display counts of gender

   # Display earliest, most recent, and most common year of birth

   print("\nThis took %s seconds." % (time.time() - start_time))
   print('-' * 40)


def raw_data_display(df):
   """Displays the raw, filtered data from the dataframe."""

   display_raw = True
   while display_raw == True:
       raw_data = input('\nWould you like to see any of the raw data? Enter either Y or N: ').lower()
       if raw_data == "y":
           print('-'*40)
           print('Loading Raw Data')
           print('-'*40)

           while True:
               print('-'*40)
               print('\nYou can enter C to cancel and go back at any time.')
               head_or_tail =  input('\nWould you like to see the first or the last rows?'
               ' Enter either F or L: ' ).lower()
               if head_or_tail == "f":
                   print()
                   print(df.head())
                   i = 5
                   while True:
                       print_more_head = input('\nWould you like to load five more rows? Enter either Y or N: ').lower()
                       if print_more_head == "y":
                           i = i + 5
                           print(df.head(i))
                       elif print_more_head == "n":
                           break
                       elif print_more_head == "q":
                           quit()
                       else:
                           print('\nPlease only enter "Y" for yes or "N" for no.')

               elif head_or_tail == "l":
                   print(df.tail())
                   i = 5
                   while True:
                       print_more_tail = input('\nWould you like to load five more rows? Enter either Y or N: ').lower()
                       if print_more_tail == "y":
                           i = i + 5
                           print(df.tail(i))
                       elif print_more_tail == "n":
                           break
                       elif print_more_tail == "q":
                           quit()
                       else:
                           print('\nPlease only enter "Y" for yes or "N" for no.')

               elif head_or_tail == "q":
                   quit()

               elif head_or_tail == "c":
                   display_raw = False
                   break

               else:
                   print('\nPlease only enter "Y" for yes or "N" for no, or "C" to cancel.')

       elif raw_data == "n":
           break
       elif raw_data == "q":
           quit()
       else:
           print('\nPlease only enter "Y" for yes or "N" for no.')

def main():
   """Holds all of the main functions and calls them when appropriate."""

   while True:
       city, month, day = get_filters()
       df = load_data(city, month, day)
       day_filtered = day_filter_check(df)
       month_filtered = month_filter_check(df)

       filter_display(month_filtered, day_filtered, month, day)
       time_stats(df)

       filter_display(month_filtered, day_filtered, month, day)
       station_stats(df, month_filtered, day_filtered)

       filter_display(month_filtered, day_filtered, month, day)
       trip_duration_stats(df, month_filtered, day_filtered)

       filter_display(month_filtered, day_filtered, month, day)
       user_stats(df, month_filtered, day_filtered)

       raw_data_display(df)


       while True:
           restart = input('\nWould you like to restart? Enter either Yes or No: ').lower()
           if restart == "yes":
               print('-'*40)
               print('Reloading Options')
               print('-'*40)
               break
           elif restart == "no":
               quit()
           elif restart == 'q':
               quit()
           else:
               print('\nPlease only enter "Yes" or "No"')

if __name__ == "__main__":
   main()
