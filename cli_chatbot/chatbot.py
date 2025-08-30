from openai import OpenAI
import boto3
import os
from datetime import datetime

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# AWS S3 client
s3 = boto3.client("s3")
bucket_name = "cli_chatbot-log-analysis"


def chat_with_ai(log_to_file=True, upload_to_s3=True):
    print("Chatbot ready! Type 'exit' to quit.\n")
    local_log_file = "chat_log.txt"

    while True:
        user_input = input("You: ")

        if not user_input:  # Skip empty input
            print("⚠️ Please enter a message.")
            continue

        if user_input.lower() == "exit":
            print("Chat ended.")
            break

        # Call OpenAI Chat API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}]
        )

        ai_reply = response.choices[0].message.content
        print("AI:", ai_reply)

        # --- Save logs locally ---
        if log_to_file:
            with open(local_log_file, "a", encoding="utf-8") as f:
                f.write(f"User: {user_input}\n")
                f.write(f"AI: {ai_reply}\n\n")

    # --- Upload complete session log to S3 once ---
    if upload_to_s3 and log_to_file:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        s3_key = f"logs/session_{timestamp}.txt"
        s3.upload_file(local_log_file, bucket_name, s3_key)
        print(f"✅ Uploaded full session log to S3: {s3_key}")


if __name__ == "__main__":
    while True:
        log_input = input("Do you want to save chat logs? (yes/no): ").strip().lower()
        if log_input in ["yes", "no"]:
            log_flag = log_input == "yes"
            break
        print("Please enter 'yes' or 'no'.")

    chat_with_ai(log_to_file=log_flag, upload_to_s3=True)
