from __future__ import print_function
from datetime import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, timedelta

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
    
    dt =datetime.now()
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    print(start)
    print(end.isoformat())
    
    
    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='lbjlpmmfi6bvvp3j5lc450a3rk@group.calendar.google.com', # Work OKE 
                                        timeMin=str(start.isoformat()) +"Z",
                                        timeMax=str(end.isoformat()) +"Z",
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        try:
            print(event['summary'])
        except:
            pass

if __name__ == '__main__':
    main()