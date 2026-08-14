import os

message = os.getenv("MESSAGE", "This is a default message from the container manager")

print(message)
