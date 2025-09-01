AI Chatbot on AWS (API Gateway + Lambda + S3)
This project implements a serverless AI chatbot using AWS Lambda, API Gateway, and S3.
The chatbot calls the OpenAI API for responses and logs each session to an S3 bucket.

### How it works
   [ Client / Postman ]
            |
            v
     [ API Gateway ]
            |
            v
      [ AWS Lambda ]
            |
      --------------------
      |                  |
      v                  v
 [ OpenAI API ]     [ AWS S3 ]

 (Generate reply)   (Store session logs)

###

### Sample Usage & Output
`Request (Postman → API Gateway)`
    POST https://<api-id>.execute-api.eu-north-1.amazonaws.com/dev/chatbot
    Content-Type: application/json
    {
      "message": "Shrishti Here!"
    }

`Lambda Response`
    {
        "session_id": "20250830_123456",
        "user_input": "Shrishti Here!",
        "ai_reply": "Hello Shrishti! 👋 How can I assist you today?",
        "log_file": "logs/session_20250830_123456.txt"
    }

`S3 Log File (logs/session_20250830_123456.txt)`
    User: Shrishti Here!
    AI: Hello Shrishti! 👋 How can I assist you today?


###

#Infrastructure
    1. Launch EC2 instance
        -Download key.pem
        -Attach IAM role for build tasks
    2. Create IAM Role with full s3 access
        -Used by Lambda to read/write chat logs
    3. Create S3 bucket
        -Example: chatbot-log-analysis
        -Will store per-session chat logs under logs/

#Prepare Project Folder
    cloudaibootcamp/
    ├── src/
    │   ├── lambda_function.py
    │   ├── utils/
    │   │   ├── __init__.py
    ├── requirements.txt
    ├── build.ps1   # Windows build script
    ├── build.sh    # Linux/EC2 build script


    1. Dependencies
        -Lambda does not include external libraries like openai by default.
        -You must package dependencies either:
            -Inside the deployment zip (lambda_deploy.zip)
            -Or install them into a Lambda Layer

#Build and deploy Lambda Package
    lambda_deploy.zip
    ├── lambda_function.py
    ├── openai/         # dependency folder
    ... other dependencies ...

    -WS Lambda expects lambda_function.py and the openai/ folder directly at the top level of the zip.

    1. Dependencies must be installed in a Linux-compatible environment. Options:
        -Docker with Amazon Linux
        -AWS Cloud9
        -Lambda Layer
        -EC2 instance (DIY Cloud9)
          -> git clone <repo>
          -> ./build.sh

.
    2. Create & Configure Lambda
        -Create Lambda function (Python 3.11 runtime)
        -Assign IAM role with S3 access
        -Set environment variable OPENAI_API_KEY
        -Upload lambda_deploy.zip
        -Configure handler: lambda_function.lambda_handler
        -Increase function timeout (default 3s → ~30s)
        -Add test events in Lambda console

#Expose as REST API
     1. Use AWS API Gateway to create a REST API.
         -Integrate the API Gateway resource/method with your Lambda function.
         -Deploy the API to a stage (e.g., dev).
         -Copy the generated endpoint URL.
         -Test the endpoint in Postman by sending a request body, and verify you receive the Lambda response and session log in s3 bucket.
           -> { "message": "Hello chatbot!" }

### Future Enhancements

-Structured Logging → Save logs in JSON format instead of plain text for easier analysis
-Session Memory → Maintain conversation history per session, not just single Q&A
-Error Handling → Add retries, input validation, and clearer error messages
-Frontend Demo → Create a simple web/CLI interface to showcase the chatbot beyond Postman
-CI/CD Pipeline → Automate Lambda deployment using GitHub Actions or AWS CodePipeline
-Security → Restrict API Gateway with authentication (e.g., API keys, Cognito)

