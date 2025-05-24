import redis
from fastapi import FastAPI

app = FastAPI()

redis_client = redis.Redis(host='localhost',port=6379,db=0)

@app.post("/publish/{message}")
async def publish_message(message: str):
    redis_client.publish("my_channel", message)
    return {"status": "Message published"}
 # Subscriber - Subscribing to a channel
def redis_listener():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("my_channel")
    for message in pubsub.listen():
        if message["type"] == "message":
            print(f"Received message: {message['data']}")

import threading
threading.Thread(target=redis_listener, daemon=True).start()


#  In this example:– The publisher (/publish/{message} endpoint) sends messages to a
#  Redis channel called my_channel.– The subscriber listens for messages on this channel and processes them
#  asynchronously.