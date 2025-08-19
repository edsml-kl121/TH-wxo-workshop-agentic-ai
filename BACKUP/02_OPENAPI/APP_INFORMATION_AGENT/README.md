## Testing

# Get promotions
```
curl -X POST "http://localhost:8000/promotions"
```

# Get products
```
curl -X POST "http://localhost:8000/products"
```

# Get order status
```
curl -X POST "http://localhost:8000/orders/status"
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

