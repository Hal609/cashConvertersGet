import requests, bs4

shopName = "Blackpool-Church-Street"
page = "1"

res = requests.get('https://www.cashconverters.co.uk/' + shopName + '/products?page=' + page)
res.raise_for_status()

ccSoup = bs4.BeautifulSoup(res.text, features="lxml")

numResults = ccSoup.select('p em')[1].getText()
numPages = int(numResults)/9 + 1

#divElems = ccSoup.select('div')

products = []

numPages = 1

for i in range(numPages):
    res = requests.get('https://www.cashconverters.co.uk/' + shopName + '/products?page=' + str(i))
    res.raise_for_status()

    ccSoup = bs4.BeautifulSoup(res.text, features="lxml")

    divElems = ccSoup.select('div')

    for j in range(len(divElems)):
        if divElems[j].get("class") == ['panel', 'panel-default', 'product-panel']:
            products.append(divElems[j])

print(products[1]["data-name"])
