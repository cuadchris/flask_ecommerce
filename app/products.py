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
        'title': data['title'],
        'description': data['description'],
        'price': data['price'],
        'rating': data['rating'],
        'image': data['images'][0]
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