from __future__ import print_function

import requests
import json
import sys
from elasticsearch import Elasticsearch



UPLOADDEST = "https://gracc-transition.herokuapp.com/upload/{}/"

def main():
    host = sys.argv[1]
    client = Elasticsearch(timeout=60)
    r=client.indices.stats(metric='docs,store')
    token = ""
    with open("token.txt", 'r') as token_file:
        token = token_file.read()
    
    headers = {"Authorization": "Bearer {}".format(token.strip())}
    
    print(requests.post(UPLOADDEST.format(host), json=json.dumps(r['indices']), headers=headers))


if __name__ == "__main__":
    main()

