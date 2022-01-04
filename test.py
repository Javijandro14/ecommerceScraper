from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import gc
import time

def play():
    exec(open("test.py").read())
    
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
    level1 = {}
    if not res1:#Si no tiene categorias, buscara paginacion y articulos
        pass
        #level1 = {}
        #pag = getProdInfo(soup,store,"pag")
        #for p in pag: #Lista links en la categorias
            #soup = getUrl(p)
            #res1 = getProdInfo(soup,store,"prod")
            # if not res1: 
            #     print("no hay productos en " + p)
            # for r1 in res1:
            #     name1 = getProdInfo(r1,store,"name")
            #     link1 = getProdInfo(r1,store,"linkProd")
            #    level1[name1] = link1
    else: # Si tiene categorias, buscara subcategorias
        for r1 in res1:
            name1 = getProdInfo(r1,store,"name").replace(" ","-")
            link1 = getProdInfo(r1,store,"linkCat")
            level1[name1]=link1
        #   soup = getUrl(link1)
        #         res2 = getProdInfo(soup,store,"cat")
        #         if not res2:

        #             res2 = getProdInfo(soup,store,"prod")
        #             if not res2:
        #                 print("No hay productos en: " + link1)
        #             else:
        #                 level2 = {}
        #                 for r2 in res2:
        #                     name2 = getProdInfo(r2,store,"name")
        #                     link2 = getProdInfo(r2,store,"linkProd")
        #                     level2[name2] = link2
        #             level1[name1] = level2
        #         else:
        #             level2 = {}
        #             for r2 in res2:
        #                 name2 = getProdInfo(r2,store,"name")
        #                 link2 = getProdInfo(r2,store,"linkProd")
        #                 soup = getUrl(link2)
        #                 res3 = getProdInfo(soup,store,"cat")
        #                 if not res3:
        #                     level3 = {}
        #                     res3 = getProdInfo(soup,store,"item")
        #                     if not res3:
        #                         print("No hay productos en: " + link2)
        #                     else:
        #                         for r3 in res3:
        #                             name3 = getProdInfo(r3,store,"name")
        #                             link3 = getProdInfo(r3,store,"linkProd")
        #                             level3[name3] = link3
        #                     level2[name2] = level3    
        #                 else:
        #                     level3 = {}
        #                     for r3 in res3:
        #                         name3 = getProdInfo(r3,store,"name")
        #                         link3 = getProdInfo(r3,store,"linkProd")
        #                         soup = getUrl(link3)
        #                         res4 = getProdInfo(soup,store,"item")
        #                         if not res4:
        #                             print("No hay productos en: " + link3)
        #                         else:
        #                             level4 = {}
        #                             for r4 in res4:
        #                                 name4 = getProdInfo(r4,store,"name")
        #                                 link4 = getProdInfo(r4,store,"linkProd")
        #                                 level4[name4] = link4
        #                             level3[name3] = level4
        #                     level2[name2] = level3
        #         level1[name1] = level2
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
            name = findItem(soup,'div','class','image-area').get('title')
            return name
        elif "linkCat" in item:
            link = base+ "/" + soup.get('href')
            return link
        elif "linkProd" in item:
            link = base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
            return link
        elif "pag" in item:
            pagination = []
            link = base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
            pagination.append(link)
            return pagination
    elif "Max" == store:
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
        elif "pag" in item:
            noProductos = int((findItem(soup,'span','class','toolbar-number').text)[:-10])
            paginas = 0
            if noProductos >= 30:
                paginas = noProductos//30
            else:
                paginas = 0
            if (noProductos % 30) >= 1:
                paginas += 1
            pag = ["?p=" + format(iter) + "&product_list_limit=30" for iter in range(1,paginas+1)]
            return pag
    elif "Goat" == store:
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
        elif "pag" in item:
            link = base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
            return link
    elif "Elektra" == store:
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
        elif "pag" in item:
            link = base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
            return link
    elif "Click" == store:
        if "cat" in item:
            lists = []
            menu = findItem(soup,'ul','class',['justify-content-center','container','d-flex','align-items-center','mb-0','mt-0','pr-4'])
            lists = findItems(menu,'li','class','nav-item')
            for l in lists:
                name = l.a.get('href')
                if name == None:
                    name = l.a.text.strip("(current)",).lower().replace("ó","o")
                    ul = findItem(soup,'div','aria-labelledby',name)
                    listar = findItems(ul,'li',None,None)
                    lists.extend(listar)
            return lists
        elif "prod" in item:
            items = findItems(soup,'div','class','zoom_info')
            return items
        elif "name" in item:
            name = soup.a.get('href')
            if name == None:
                name = soup.a.text.strip("(current)",).lower().replace("ó","o")
                ul = findItem(soup,'div','aria-labelledby',name)
                listar = findItems(ul,'li',None,None)
                for l in listar:
                    return l.a.get('href').replace("/productos/","")
            else:
                return name.replace("/productos/","")
        elif "linkCat" in item:
            link = soup.a.get('href')
            if link == None:
                name = soup.a.text.strip("(current)",).lower().replace("ó","o")
                ul = findItem(soup,'div','aria-labelledby',name)
                listar = findItems(ul,'li',None,None)
                level = {}
                for l in listar:
                    linkl = base + l.a.get('href')
                    return linkl
            return base + link
        elif "linkProd" in item:
            link = base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
            return link
        elif "pag" in item:
            links = []
            return links
    elif "Spirit" == store:
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
        elif "pag" in item:
            link = base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
            return link
    elif "Macro" == store:
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
        elif "pag" in item:
            link = base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
            return link
    elif "Funky" == store:        
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
        elif "pag" in item:
            link = base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
            return link


opcion = int(input("Ingrese una Opcion que desee ver: \n1.Intelaf \n2.Click \n"))

if opcion == 1:
    #Intelaf
    url = "https://www.intelaf.com/js/menu_productos22112021091955.json"
    base = "https://www.intelaf.com"
    res = getUrl(url)
    data = json.loads(res.text)
    menu = data['menu_sub_1s']
    categorias = {}
    for info in menu:
        area = info['Area']
        url = info['url']
        categorias[area.replace(" ","-")]= getCategorias(base + url, "Intelaf")
    print(categorias)
    # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/intelaf/intelafJson.json",'w') as file:
    #     json.dump(categorias,file)
    # file.close()
elif opcion == 2:
    #Click
    base = "https://www.click.gt"
    categorias = getCategorias(base,"Click")
    print(categorias)

