
# For local dev

# Create your own certificates

1. Place on server directory

```sh
     cd server/
   ```

2. Create certs folder

```sh
     mkdir certs
```

3. On certs folder create certificates

```sh
    openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
```


# RUN Server Locally for development 

   For RUN Server FROM root folder (~/open-llm-prototype)
   ```sh
        PYTHONPATH=./server uvicorn app.main:app --reload --ssl-keyfile=server/certs/key.pem --ssl-certfile=server/certs/cert.pem
   ```


# Curl example to test the server
   ```sh
        curl -k -X POST https://localhost:8000/chat \
        -H "Content-Type: application/json" \
        -d '{
        "query": "What does the code do?",
        "top_k":10,
        "response_mode": "compact",
        "temperature": 0.5
        }'
   ```