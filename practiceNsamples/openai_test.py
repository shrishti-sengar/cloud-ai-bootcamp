from openai import OpenAI
import os

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_ai(log_to_file=True):
    print("Chatbot ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

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

        # Optional logging
        if log_to_file:
            with open("chat_log.txt", "a", encoding="utf-8") as f:
                f.write(f"User: {user_input}\n")
                f.write(f"AI: {ai_reply}\n\n")

if __name__ == "__main__":
    # Ask user whether to log or not
    while True:
        log_input = input("Do you want to save chat logs? (yes/no): ").strip().lower()
        if log_input in ["yes", "no"]:
            log_flag = log_input == "yes"
            break
        print("Please enter 'yes' or 'no'.")

    chat_with_ai(log_to_file=log_flag)
