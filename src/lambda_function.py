import os
import json
import boto3
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
s3 = boto3.client("s3")
bucket_name = "chatbot-log-analysis"


def lambda_handler(event, context):
    """
    AWS Lambda entry point
    event = request payload (API Gateway JSON)
    context = runtime info
    """

    try:
        # Extract user input from API Gateway POST body
        body = json.loads(event.get("body", "{}"))
        user_input = body.get("message", "").strip()
        session_id = body.get("session_id", None)

        if not user_input:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No input message provided"})
            }

        # If no session_id given, create one
        if not session_id:
            session_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        # Call openai
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}]
        )
        ai_reply = response.choices[0].message.content

        # S3 log file for this session
        s3_key = f"logs/session_{session_id}.txt"

        # Append to session log
        log_entry = f"User: {user_input}\nAI: {ai_reply}\n\n"

        # Try to get existing log, then append
        try:
            existing_log = s3.get_object(Bucket=bucket_name, Key=s3_key)["Body"].read().decode(
                "utf-8")
        except s3.exceptions.NoSuchKey:
            existing_log = ""

        updated_log = existing_log + log_entry

        # Upload back to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=updated_log.encode("utf-8")
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "session_id": session_id,
                "user_input": user_input,
                "ai_reply": ai_reply,
                "log_file": s3_key
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
