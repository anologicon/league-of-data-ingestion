from tempfile import NamedTemporaryFile
import boto3
import datetime
from typing import List
import json
from .writer_interface import WriterInterface
import os
from dotenv import load_dotenv

load_dotenv()


class MinioWriter(WriterInterface):
    def __init__(self, bucket_name: str):
        self.bucket = bucket_name
        self.tempfile = NamedTemporaryFile()
        self.client = boto3.client(
            "s3",
            endpoint_url=os.environ["MINIO_URL"],
            aws_access_key_id="minio-root-user",
            aws_secret_access_key="minio-root-password",
            aws_session_token=None,
            config=boto3.session.Config(signature_version="s3v4"),
            verify=False,
        )

    def write(self, file_path: str, json_data: [List, dict]):
        file_name = f"{file_path}.json"
        self._write_to_file(json_data)
        self.client.put_object(Body=self.tempfile, Bucket=self.bucket, Key=file_name)

    def _write_row(self, row: str) -> None:
        with open(self.tempfile.name, "a") as f:
            f.write(row)

    def _write_to_file(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        if isinstance(data, List):
            for row in data:
                self._write_to_file(row)
