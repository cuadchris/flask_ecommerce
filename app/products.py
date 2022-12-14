import requests as r
import random

def getProduct(id):
    url = f'https://dummyjson.com/products/{id}'
    response = r.get(url)
    if not response.ok:
        return False
    data = response.json()
    product = {
        'id': data['id'],
        'title': data['title'].capitalize(),
        'description': data['description'],
        'price': data['price'],
        'rating': data['rating'],
        'image': data['thumbnail']
    }
    return product

def get5RandomProducts():
    ids = []
    products = []
    while len(ids) < 5:
        num = random.randrange(1, 99)
        if num not in ids:
            ids.append(num)
    for id in ids:
        products.append(getProduct(id))

    return products

def getCategory(category):
    url = f'https://dummyjson.com/products/category/{category}'
    response = r.get(url)
    if not response.ok:
        return False
    res = response.json()
    data = res['products']
    return data
