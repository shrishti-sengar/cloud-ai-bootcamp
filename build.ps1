# Clean build folder
Remove-Item -Recurse -Force lambda_package -ErrorAction SilentlyContinue
mkdir lambda_package

# Install dependencies into build folder
pip install --no-cache-dir -r requirements.txt -t .\lambda_package

# Copy your src files into build folder
Copy-Item .\src\* .\lambda_package\ -Recurse

# Create zip (contents only, no nested folder)
cd lambda_package
Compress-Archive -Path * -DestinationPath ..\lambda_deploy.zip -Force
cd ..
