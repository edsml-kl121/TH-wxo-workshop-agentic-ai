```
curl -X POST "http://localhost:8000/send_gmail" \
-H "Content-Type: application/json" \
-d '{
  "to": "mew.chayutaphong@gmail.com",
  "subject": "<b>Test Email</b> r\\u0e32\\u0e21\\u0e19 \\u0e2b\\u0e21\\u0e48\\u0e32\\u0e19\\u0e04\\u0e23\\u0e31\\u0e1a \\u0e01\\u0e32\\u0e23\\u0e04\\u0e32\\u0e07",
  "body": "Hello from FastAPI! \n\n r\\u0e32\\u0e21\\u0e19 \\u0e2b\\u0e21\\u0e48\\u0e32\\u0e19\\u0e04\\u0e23\\u0e31\\u0e1a \\u0e01\\u0e32\\u0e23\\u0e04\\u0e32\\u0e07"
}'
```


```
curl -X POST "http://localhost:8000/create_calendar_event" \
-H "Content-Type: application/json" \
-d '{
  "title": "Team Meeting",
  "date": "2025-08-01",
  "time": "2-4pm",
  "attendees": ["Kandanai.Leenutaphong@ibm.com"]
}'
```