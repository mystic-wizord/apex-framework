# app.py
from flask import Flask, request, jsonify
import subprocess
import re
import datetime
import time

app = Flask(__name__)

valid_endpoints = [
    {
        'name': 'service-a',
        'endpoint-pattern': "^test\-a$",
        'url': 'http://127.0.0.1:8080/'
    },
    {
        'name': 'service-b',
        'endpoint-pattern': "^test\-b$",
        'url': 'http://127.0.0.1:8081/'
    } ,
    {
        'name': 'service-c',
        'endpoint-pattern': "^test\-c$",
        'url': 'http://127.0.0.1:8082/'
    } ,
    {
        'name': 'service-a',
        'endpoint-pattern': "^test\-a/[0-9]+$",
        'url': 'http://127.0.0.1:8080/'
    } 
]

def timeit(f):

    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print(f'Executed {f.__name__} in: {(te-ts) * 1000} milliseconds')
        return result

    return timed

@app.route('/<path:endpoint_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def get_path(endpoint_path):
    print('New request received. Scraping REST call and rerouting...')

    api_details = get_downstream_api_details(endpoint_path)

    if api_details is not None: 
        if 'Authorization' in request.headers:
            print(f'{request.headers}')

        print(f'Rerouting request: {request.method} {api_details + endpoint_path}')
        
        # subprocess.call('/media/wizord/cleopatra/repositories/bash-scripts/audio/audio-stream.sh')
        return f'Endpoint read: {endpoint_path}'
        
    else:
        return 'Not Found!', 404

@timeit
def get_downstream_api_details(endpoint_path):
    for valid_endpoint in valid_endpoints:
        matches = re.search(valid_endpoint['endpoint-pattern'], endpoint_path)
        if matches is not None:
            print('Match found for endpoint')
            return valid_endpoint['url']
        else:
            print('No match found for endpoint')

    return None

@app.route('/info', methods=['GET'])
def get_api_info():
    return 'info'