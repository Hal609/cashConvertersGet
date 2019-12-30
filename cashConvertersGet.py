import requests, bs4, time

def loadPage(shopName, page):
    #Get page of products for a location
    res = requests.get('https://www.cashconverters.co.uk/' + shopName + '/products?page=' + str(page))
    res.raise_for_status()

    return(bs4.BeautifulSoup(res.text, features="lxml")) #Return page HTML as BeautifulSoup variable


def pageCount(shopName):
    ccSoup = loadPage(shopName, 1)

    #Find the number of restuls and thus the number of pages to check
    numResults = ccSoup.select('p em')[1].getText() #Grabs second <em> element within a <p> element
    return(int(int(numResults)/9 + 1)) #Claculates number of pages at 9 items per page

def loadProducts(shopName):
    products.clear() #Removes previous shops products from list

    with open(outputFile, "a") as out: #Write shop name as tiltle
        out.write("\n\n" + shopName + "\n" + "="*len(shopName) + "\n")

    numPages = pageCount(shopName) #Find the number of pages of products
    numPages = 5

    for i in range(numPages): #Loop trough all pages
        ccSoup = loadPage(shopName, i) #Load each page
        divElems = ccSoup.select('div') #Select div elements

        for j in range(len(divElems)): #Check each <div> elem to see if it is a product
            if divElems[j].get("class") == ['panel', 'panel-default', 'product-panel']:
                products.append(divElems[j])

def productSearch(*searchTerms):
    found = []
    entry = ()
    results = []

    with open(outputFile, "a") as out:
        out.write("{0:60.60}    {1:6}     {2:100} \n\n".format("Item", "Price", "URL"))

    for id in range(len(products)):
        cat = products[id]["data-category"].lower()
        name = products[id]["data-name"].lower()


        for search in searchTerms:

            if search[0] == "-": #If negative search term
                search = search[1:] #Remove negative
                if search in cat or search in name: #search for term
                    if id in found:
                        found.remove(id) #Remove matching terms from results
            elif search in cat or search in name:
                if id not in found:
                    found.append(id) #Add matching terms to results

    for id in found:
        entry = (float(products[id]["data-price"]), id)
        results.append(entry)

    print(results)
    results.sort()
    print(results)

    for prod in results:
        id = prod[1]
        result = "{0:60.60}:   {1:>6.6}     {2:100}".format(products[id]["data-name"].title(), products[id]["data-price"].title(), products[id].find_all("a")[0].get("href"))
        with open(outputFile, "a") as out:
            out.write(result + "\n")

products = []
outputFile = "/home/hal/Documents/PythonScripts/cashConverters/Output.txt"

with open(outputFile, "w") as out:
    out.write("╔═╗┌─┐┌─┐┬ ┬╔═╗┌─┐┬  ┬┌─┐┬─┐┌┬┐┌─┐┬─┐┌─┐╔╦╗┌─┐┌─┐┬\n║  ├─┤└─┐├─┤║  │ │└┐┌┘├┤ ├┬┘ │ ├┤ ├┬┘└─┐ ║ │ ││ ││\n╚═╝┴ ┴└─┘┴ ┴╚═╝└─┘ └┘ └─┘┴└─ ┴ └─┘┴└─└─┘ ╩ └─┘└─┘┴─┘\n")

#shops = ["Sheffield-Gleadless-Road", "Sheffield-Hillsborough", "Preston", "Blackpool-Church-Street", "Blackpool-South-Shore"]
shops = ["Blackpool-Church-Street"]

for shop in shops:
    initTime = time.time()
    loadProducts(shop)
    print("Prod load time:", (time.time() - initTime))
    initTime = time.time()
    #productSearch("guitar", "instrument", "-junior", "-kid", "-child", "-1/2", "-3/4", "-amp", "-amplifier", "-tuner", "-pedal")
    productSearch("ring")
    print("Search time:", (time.time() - initTime))
