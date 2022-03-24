import requests

#get data from API
res = requests.get('https://api.rarible.org/v0.1/items/byCollection', 
    params={
        'collection': 'ETHEREUM:0x4b61413d4392c806e6d0ff5ee91e6073c21d6430'
        })