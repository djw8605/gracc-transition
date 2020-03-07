from __future__ import print_function

import requests
import json
from elasticsearch import Elasticsearch



UPLOADDEST = "https://gracc-transition.herokuapp.com/upload/gracc.opensciencegrid.org/"

def main():
    client = Elasticsearch(timeout=60)
    r=client.indices.stats(metric='docs,store')
    token = ""
    with open("token.txt", 'r') as token_file:
        token = token_file.read()
    
    headers = {"Authorization": "Bearer {}".format(token.strip())}
    print(json.dumps(r['indices']))
    
    print(requests.post(UPLOADDEST, json=json.dumps(r['indices']), headers=headers))


if __name__ == "__main__":
    main()

