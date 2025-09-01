#!/bin/bash
set -e  # Exit on error

echo "Starting Lambda build with Python 3.11..."

# Ensure Python 3.11 is installed
if ! command -v python3.11 &> /dev/null
then
    echo "Python 3.11 not found. Installing..."
    sudo dnf install -y python3.11
fi

# Ensure pip3.11 is installed
if ! command -v pip3.11 &> /dev/null
then
    echo "pip3.11 not found. Installing..."
    sudo dnf install -y python3.11-pip
fi

# Clean previous builds
rm -rf lambda_package lambda_deploy.zip
mkdir lambda_package

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip3.11 install --no-cache-dir -r requirements.txt -t lambda_package

# Copy source code
echo "Copying source code..."
cp -r src/* lambda_package/

# Create zip
echo "Creating deployment package..."
cd lambda_package
zip -r ../lambda_deploy.zip .
cd ..

echo "Build complete: lambda_deploy.zip is ready!"
