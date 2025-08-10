## Testing

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

```
curl -X POST "http://localhost:8000/place_order" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "tablet",
    "quantity": 3
  }' | jq
```


## Setup

```
1. Create a gmail.
e.g.
demowxo27@gmail.com

2. Register via. Google cloud Platform (Login with the same email)
3. Create a new project called wxo-demo
4. Search APIs & Services (in library) and enable Gmail API & Google Calendar API, Generative Language API
5. Google Auth Platform -> overview -> project configuration -> add your email in. e.g. demowxo27@gmail.com
6. Google Auth Platform -> Clients -> Create client -> choose DESKTOP
7. Audience -> publish app
```

