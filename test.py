from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import gc
import time


def getUrl(url):
    try:
        send = requests.get(url)
        time.sleep(1)
    except:
        print("Revise el url, no se proceso correctamente")
        print("Url Fallido:" + url)
    else:
        soup = BeautifulSoup(send.text, 'html.parser')
        return soup

def findItem(soup, item, attType, attName):
    try:
        result = soup.find(item, {attType: attName})
    except:
        print("error en la funcion 'findItem'")
        print("Item Fallido: " + format(item) + " Tipo de Atributo: " + format(attType) + " Nombre del Atributo: " +format(attName))
    else:
        return result

def findItems(soup, item, attType, attName):
    try:
        result = soup.find_all(item, {attType: attName})
    except:
        print("error en la funcion 'findItems'")
        print("Item Fallido: " + format(item) + " Tipo de Atributo: " + format(attType) + " Nombre del Atributo: " +format(attName))
    else:
        return result

def getCategorias(link,store):
    level0 = {}
    soup = getUrl(link)
    res1 = getProdInfo(soup,store,"cat")
    if not res1:
        res1 = getProdInfo(soup,store,"prod")
        if not res1:
            print("no hay productos en " + link)
        level1 = {}
        for r1 in res1:
            name1 = getProdInfo(r1,store,"name")
            link1 = getProdInfo(r1,store,"linkProd")
            level1[name1] = link1
    else:
        level1 = {}
        for r1 in res1:
            name1 = getProdInfo(r1,store,"cat")
            link1 = getProdInfo(r1,store,"linkCat")
            soup = getUrl(link1)
            res2 = getProdInfo(soup,store,"cat")
            if not res2:
                res2 = getProdInfo(soup,store,"prod")
                if not res2:
                    print("No hay productos en: " + link1)
                else:
                    level2 = {}
                    for r2 in res2:
                        name2 = getProdInfo(r2,store,"name")
                        link2 = getProdInfo(r2,store,"linkProd")
                        level2[name2] = link2
                level1[name1] = level2
            else:
                level2 = {}
                for r2 in res2:
                    name2 = getProdInfo(r2,store,"name")
                    link2 = getProdInfo(r2,store,"linkProd")
                    soup = getUrl(link2)
                    res3 = getProdInfo(soup,store,"cat")
                    if not res3:
                        level3 = {}
                        res3 = getProdInfo(soup,store,"item")
                        if not res3:
                            print("No hay productos en: " + link2)
                        else:
                            for r3 in res3:
                                name3 = getProdInfo(r3,store,"name")
                                link3 = getProdInfo(r3,store,"linkProd")
                                level3[name3] = link3
                        level2[name2] = level3    
                    else:
                        level3 = {}
                        for r3 in res3:
                            #print(r3.text)
                            link = base + "/" + r3.get('href')
                            soup = getUrl(link)
                            res4 = getProdInfo(soup,store,"item")
                            if not res4:
                                print("No hay productos en: " + r3.get('href'))
                            else:
                                level4 = {}
                                for r4 in res4:
                                    nombre = (findItem(r4,'button','class','btn_cotiza')).get('name')
                                    link = base + "/" + (findItem(r4,'button','class','btn_mas_info')).get('name')
                                    level4[nombre] = link
                                level3[r3.text] = level4
                        level2[r2.text] = level3
            level1[name1] = level2
    level0 = level1  
    return level0

def getProdInfo(soup,store,item):
    if "Intelaf" in store:
        if "cat" in item:
            menu = findItems(soup,'a','class','hover_effect')
            if menu == None:
                menu = findItem(soup,'div','class','image-area').get('title')
            return menu
        elif "prod" in item:
            items = findItems(soup,'div','class','zoom_info')
            return items
        elif "name" in item:
            name = findItem(soup,'button','class','btn_cotiza').get('name')
            return name
        elif "linkCat" in item:
            link = base+ "/" + soup.get('href')
            return link
        elif "linkProd" in item:
            link = base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
            return link



#Getting Json file
url = "https://www.intelaf.com/js/menu_productos22112021091955.json"
base = "https://www.intelaf.com"
res = getUrl(url)
data = json.loads(res.text)
menu = data['menu_sub_1s']
categorias = {}
for info in menu:
    area = info['Area']
    url = info['url']
    categorias['Area']= getCategorias(base + url, "Intelaf")


        # #Se imprime 2 archivos, uno de texto y otro JSON, solo es de preuba el de txt, para ver que si nos sale el resultado deseado, la que nos importa seria JSON
        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/intelaf/intelafJson.json",'w') as file:
        #     json.dump(level0,file)
        # file.close()
        #Cerramos este fragmento de codigo porque lo queremos volver como funcion si es posible, porque queremos dar la opcion de solo analizar los links
        #y de ponerlo en un archivo por separado y no tener que consultar cada vez que se entra a la pagina