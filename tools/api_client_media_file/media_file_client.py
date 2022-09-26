
import requests
import argparse

parser = argparse.ArgumentParser(description='Send media file (video) to the backend identify motorcycles.')
parser.add_argument('--path', type=str, required=True)
parser.add_argument('--host', type=str, required=False, default='http://localhost:8080/media')
args = parser.parse_args()


with open(args.path, "rb") as a_file:
    file_dict = {'file': a_file}
    response = requests.post(args.host, files=file_dict)
    print(response.text)