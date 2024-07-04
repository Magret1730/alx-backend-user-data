#!/usr/bin/env python3
"""Copy files"""
from sys import argv
import requests

URL = 'https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2019/11/a2e00974ce6b41460425.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240703%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240703T162329Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=6b924a25a11f93c1d9a3e94853c96baaea10b7f65aef3a396a32fa9da890783c'

try:
    response = requests.get(URL)
    response.raise_for_status()
    content = response.text

    with open('user_data.csv', 'w', encoding='utf-8') as dest:
        dest.write(content)

    print('Copied completed')
except Exception as e:
     print(f"An error occurred: {e}")
