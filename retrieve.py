import requests
import shutil
import csv

indexItem = 0;

def download_image(_data_):
    _img_ = requests.get(_data_['meta']['content'][0]['url'], stream=True)
    _tok_ = _data_['id']
    _path_ = 'D:/Github/Capstone/nft-backend/Example/' + str(indexItem) + '.png'
    with open(_path_, 'wb') as f:
        _img_.raw.decode_content = True
        shutil.copyfileobj(_img_.raw, f)
    return [_tok_, _path_]


def get_rarible(_cont_ = ""):
    _address_ = {}
    print(_cont_)
    _req_ = requests.get('https://api.rarible.org/v0.1/items/byCollection', timeout=100,
    params={
        'collection': 'ETHEREUM:0x4b61413d4392c806e6d0ff5ee91e6073c21d6430',
        'continuation': _cont_
        })
    if _req_.status_code == 200:
        _jfile_ = _req_.json()
        if "continuation" not in _jfile_:
            return
        _ncont_ = _jfile_["continuation"]
        _result_ = _jfile_["items"]
        for __it in  _result_:
            _item_ = download_image(__it)
            _address_[_item_[0]] = _item_[1]
        if not _ncont_ == _cont_:
            _add_ = get_rarible(_ncont_)
            if _add_ == None:
              if _address_ == None:
                return {}
              return _address_
            if _address_ == None:
              return _add_
            return {**_address_, **_add_}
        return _address_
    else:
        print("error network")
        return get_rarible(_cont_)

print('done crawling')

AddressBook = get_rarible()
with open('dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in AddressBook.items():
       writer.writerow([key, value])
