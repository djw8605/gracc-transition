import requests
from elasticsearch import Elasticsearch



UPLOADDEST = "https://..."

def main():
    client = Elasticsearch()
    r=client.indices.stats(metric='docs,store')
    token = ""
    with open("token.txt", 'r') as token_file:
        token = token_file.read()
    
    headers = {"Authorization": "Bearer {}".format(token)}
    
    print(requests.post(UPLOADDEST, r['indices']), headers = headers)


if __name__ == "__main__":
    main()

