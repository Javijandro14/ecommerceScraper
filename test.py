import json
import requests
from datetime import date
import concurrent.futures as cf
from time import perf_counter
from bs4 import BeautifulSoup


def getUrl(url,client):
    try:
        send = client.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
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
        pass
        #print("error en la funcion 'findItem'")
        #print("Item Fallido: " + format(item) + " Tipo de Atributo: " + format(attType) + " Nombre del Atributo: " +format(attName))
    else:
        return result

def findItems(soup, item, attType, attName):
    try:
        result = soup.find_all(item, {attType: attName})
    except:
        pass
        # print("error en la funcion 'findItems'")
        # print("Item Fallido: " + format(item) + " Tipo de Atributo: " + format(attType) + " Nombre del Atributo: " +format(attName))
    else:
        return result

def checkMenu(resList, res1):
    if resList == None or not resList:
        return False
    else:
        for r in resList:
            for r1 in res1:
                if r == r1:
                    return True
        else:
            return False

def jsonFile(directory,action,jsonData):
    if action == "newCatJson":
        products = {
            "Kemik": {"link": "https://www.kemik.gt", "categorias":{}},
            "Intelaf": {"link":"https://www.intelaf.com", "categorias":{}},
            "Click": {"link":"https://click.gt", "categorias":{}},
            "Funky": {"link": "https://storefunky.com", "categorias":{}},
            "Max": {"link":"https://www.max.com.gt", "categorias":{}},
            "Goat": {"link":"https://goatshopgt.com", "categorias":{}},
            "Elektra": {"link":"https://www.elektra.com.gt", "categorias":{}},
            "Spirit": {"link":"https://spiritcomputacion.com","categorias":{}},
            "MacroSistemas": {"link":"https://www.macrosistemas.com","categorias":{}},
            "TecnoFacil": {"link":"https://www.tecnofacil.com.gt","categorias":{}},
            "Pacifiko": {"link":"https://www.pacifiko.com","categorias":{}},
            "Zukko": {"link":"https://zukko.store","categorias":{}},
            "Guateclic": {"link":"https://www.guateclic.com","categorias":{}},
            "Imeqmo": {"link":"https://www.imeqmo.com","categorias":{}},
            "Office Depot": {"link":"https://www.officedepot.com.gt","categorias":{}}
        }
        with open(directory,'w',encoding='utf-8') as f:
            json.dump(jsonData,f,ensure_ascii=False)
        return products
    elif action == "getJson":
        file = open(directory,"r")
        jsonData = json.load(file)
        file.close()
        return jsonData
    elif action == "writeJson":
        with open(directory,'w',encoding='utf-8') as f:
            json.dump(jsonData,f,ensure_ascii=False)

def instr(store,opcion):
    today = date.today()
    print("Starting with...",store)
    client = requests.Session()
    base = categories[store]["link"]
    categories[store] = {"categorias": getCategorias(base,base,store,[],"{:02d}".format(int(opcion)),client)}
    #categories[store] = {"categorias": "test" }
    categories[store]["fechaAct"] = today.strftime("%d-%b-%Y")
    jsonFile("C:/Users/javie/Desktop/testing.json","writeJson",categories)
    return store + "Finished"
    
def getCategorias(base,link,store,res,codigo,client):
    level0 = {}
    soup = getUrl(link,client)
    res1 = getProdInfo(base,soup,store,"cat",client)
    level1 = {}
    same = checkMenu(res,res1)
    if not res1 or same==True:
        pag = getProdInfo(base,link,store,"pag",client)
        for p in pag: #Lista links en la categorias
            soup = getUrl(p,client)
            res1 = getProdInfo(base,soup,store,"prod",client)
            if not res1: 
                print("no hay productos en " + p)
            else:
                codeProd = 0
                #for r1 in res1:
                with cf.ThreadPoolExecutor() as executor:
                    name1= [executor.submit(getProdInfo,base,r1,store,"nameProd",client) for r1 in res1]
                    for n1 in cf.as_completed(name1):
                        print(n1.result())
                    link1= [executor.submit(getProdInfo,base,r1,store,"linkProd",client) for r1 in res1]
                    for l1 in cf.as_completed(link1):
                        print(l1.result())
                    codeProd +=1
    else:
        res.extend(res1)
        code = 0
        with cf.ThreadPoolExecutor() as executor:            
            name1= [executor.submit(getProdInfo,base,r1,store,"name",client) for r1 in res1]
            link1= [executor.submit(getProdInfo,base,r1,store,"linkCat",client) for r1 in res1]
            for i in range(len(name1)):
                code+=1
                level1[name1[i].result().replace(" ","-")] = getCategorias(base,link1[i].result(),store,res,codigo+"{:02d}".format(code),client)
    level0 = level1  
    return level0

def getProdInfo(base,soup,store,item,client):
    if "Kemik" == store:
        if item == "cat":
            subcat = findItems(soup,'div','class','product-category')
            if not subcat:
                menu = findItem(soup,'div','class','wide-nav')
                cat = findItems(menu,'a','class','nav-top-link')
                categorias = []
                for c in cat:
                    name = c.next_sibling
                    if name != None:
                        temp = findItems(name.next_sibling,'a',None,None)
                        for t in temp:
                            t.attrs = {'href' : t['href']}
                            categorias.append(t)
                    else:
                        c.attrs ={'href': c['href']}                        
                        categorias.append(c)
                #print(categorias)
                return categorias[:-1]
            else:
                #print(subcat)
                sc = [i.a for i in subcat]
                return sc
        elif item == "prod":
            productos = findItems(soup,'a','class','woocommerce-loop-product__link')
            return productos
        elif item == "name":
            name = soup.text.strip()
            #print(name)
            return name
        elif item == "linkCat":
            link = soup.get('href')
            return link
        elif item == "nameProd":
            name = soup.text.strip()
            return name
        elif item == "linkProd":
            link = soup.get('href')
            return link
        elif item == "pag":
            pag = []
            url = soup
            stop = False
            while not stop:
                pag.append(url)
                soup = getUrl(url,client)
                newLink = findItem(soup,'link','rel','next')
                if newLink != None:
                    url = newLink.get('href')
                else:
                    stop = True
            return pag 
    elif "Intelaf" == store:
        if item == "cat":
            cat = findItems(soup,'a','class','hover_effect')
            if not cat:
                url = "https://www.intelaf.com/js/menu_productos22112021091955.json"
                res = getUrl(url,client)
                data = json.loads(res.text)
                menu = data['menu_sub_1s']
                categorias = []
                for info in menu:
                    area = info['Area']
                    url = info['url']
                    tag = BeautifulSoup('<a href="'+ url +'">'+area.replace(" ","-")+ '</a>','html.parser')
                    categorias.append(tag)
                #print(categorias)
                return categorias
            else:
                return cat
        elif item == "prod":
            return findItems(soup,'div','class','zoom_info')
        elif item == "name":
            #print(soup)
            name = (findItem(soup,'div','class','image-area'))
            if name == None:
                name = soup.text
                return name
            else:
                return name.get('title')
        elif item == "linkCat":
            if soup.get('href') == None:
                link = base+ "/" + soup.a['href']
            else:
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
    elif "Click" == store:
        if item == "cat":
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
        elif item == "prod":
            products = findItems(soup,'div','class','pt-2')
            return products
        elif item == "name":
            name = soup.a.get('href')
            if name == None:
                name = soup.a.text.strip("(current)",).lower().replace("ó","o")
                ul = findItem(soup,'div','aria-labelledby',name)
                listar = findItems(ul,'li',None,None)
                for l in listar:
                    return l.a.get('href').replace("/productos/","")
            else:
                return name.replace("/productos/","")
        elif item == "linkCat":
            link = soup.a.get('href')
            if link == None:
                name = soup.a.text.strip("(current)",).lower().replace("ó","o")
                ul = findItem(soup,'div','aria-labelledby',name)
                listar = findItems(ul,'li',None,None)
                for l in listar:
                    linkl = base + l.a.get('href')
                    return linkl
            return base + link
        elif item == "nameProd":
            name = soup.h5.text +'-'+soup.textarea.text
            return name
        elif item == "linkProd":
            link = base + soup.a.get('href')
            return link
        elif item == "pag":
            tempsoup = getUrl(soup)
            links =[]
            pagination = findItems(tempsoup,'button','class','page-link')
            if len(pagination) == 0:
                res = soup
                links.append(res)
            elif len(pagination) == 2:
                paginas = int(pagination[0].text)
                for i in range(1, paginas+1):
                    res = soup+"?page="+format(i)
                    links.append(res)
            elif len(pagination) == 3:
                paginas = int(pagination[-2].text)
                for i in range(1, paginas+1):
                    res = soup+"?page="+format(i)
                    links.append(res)
            else:
                paginas = int(pagination[-2].text)
                for i in range(1, paginas+1):
                    res = soup+"?page="+format(i)
                    links.append(res)
            return links
    elif "Spirit" == store:
        if item == "cat":
            categorias = findItems(soup,'div','class','vertical-separator')
            if not categorias:
                categorias = findItems(soup,'li','class','vm-categories-wall-catwrapper')
            return categorias
        elif item == "prod":
            productos = findItems(soup,'a','class','item-title')
            return productos
        elif item == "name":
            name = soup.a.text.strip()
            return name
        elif item == "linkCat":
            link = base + soup.a.get('href')
            return link
        elif item == "nameProd":
            name = soup.text.strip().replace("\n","").replace(" ","-")
            return name
        elif item == "linkProd":
            link = base + soup.get('href')
            return link
        elif item == "pag":
            links = []
            tempsoup = getUrl(soup)
            # paginacion = findItem(tempsoup,'div','class',['vm-pagination','vm-pagination-bottom'])
            paginas = findItems(tempsoup,'a','class','pagenav')
            if not paginas:
                links.append(soup)
            else:
                links = [base + i.get('href') for i in paginas[:-2]]
                links.insert(0,soup)
            return links
    elif "MacroSistemas" == store:
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
    elif "Elektra" == store:
        if item == "cat":
            categorias = findItems(soup,'div','class','vtex-store-components-3-x-infoCardTextContainer--homeImgCategorias')
            return categorias
        elif item == "prod":
            productos = findItems(soup,'section','class','vtex-product-summary-2-x-container--shelfPLP')
            return productos
        elif item == "name":
            name = soup.text
            print(name)
            return name
        elif item == "linkCat":
            link = soup.a.get('href')
            return base + link
        elif item == "nameProd":
            name = soup.h1.text.strip()
            return name
        elif item == "linkProd":
            link = soup.a.get('href')
            return base + link
        elif item == "pag":
            links = []
            page = 1
            running = True
            link = soup
            while running:
                links.append(link)
                tempsoup = getUrl(link)
                nextPage = tempsoup.find('div',{'class':'vtex-search-result-3-x-buttonShowMore--layout'})
                if nextPage.button != None:
                    page+=1
                    link = soup +"?page="+str(page)
                else:
                    running = False
            return links
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
    elif store == "TecnoFacil":
        if item == "cat":
            lists = findItems(soup,'div','class','media-body')
            cat = []
            for l in lists:
                temp = l.a['href'].find("?")
                if temp == -1:
                    pass
                else:
                    l.a['href'] = l.a['href'][:temp+1].replace("?","")
                cat.append(l.a)
            return cat
        elif item == "prod":
            prod = findItems(soup,'h2','class','product-name')
            return prod
        elif item == "name":
            name = soup.text.strip()
            return name
        elif item == "linkCat":
            link =soup["href"]
            return link
        elif item == "nameProd":
            name = soup.text
            return name
        elif item == "linkProd":
            link = soup.a["href"]
            return link
        elif item == "pag":
            links = []
            running = True
            link = soup
            #print(soup)
            while running:
                links.append(link)
                tempsoup = getUrl(link)
                nextPage = findItem(tempsoup,'a','title','Siguiente')
                if nextPage != None:
                    link = nextPage["href"]
                else:
                    running = False
            return links
    elif store == "Pacifiko":
        if item == "cat":
            lists = findItems(soup,'div','class','responsiveS')
            if not lists :
                cat = []
                cat.extend(findItems(soup,'a','class','clearfix')[:-1])
                cat.extend(findItems('main-menu'))
            else:
                cat = [l.a for l in lists]
            return cat
        elif item == "prod":
            lists = findItems(soup,'div','class','product-image-container')
            prod = [l.a for l in lists]
            return prod
        elif item == "name":
            name = soup["href"][soup["href"].rfind("/")+1:].replace("-"," ")
        elif item == "linkCat":
            link = soup["href"]
            return link
        elif item == "nameProd":
            pass
        elif item == "linkProd":
            pass
        elif item == "pag":
            pass
    elif store == "Guateclic":
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
    elif store == "Imeqmo":
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
    elif store == "Office Depot":
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
    #Postponed
    elif store == "Zukko":
       pass
 

def menu():
    tienda = [c.strip() for c in categories]
    opcion = 0
    while opcion != 3:
        opcion = int(input("Seleccione una opcion:\n1.Conseguir las categorias y productos de una pagina \n2.Conseguir informacion de todos los productos de una pagina\n3.Salir\n"))
        if opcion == 1:
            print("Elige una opcion:")
            for i in range(0,len(tienda)):
                print(str(i+1),tienda[i])
            ingreso = input("Escoge las tiendas que desee ver, presionando un numero separado por un espacio\n")
            opciones = ingreso.split(" ")
            store = []
            for o in opciones:
                if int(o) < 16: store.append(tienda[int(o)-1])
                else: print(o + " no es una opcion valida, se ira a la siguiente"); opciones.remove(o)
            #categories.clear()
            with cf.ThreadPoolExecutor() as executor:
                run = [executor.submit(instr, store[int(o)],opciones[int(o)]) for o in range(len(store))]
                for r in cf.as_completed(run):
                    print(r.result())
        elif opcion == 2:
            pass
        elif opcion == 3:
            pass
        else:
            pass


categories = jsonFile("C:/Users/javie/Desktop/ecommerceScraper/testing.json","getJson",None)

if __name__ == "__main__":
    start = perf_counter()
    print("Webscraper comparison project")
    menu()
    stop = perf_counter()
    print("Duration of Program:", stop-start)
