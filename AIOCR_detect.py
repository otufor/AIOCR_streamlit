from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.cognitiveservices.vision.computervision.models import _models_py3
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json


class AiocrDetect:
    def __init__(self, subscription_key, endpoint) -> None:
        # if os.path.exists(azure_secret.json):
        #     with open('azure_secret.json') as f:
        #     secret = json.load(f)
        #     subscription_key = secret["subscription_key"]
        #     endpoint = secret["endpoint"]
        # クライアント認証
        self.computervision_client = ComputerVisionClient(
            endpoint, CognitiveServicesCredentials(subscription_key))

    images_folder = "./resources"
    read_image_path = os.path.join(images_folder, "japaneseText1rotate90.jpg")

    def send_ocr_request(self, read_image_path) -> str:
        with open(read_image_path, "rb") as read_image:
            read_response = self.computervision_client.read_in_stream(
                read_image, raw=True)
            read_operation_location = read_response.headers["Operation-Location"]
            operation_id = read_operation_location.split("/")[-1]
            return operation_id

    def wait_response(self, operation_id: str, sleep_time=10) -> _models_py3.ReadOperationResult:
        while True:
            read_result = self.computervision_client.get_read_result(
                operation_id)
            if read_result.status.lower() not in ['notstarted', 'running']:
                return read_result
            print('Waiting for result...')
            time.sleep(sleep_time)

    def print_ocr_result(self, read_result):
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    print(line.text)
                    print(line.bounding_box)

    def get_ocr_results(self, read_result) -> _models_py3.ReadResult:
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                return text_result

    # operation_id = send_ocr_request(computervision_client, read_image_path)
    # read_result = wait_response(computervision_client, operation_id)
    # print_ocr_result(read_result)
