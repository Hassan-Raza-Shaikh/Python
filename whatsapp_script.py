import pywhatkit as kit
import time

# Your target numbers (must be in international format, e.g., 923001234567 for Pakistan)
numbers = [
    "923332333460",
    "923312513656",
    "923195529744",    # Example number 1
]
message = (
    "Hello, this is an official invite from Team Foxtrot "
)

# Loop through all numbers and send instantly
for number in numbers:
    try:
        kit.sendwhatmsg_instantly(f"+{number}", message, 15, True, 2)
        # params: phone, message, wait_time, tab_close, close_time
        print(f"Message sent to {number}")
        time.sleep(6)  # wait between sends so WhatsApp doesn’t block
    except Exception as e:
        print(f"Failed to send message to {number}: {e}")

print("Done sending messages.")