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
    return(int(int(numResults)/9 + 1)) #Claculates number of pages at 9 items per page

def loadProducts(shopName):
    products.clear()

    print("\n" + shopName + "\n" + "="*len(shopName) + "\n")

    numPages = pageCount(shopName)

    for i in range(numPages): #Loop trough all pages
        ccSoup = loadPage(shopName, i) #Load each page
        divElems = ccSoup.select('div') #Select div elements

        for j in range(len(divElems)): #Check each <div> elem to see if it is a product
            if divElems[j].get("class") == ['panel', 'panel-default', 'product-panel']:
                products.append(divElems[j])

def productSearch(*searchTerms):
    found = []

    print("{0:60.60}    {1:5}     {2:100} \n".format("Item", "Price", "URL"))

    for id in range(len(products)):
        cat = products[id]["data-category"].lower()
        name = products[id]["data-name"].lower()

        for search in searchTerms:

            if search[0] == "-": #If negative search term
                search = search[1:]
                if search in cat or search in name:
                    if id in found:
                        found.remove(id)
            elif search in cat or search in name:
                if id not in found:
                    found.append(id)
    for id in found:
        print("{0:60.60}:   {1:5.5}     {2:100}".format(products[id]["data-name"].title(), products[id]["data-price"].title(), products[id].find_all("a")[0].get("href")))

products = []

shops = ["Sheffield-Gleadless-Road", "Sheffield-Hillsborough", "Preston", "Blackpool-Church-Street", "Blackpool-South-Shore"]

for shop in shops:
    loadProducts(shop)
    productSearch("guitar", "-amp", "-amplifier", "-tuner")


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
