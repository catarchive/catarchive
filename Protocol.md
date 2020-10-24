# Cat Archive Protocol 0.1.0

Basic syntax (UTF-8 encoded):

```
CAP/0.1.0 <TYPE> [DATA]...
```

## Types

### Client to server

- `AUTH`: Authenticate with the server. Contains one token as data.
- `IMAG`: Send a cat image to the server. Contains one URL as data.
- `URLS`: Ask the server for URLs to crawl. Contains no data.
- `PING`: Sent at intervals to signify normal operation. Contains no data.
 
### Server to client

- `STRT`: Tells the client to start crawling. Contains no data.
- `URLS`: In response to a client's `URLS`. Contains atleast one URL to crawl as data.
- `PING`: In response to a client's `PING` to signify normal operation. Contains no data.
