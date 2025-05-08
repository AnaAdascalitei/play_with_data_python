import pandas as pd
import matplotlib

df = pd.read_csv('ViewingActivity-sample.csv')

#print(df.shape)

#drop the unnecessary columns, not a good idea lor a large scale projects
df = df.drop(['Profile Name', 'Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark', 'Country'], axis=1)
#print(df.head(1)) #see how the csv looks

#how much and when you watched The Office

#print(df.dtypes) #all 3 columns stored as objects; start time, duration, title
'''
convert Start time to datetime - panda can undersatan and perform calculations
convert Start Time from utc to my time zone - romanian time zone
convert Duration to timedelta - panda can undersatan and perform calculations
'''

#step 1 - conver Start Time to datetime using panda

df['Start Time'] = pd.to_datetime(df['Start Time'], utc = True)
#print(df.dtypes)

#we have to use set_index in order to use tz_convert on a DateTimeIndex

df = df.set_index('Start Time') 

#convert to eest time
df.index = df.index.tz_convert('Europe/Bucharest')

#reset the index so it is a column again
df = df.reset_index()

#print(df.head(1))


#step 2 - duration - convert to timedelta - measure of time that panda understands

df['Duration'] =  pd.to_timedelta(df['Duration'])

#print(df.dtypes)

#step 3 - create a new dataframe called office - where we will populate with rows where the Title column contains 'The Office(U.S)'

#use str.contains()

office = df[df['Title'].str.contains('The Office (U.S.)', regex=False)]
#contains the rows in which the Title column contains that title

#print(office.sample(20))  #check the first 20 rows

#step 4 - filter when the duration is >1min, because it takes into account the trailers/"preview" views

office = office[(office['Duration'] > '0 days 00:01:00')]
#print(office.sample(20))


#step 5 - analyze data! how much did i watch the office

print(office['Duration'].sum()) # watched the office for 1 day, 14 hours, 57 minutes and 28 seconds

#step 5' - when did i watch the office - on which days of the week did i watch the most ; during which hours of the day do i most often start Office episodes

office['weekday'] = office['Start Time'].dt.weekday
office['hour'] = office['Start Time'].dt.hour

print(office.head(1))

#step 6 - plot some charts/ghraps of viewing habits by day of the week

office['weekday'] = pd.Categorical(office['weekday'], categories= [0,1,2,3,4,5,6], ordered=True) # we defined the days Monday-Sunday

office_by_day = office['weekday'].value_counts() # office by day - for each weekday

office_by_day = office_by_day.sort_index() #sort by categorical Monday(0)-Sunday(6)

matplotlib.rcParams.update({'font.size': 22}) #this is for aesthetics, make the dont larger for reading a bit easier

office_by_day.plot(kind='bar', figsize=(20,10), title='Office Episodes watched by day') #plot minutes/weekday



#step 7 - same data, but by hour

office['hour'] = pd.Categorical(office['hour'], categories= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], ordered=True) # we defined the hours

office_by_hour = office['hour'].value_counts() # office by hou - for each hour

office_by_hour = office_by_hour.sort_index() #sort by categorical hour 0-23

office_by_hour.plot(kind='bar', figsize=(20,10), title='Office Episodes watched by hour') #plot minutes/hour of the day


#step 8 - same data, but anaylze the most and least watched episodes

# Count how many times each episode was watched
episode_counts = office['Title'].value_counts()

most_watched = episode_counts.head(1) #see most watched episode(s)

least_watched = episode_counts[episode_counts == episode_counts.min()] #see least watched episode(s)

print("Most watched episode:")
print(most_watched)

print("\nLeast watched episode(s):")
print(least_watched)
