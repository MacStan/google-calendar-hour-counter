from __future__ import print_function
from datetime import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, timedelta
from dateutil.parser import parse
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'



def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    #DATE
    
    dt = datetime.now()
    start = dt - timedelta(days=dt.weekday()) 
    end = start + timedelta(days=6)
    start = start - timedelta(hours=dt.hour)
    print('start: ', start)
    print('end: ', end)
    
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='lbjlpmmfi6bvvp3j5lc450a3rk@group.calendar.google.com', # Work OKE 
                                        timeMin=str(start.isoformat()) +"Z",
                                        timeMax=str(end.isoformat()) +"Z",
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])


    dates = {}
    if not events:
        print('No upcoming events found.')
    for event in events:
        try:
            if( "You" in event['summary']):
                print(event['summary'])
                print()
                #print(date.year, date.month, date.day, date.hour, date.minute )
                date = parse(event['start']['dateTime'])
                
                if(date.day not in dates):
                    dates[date.day] = []
                    
                if(date.day in dates):
                    if( "entered" in event['summary']):
                        dates[date.day].append( ('S', date.hour, date.minute) )
                    else:
                        dates[date.day].append( ('E', date.hour, date.minute) )
        except:
            pass
    
    print(dates)
    days = []
    for date, value in dates.items():
        try:
            start = [x for x in value if x[0] == 'S'][0]
            end = [x for x in value if x[0] == 'E'][0]
            span = timedelta(hours = end[1], minutes = end[2]) - timedelta(hours = start[1], minutes = start[2])
            days.append(span)
            print( date, span )
        except:
            pass
            
    worktime = timedelta()
    for each in days:
        worktime += each
    
    worked = worktime.days * 24 + worktime.seconds /3600
    print(worked)
        
    
if __name__ == '__main__':
    main()