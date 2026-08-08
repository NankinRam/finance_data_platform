import os
from dotenv import load_dotenv
from minio import Minio
from pandas import DataFrame
import io

from src.logger import log

load_dotenv()

class MinioService:

    def __init__(self):
        self.client = Minio(
            endpoint=os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("ACCESS_KEY"),
            secret_key=os.getenv("SECRET_KEY"),
            secure=False
        )

    def __check_bucket(self, name_bucket: str):
        return self.client.bucket_exists(name_bucket)

    def load_original(self, object_name: str, file_path: str):
        if self.__check_bucket("finance-data"):

            self.client.fput_object(
            bucket_name="finance-data",
            object_name=object_name,
            file_path=file_path
            )

    def load_df(self, object_name: str, df: DataFrame):
        if self.__check_bucket("finance-data"):

            csv_bytes = df.copy().to_csv(index=False).encode("utf-8")
            buffer = io.BytesIO(csv_bytes)

            self.client.put_object(
                bucket_name="finance-data",
                object_name=object_name,
                data=buffer,
                length=len(csv_bytes),
                content_type="text/csv"
            )

    def unload_df(self, path: str):
        if self.__check_bucket("finance-data"):

            file = self.client.get_object(
                bucket_name="finance-data",
                object_name=path
            )

        return file