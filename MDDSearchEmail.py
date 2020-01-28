from importlib import reload

import requests
import json
import smtplib
import SqlliteUtil
from sqlite3 import Error
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Variables to edit
headers = {'apikey': '<your-api-key>'}
email = 'youremail@gmail.com';
password = 'Password';
search_string = 'Maladaptive Daydreaming' #change it to a different search string if you want
params = (
    ('q', search_string),
    ('device', 'desktop'), #you can change this to mobile if you want
    ('location', 'United States'),
    ('num', '20'),
)

response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
json_data = json.loads(response.text.encode("ascii", 'replace'))

msg = MIMEMultipart('alternative')
msg['Subject'] = 'New Search results for query '+ search_string
msg['From'] = email
msg['To'] = email
message = ""
conn = SqlliteUtil.create_connection('pythonsqlite.db')
counter = 0
for data in json_data['organic']:
    try:
        entry = SqlliteUtil.search_result(conn, data['url'])
        if entry is None:
            print(entry)
            SqlliteUtil.create_result(conn, (data['url'], data['title']))
            message += 'Title: ' + data['title'] + ' Url: ' + data['url']
            message += '\n'
            counter += 1
        else:
            print("Entry already exists")
    except KeyError:
        pass
    except Error as e:
        print(e)
        continue
conn.commit()
conn.close()
if counter is 0:
    message = "No new search results this week"

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
body = MIMEText(message, "plain")
msg.attach(body)
try:
    # start TLS session
    s.starttls()
    s.login(email, password)
    # message to be sent 
    s.sendmail(email, email, msg.as_string())
    print('Email sent successfully')
except Error as e:
    print(e)
    print('Couldn\'t send the email')
finally:
    s.quit()
