import requests

def add(keyword, api_url = 'http://127.0.0.1:8000/api/products/'):
    data = {'keyword': keyword}
    add_resp = requests.post(api_url, json=data)

    print(add_resp.status_code)

def show(api_url = 'http://127.0.0.1:8000/api/products/'):
    detail_resp = requests.get(api_url)

    if detail_resp.status_code == 200:
        data = detail_resp.json()
        print(data)
    else:
        print('Failed')

def delete(keyword, api_url = 'http://127.0.0.1:8000/api/products/'):
    url = f'{api_url}{keyword}/'
    del_resp = requests.delete(url)
    print(del_resp.status_code)

def find(keyword, store, api_url = 'http://127.0.0.1:8000/api/products_detail/'):
    url = f'{api_url}{store}/{keyword}/'
    find_resp = requests.get(url)

    if find_resp.status_code == 200:
        data = find_resp.json()
        print(data)
    else:
        print('Failed')


add('體重計')

# show()

# find('keyword', 'store')

# delete('關鍵字2')