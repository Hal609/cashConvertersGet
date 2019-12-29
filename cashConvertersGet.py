import requests, bs4

def loadPage(shopName, page):
    #Get page of products for a location
    res = requests.get('https://www.cashconverters.co.uk/' + shopName + '/products?page=' + str(page))
    res.raise_for_status()

    return(bs4.BeautifulSoup(res.text, features="lxml")) #Return page HTML as BeautifulSoup variable

    #return(ccSoup.select('div')) #Selct <div> elements

def pageCount(shopName):
    ccSoup = loadPage(shopName, 1)

    #Find the number of restuls and thus the number of pages to check
    numResults = ccSoup.select('p em')[1].getText() #Grabs second <em> element within a <p> element
    return(int(numResults)/9 + 1) #Claculates number of pages at 9 items per page

def loadProducts(shopName):
    numPages = pageCount(shopName)
    numPages = 5

    for i in range(numPages): #Loop trough all pages
        ccSoup = loadPage(shopName, i) #Load each page
        divElems = ccSoup.select('div') #Select div elements

        for j in range(len(divElems)): #Check each <div> elem to see if it is a product
            if divElems[j].get("class") == ['panel', 'panel-default', 'product-panel']:
                products.append(divElems[j])

def productSearch(searchTerm, *secondTerm):
    for i in range(len(products)):
        cat = products[i]["data-category"].lower()
        name = products[i]["data-name"].lower()
        if searchTerm in cat or searchTerm in name:
            print("{0:70.70}:   {1:5}".format(products[i]["data-name"].title().encode("utf-8"), products[i]["data-price"].title().encode("utf-8")))
            print(products[i].find_all("a")[0].get("href"))


#init variables
#shopName = "Blackpool-Church-Street"
page = "1"
products = []

#numPages = pageCount(shopName)
#numPages = 5 #Temporarily overwrite number of pages to one to save time when debugging

loadProducts("Blackpool-Church-Street")

productSearch("guitar")
productSearch("tv")


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

'''
for i in range(len(products)):
    print("{0:70.70}:   {1:5}".format(products[i]["data-name"].title().encode("utf-8"), products[i]["data-price"].title().encode("utf-8")))
'''
