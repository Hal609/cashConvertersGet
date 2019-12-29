import requests, bs4

#init variables
shopName = "Blackpool-Church-Street"
page = "1"

#get first page of products for a location
res = requests.get('https://www.cashconverters.co.uk/' + shopName + '/products?page=' + page)
res.raise_for_status()

#Load page HTML to BeautifulSoup variable
ccSoup = bs4.BeautifulSoup(res.text, features="lxml")

#Find the number of restuls and thus the number of pages to check
numResults = ccSoup.select('p em')[1].getText() #Grabs second <em> element within a <p> element
numPages = int(numResults)/9 + 1 #Claculates number of pages at 9 items per page

#divElems = ccSoup.select('div')

products = [] #Initialises products list

#numPages = 1 #Temporarily overwrite number of pages to one to save time when debugging

for i in range(numPages): #Loop trough all pages of restuls
    res = requests.get('https://www.cashconverters.co.uk/' + shopName + '/products?page=' + str(i))
    res.raise_for_status()

    ccSoup = bs4.BeautifulSoup(res.text, features="lxml")

    divElems = ccSoup.select('div') #Selct <div> elements

    for j in range(len(divElems)): #Check each <div> elem to see if it is a product
        if divElems[j].get("class") == ['panel', 'panel-default', 'product-panel']:
            products.append(divElems[j])

'''
Product Info
============
Barcode == "data-barcode"
Brand == "data-brand"
Category == "data-category"
Name == "data-name"
Price == "data-price"
href == "href"
'''
for i in range(len(products)):
    print("{0:70.70}:   {1:5}".format(products[i]["data-name"].title().encode("utf-8"), products[i]["data-price"].title().encode("utf-8")))
