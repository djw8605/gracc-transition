import requests
from elasticsearch import Elasticsearch



UPLOADDEST = "https://..."

def main():
    client = Elasticsearch()
    r=client.indices.stats(metric='docs,store')
    token = ""
    with open("token.txt", 'r') as token_file:
        token = token_file.read()
    
    requests.post(UPLOADDEST, r['indices'])


if __name__ == "__main__":
    main()

