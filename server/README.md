
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


# Curl example to test the server (Can be tested using postman too)

1. Start a session, 


    Run:

    ```sh
        curl -k -X POST https://localhost:8000/session/ \
        -H "Content-Type: application/json" \
   ```

    this returns a json with a session_id:

    ```json response
   {
    "session_id": <session_id number>
   }
   ```

2. Start a chat, using the session_id value on payloadon key session_id.

   ```sh
        curl -k -X POST https://localhost:8000/chat \
        -H "Content-Type: application/json" \
        -d '{
        "query": "What does the code do?",
        "session_id": <session_id>,
        "top_k":10,
        "temperature": 0.5,
        "response_mode": "compact",
        }'
   ```
