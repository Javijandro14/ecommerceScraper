from os import set_inheritable
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
    level1 = {}
    if not res1:#Si no tiene categorias, buscara paginacion y articulos
        pag = getProdInfo(link,store,"pag")
        for p in pag: #Lista links en la categorias
            soup = getUrl(p)
            res1 = getProdInfo(soup,store,"prod")
            if not res1: 
                print("no hay productos en " + p)
            else:
                for r1 in res1:
                    name1 = getProdInfo(r1,store,"nameProd")
                    link1 = getProdInfo(r1,store,"linkProd")
                    level1[name1] = link1
    else: # Si tiene categorias, buscara subcategorias
        for r1 in res1:
            name1 = getProdInfo(r1,store,"name").replace(" ","-")
            link1 = getProdInfo(r1,store,"linkCat")
            #level1[name1]=link1
            soup = getUrl(link1)
            res2 = getProdInfo(soup,store,"cat")
            level2 = {}
            if not res2 or res2 == res1:#Si no hay SubCategorias, buscara productos
                pag = getProdInfo(link1,store,"pag")
                for p in pag: #Lista links en la categorias
                    soup = getUrl(p)
                    res2 = getProdInfo(soup,store,"prod")
                    if not res2: 
                        print("no hay productos en " + p)
                    else:
                        for r2 in res2:
                            name2 = getProdInfo(r2,store,"nameProd")
                            link2 = getProdInfo(r2,store,"linkProd")
                            level2[name2] = link2
            else: #Si hay SubCategorias, buscara subcategorias dentro de si mismos
                for r2 in res2:
                    name2 = getProdInfo(r2,store,"name").replace(" ","-")
                    link2 = getProdInfo(r2,store,"linkCat")
                    soup = getUrl(link2)
                    res3 = getProdInfo(soup,store,"cat")
                    level3 = {}
                    if not res3 or res2 == res3: #Si no hay Sub-SubCategorias, buscara productos
                        pag = getProdInfo(link2,store,"pag")
                        for p in pag: #Lista links en la categorias
                            soup = getUrl(p)
                            res3 = getProdInfo(soup,store,"prod")
                            if not res3:
                                print("No hay productos en: " + p)
                            else:
                                for r3 in res3:
                                    name3 = getProdInfo(r3,store,"nameProd")
                                    link3 = getProdInfo(r3,store,"linkProd")
                                    level3[name3] = link3
                    else: #Si hay Sub-SubCategorias, se buscara dentro de si mismo mas SubCategorias
                        level3 = {}
                        for r3 in res3:
                            name3 = getProdInfo(r3,store,"name").replace(" ","-")
                            link3 = getProdInfo(r3,store,"linkCat")
                            soup = getUrl(link3)
                            res4 = getProdInfo(soup,store,"cat")
                            level4 = {}
                            if not res4 or res3 == res4:
                                pag = getProdInfo(link3,store,"pag")
                                for p in pag: #Lista links en la categorias
                                    soup = getUrl(p)    
                                    res4 = getProdInfo(soup,store,"prod")
                                    if not res4:
                                        print("No hay productos en: " + p)
                                    else:
                                        for r4 in res4:
                                            name4 = getProdInfo(r4,store,"nameProd")
                                            link4 = getProdInfo(r4,store,"linkProd")
                                            level4[name4] = link4
                            else:
                                for r4 in res4:
                                    name4 = getProdInfo(r4,store,"name").replace(" ","-")
                                    link4 = getProdInfo(r4,store,"linkCat")
                                    soup = getUrl(link4)
                                    #Ultimo nivel, si hay mas subcategorias, se deberia implementar mas codigo para que se busque lo que necesitamos
                                    res5 = getProdInfo(soup,store,"cat")
                                    level5 = {}
                                    if not res5 or res5 == res4:
                                        pag = getProdInfo(link4,store,"pag")
                                        for p in pag: #Lista links en la categorias
                                            soup = getUrl(p)
                                            res5 = getProdInfo(soup,store,"prod")
                                            if not res5:
                                                print("No hay productos en: " + p)
                                            else:
                                                for r5 in res5:
                                                    name5 = getProdInfo(r5,store,"nameProd")
                                                    link5 = getProdInfo(r5,store,"linkProd")
                                                    level5[name5] = link5
                                    else:
                                        print("No se puede ir mas a fondo")
                                        break
                                    level4[name4] = level5
                            level3[name3] = level4
                    level2[name2] = level3
            level1[name1] = level2
    level0 = level1  
    return level0

def getProdInfo(soup,store,item):
    if "Intelaf" in store:
        if item == "cat":
            cat = findItems(soup,'a','class','hover_effect')
            
            return cat
        elif item == "prod":
            return findItems(soup,'div','class','zoom_info')
        elif item == "name":
            name = (findItem(soup,'div','class','image-area'))
            if name == None:
                name = soup.text
                return name
            else:
                return name.get('title')
        elif item == "linkCat":
            link = base+ "/" + soup.get('href')
            return link
        elif item == "nameProd":
            return (findItem(soup,'button','class','btn_cotiza')).get('name')
        elif item == "linkProd":
            return base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
        elif item == "pag":
            return [soup]
    elif "Max" == store:
        if item == "cat":
            subcategorias = findItem(soup,'ul','class',['sub-cat-list' ,'slick-initialized' ,'slick-slider'])
            if subcategorias != None:
                list = findItems(subcategorias,'li',None,None)
                categorias = [i.a for i in list]
            else:
                menu = findItem(soup,'div','class','content-mega')
                cat = findItems(menu,'li','class','level2')
                categorias = [c.a for c in cat]
            return categorias
        elif item == "prod":
            container = findItem(soup,'ol','class',['products','list','items','product-items'])
            products = findItems(container,'a','class','product-item-link')
            return products
        elif item == "name":
            print(soup.text.strip())
            return soup.text.strip()
        elif item == "linkCat":
            return soup.get('href')
        elif item == "nameProd":
            return soup.text.strip()
        elif item == "linkProd":
            return soup.get('href')
        elif item == "pag":
            links = []
            souptemp = getUrl(soup)
            num = findItem(souptemp,'span','class','toolbar-number')
            if num != None:
                noProductos = int(num.text.replace("Productos"," ").replace("Producto"," "))
                paginas = 0
                if noProductos >= 30:
                    paginas = noProductos//30
                else:
                    paginas = 0
                if (noProductos % 30) >= 1:
                    paginas += 1
                for iter in range(1,paginas+1):
                    links.append(format(soup+"?p=" + format(iter) + "&product_list_limit=30"))
                return links
            else:
                return [soup]
    elif "Goat" == store:
        if item == "cat":
            pass
        elif item == "prod":
            pass
        elif item == "name":
            pass
        elif item == "linkCat":
            pass
        elif item == "nameProd":
            pass
        elif item == "linkProd":
            pass
        elif item == "pag":
            pass
    elif "Elektra" == store:
        if item == "cat":
            pass
        elif item == "prod":
            pass
        elif item == "name":
            pass
        elif item == "linkCat":
            pass
        elif item == "nameProd":
            pass
        elif item == "linkProd":
            pass
        elif item == "pag":
            pass
    elif "Click" == store:
        if item == "cat":
            pass
        elif item == "prod":
            pass
        elif item == "name":
            pass
        elif item == "linkCat":
            pass
        elif item == "nameProd":
            pass
        elif item == "linkProd":
            pass
        elif item == "pag":
            pass
    elif "Spirit" == store:
        if item == "cat":
            pass
        elif item == "prod":
            pass
        elif item == "name":
            pass
        elif item == "linkCat":
            pass
        elif item == "nameProd":
            pass
        elif item == "linkProd":
            pass
        elif item == "pag":
            pass
    elif "Macro" == store:
        if item == "cat":
            subcategorias = findItem(soup,'ul','class',['nav','menu-left','mod-list'])
            if subcategorias != None:
                categorias = findItems(subcategorias,'a',None,None)
            else:
                menu = findItem(soup,'ul','id','menu_footer')
                categorias = findItems(menu,'a',None,None)
            return categorias
        elif item == "prod":
            productos = findItems(soup,'div','class','product-inner')
            return productos
        elif item == "name":
            name = soup.text
            return name
        elif item == "linkCat":
            link = base + format(soup.get('href'))
            return link
        elif item == "nameProd":
            name = findItem(soup,'a','class','item-title')
            return name.text.strip()
        elif item == "linkProd":
            link = base + findItem(soup,'a','class','item-title').get('href')
            return link
        elif item == "pag":
            tempsoup = getUrl(soup)
            divpag = findItem(tempsoup,'div','class','vm-pagination')
            if divpag == None:
                numeroPag = 1
            else:
                paginacion = findItem(divpag,'span','class','vm-page-counter')
                if paginacion.text=="":
                    numeroPag = 1
                else:
                    numeroPag = int(paginacion.text[-2:])
            links = []
            for pag in range(1,(numeroPag+1)):
                if pag == 1:
                    links.append(format(soup)+"?start=0")
                elif pag >1:
                    links.append(format(soup)+"?start="+str((pag-1)*24))
            return links
                
    elif "Funky" == store:        
        if item == "cat":
            menu = soup.find('ul',{'class':'sub-menu'})
            categorias = menu.find_all('li')
            cat = [c.a for c in categorias]
            return cat
        elif item == "prod":
            lista = findItem(soup,'ul','class','tablet-columns-2')
            products = findItems(lista,'div','class','product-loop-content')
            return products
        elif item == "name":
            name = soup.text
            return name
        elif item == "linkCat":
            link = soup.get('href')
            return link
        elif item == "nameProd":
            name = soup.h2.text.strip()
            return name
        elif item == "linkProd":
            link = soup.h2.a.get('href')
            return link
        elif item == "pag":
            lista = findItem(soup,'ul','class','page-numbers')
            if lista != None:
                links = findItems(lista,'a','class','page-numbers')
                newList = [l.get('href') for l in links]
                newList.insert(0,newList[-1][:-2]+'1/')
                newList.pop(-1)
                return newList
            else:
                return [soup]  

opcion = 0
while opcion != 9:
    opcion = int(input("Ingrese una Opcion que desee ver: \n1.Intelaf \n2.Click \n3.Funky \n4.Max \n5.Goat \n6.Elektra \n7.Spirit \n8.MacroSistemas \n9.Salir \n"))
    #Intelaf
    if opcion == 1:
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
        #Si quiero ver solo una categoria, solo poner comentario la de arriba y quitar comentarios abajo
        #     categorias[area.replace(" ","-")] = base + url
        # categorias['Audio'] = getCategorias(categorias['Audio'],"Intelaf")
        with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/intelaf/Intelaf.json",'w') as file:
            json.dump(categorias,file)
        file.close()
    #Click
    elif opcion == 2:
        categorias = {}
        base = "https://www.click.gt"
        categorias = getCategorias(base,"Click")
        print(categorias)
    #Funky
    elif opcion == 3:
        categorias = {}
        base = "https://storefunky.com"
        categorias = getCategorias(base,"Funky")
        #print(categorias)
        with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/funky/Funky.json",'w') as file:
            json.dump(categorias,file)
        file.close()
    #Max
    elif opcion == 4:
        categorias = {}
        base = "https://www.max.com.gt/"
        categorias = getCategorias(base,"Max")
        print(categorias)
        with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/max/max.json",'w') as file:
            json.dump(categorias,file)
        file.close()
    #Goat
    elif opcion == 5:
        pass
    #Elektra
    elif opcion == 6:
        pass
    #Spirit
    elif opcion == 7:
        pass
    #Macro
    elif opcion == 8:
        categorias = {}
        base = "https://www.macrosistemas.com"
        categorias = getCategorias(base,"Macro")
        print(categorias)
        with open("C:/Users/javie/Desktop//ecommerceScraper/EcommerceData/Guatemala/macrosistemas/macro.json",'w') as file:
            json.dump(categorias,file)
        file.close()
    #Salir
    elif opcion == 9:
        print("Adios")
