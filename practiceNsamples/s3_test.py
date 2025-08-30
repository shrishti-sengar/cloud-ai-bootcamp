import boto3

class MyBucket:

    def __init__(self, bucket_name):
        # Create S3 client
        self.s3 = boto3.client('s3')
        self.name = bucket_name

    def list_all(self):
        # List all buckets
        response = self.s3.list_buckets()
        print("Buckets:")
        for bucket in response['Buckets']:
            print(f" {bucket['Name']}")

    def download_file(self, key_name, download_path):
        """Download a file from S3"""
        try:
            self.s3.download_file(self.name, key_name, download_path)
            print(f"\n Downloaded s3://{self.name}/{key_name} -> {download_path}")
        except Exception as e:
            print(f"\n Download failed: {e}")


    def upload_file(self, file_path, key_name):
        """Upload a file from S3"""
        try:
            self.s3.upload_file(file_path, self.name, key_name)
            print(f"\n Uploaded {file_path} to s3://{self.name}/{key_name}")
        except Exception as e:
            print(f"\n Upload failed: {e}")


if __name__ == "__main__":
    bucket_name = "cloud-ai-sss"
    bucket = MyBucket(bucket_name)
    bucket.list_all()
    bucket.upload_file(r"C:\Users\shrishti.sengar\OneDrive - ION\Desktop\Cloud+AI\test.txt", "test_upload.txt")
    bucket.download_file("test_upload.txt", r"C:\Users\shrishti.sengar\OneDrive - ION\Desktop\Cloud+AI\downloaded_test.txt")


