# =============================================================== #
#             Project Name: WebScraping Website service           #
#               Author: Javier Alejandro Diaz Portillo            #
#   Descripcion: Programa sirve para extraer links necesarios,    #
#       y tambien para extaer los datos de cada productos         #
# =============================================================== #

# Mi forma de resolver este problema es hacer 2 tipos de archivos JSON: uno para conseguir los links, otra para los datos de productos #
import json
from requests_html import HTMLSession
from datetime import date
import concurrent.futures as cf
from time import perf_counter
from bs4 import BeautifulSoup
from difflib import get_close_matches as gcm


#========Funciones Generales============#
def getUrl(url,session):
    try: send = session.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
    except:
        print("Revise el url, no se proceso correctamente")
        print("Url Fallido:" + url)
    else: return BeautifulSoup(send.text, 'html.parser')
        
def findItem(soup, item, attType, attName):
    try:result = soup.find(item, {attType: attName})
    except:pass #print("error en la funcion 'findItem'")#print("Item Fallido: " + format(item) + " Tipo de Atributo: " + format(attType) + " Nombre del Atributo: " +format(attName))
    else:return result

def findItems(soup, item, attType, attName):
    try:result = soup.find_all(item, {attType: attName})
    except: pass # print("error en la funcion 'findItems'") # print("Item Fallido: " + format(item) + " Tipo de Atributo: " + format(attType) + " Nombre del Atributo: " +format(attName))
    else: return result

def checkMenu(resList, res1):
    if resList == None or not resList or res1 == None or not res1: return False
    else:
        for r in resList:
            for r1 in res1: 
                if r == r1: return True
        else: return False

def jsonFile(directory,action,jsonData):
    if action == "newCatJson":
        products = {"Kemik": {"link": "https://www.kemik.gt", "categorias":{}},"Intelaf": {"link":"https://www.intelaf.com", "categorias":{}},"Click": {"link":"https://click.gt", "categorias":{}},"Funky": {"link": "https://storefunky.com", "categorias":{}},"Max": {"link":"https://www.max.com.gt", "categorias":{}},"Goat": {"link":"https://goatshopgt.com", "categorias":{}},"Elektra": {"link":"https://www.elektra.com.gt", "categorias":{}},"Spirit": {"link":"https://spiritcomputacion.com","categorias":{}},"MacroSistemas": {"link":"https://www.macrosistemas.com","categorias":{}},"TecnoFacil": {"link":"https://www.tecnofacil.com.gt","categorias":{}},"Pacifiko": {"link":"https://www.pacifiko.com","categorias":{}},"Zukko": {"link":"https://zukko.store","categorias":{}},"Guateclic": {"link":"https://www.guateclic.com","categorias":{}},"Imeqmo": {"link":"https://www.imeqmo.com","categorias":{}},"Office Depot": {"link":"https://www.officedepot.com.gt","categorias":{}}}
        with open(directory,'w',encoding='utf-8') as f: json.dump(jsonData,f,ensure_ascii=False)
        return products
    elif action == "getJson":
        file = open(directory,"r",encoding='utf-8-sig')
        jsonData = json.load(file)
        file.close()
        return jsonData
    elif action == "writeJson":
        with open(directory,'w',encoding='utf-8') as f: json.dump(jsonData,f,ensure_ascii=False)

#=======Funciones para Categorias========#
def instr1(store,opcion):
    start = perf_counter()
    today = date.today()
    print("Starting with...",store)
    client = HTMLSession()
    base = categories[store]["link"]
    categories[store] = {"categorias": getCategorias(base,base,store,[],"{:02d}".format(int(opcion)),client)}
    categories[store]["fechaAct"] = today.strftime("%d-%b-%Y")
    categories[store]["Duration"] = str(perf_counter() -start)
    jsonFile(dirCategories,"writeJson",categories)
    client.close()
    stop = perf_counter()
    return store + " Finished || Duration: " +  str(stop-start)
    
def getCategorias(base,link,store,res,codigo,client):
    level0 = {}
    soup = getUrl(link,client)
    res1 = getProdInfo(base,soup,store,"cat",client)
    level1 = {}
    same = checkMenu(res,res1)
    if not res1 or same==True:
        pag = getProdInfo(base,link,store,"pag",client)
        if not pag:
            print("No hay productos en " + link)
        else:
            for p in pag: #Lista links en la categorias
                soup = getUrl(p,client)
                res1 = getProdInfo(base,soup,store,"prod",client)
                if not res1: print("no hay productos en " + p)
                else:
                    codeProd = 0
                    #for r1 in res1:
                    with cf.ThreadPoolExecutor() as executor:
                        name1= [executor.submit(getProdInfo,base,r1,store,"nameProd",client) for r1 in res1]
                        link1= [executor.submit(getProdInfo,base,r1,store,"linkProd",client) for r1 in res1]
                        for i in range(len(name1)): codeProd +=1; level1[name1[i].result()] = { "codigo": codigo+"{:02d}".format(codeProd),"link" : link1[i].result()}
    else:
        res.extend(res1)
        code = 0
        with cf.ThreadPoolExecutor() as executor:            
            name1= [executor.submit(getProdInfo,base,r1,store,"name",client) for r1 in res1]
            link1= [executor.submit(getProdInfo,base,r1,store,"linkCat",client) for r1 in res1]
            for i in range(len(name1)): code+=1; print("Store:",store, "Category:", name1[i].result()); level1[name1[i].result().replace(" ","-")] = getCategorias(base,link1[i].result(),store,res,codigo+"{:02d}".format(code),client)
    level0 = level1 
    return level0

def getProdInfo(base,soup,store,item,client):
    if "Kemik" == store:
        if item == "cat":
            #Primero se busca submenu, porque el menu principal va a estar en cada pagina
            subcat = findItems(soup,'div','class','product-category')
            if not subcat: # Si no tiene submenus, entonces buscara el menu principal 
                menu = findItem(soup,'div','class','wide-nav')
                cat = findItems(menu,'a','class','nav-top-link')
                categorias = []
                for c in cat:#si encuentra el menu, tendremos categorias que tienen de por si, subcategorias
                    name = c.next_sibling
                    if name != None:
                        temp = findItems(name.next_sibling,'a',None,None)
                        for t in temp:
                            t.attrs = {'href' : t['href']} #Muchos de los links de kemik tienen mucha info inecesaria, entonces borramos eso y solo se agrega su link
                            categorias.append(t)
                    else:
                        c.attrs ={'href': c['href']}#Muchos de los links de kemik tienen mucha info inecesaria, entonces borramos eso y solo se agrega su link                   
                        categorias.append(c)
                #print(categorias)
                return categorias[:-1] 
            else:
                #print(subcat)
                sc = [i.a for i in subcat] #Si la url busca los submenus, entonces regresara eso y no el menu principal
                return sc
        elif item == "prod": return findItems(soup,'a','class','woocommerce-loop-product__link') #Busca todos los productos de una pagina, en la parte 'pag' iteramos para que repita en paginas con paginaciones
        elif item == "name": return soup.text.strip() # Quita todo el codigo html y nos muestra el nombre de la categoria
        elif item == "linkCat": return soup.get('href') #Quita el codigo html y muestra el link de la categoria
        elif item == "nameProd": return soup.text.strip() #Quita codigo html y muestra el nombre de productos
        elif item == "linkProd": return soup.get('href') #Quita codigo html y muestra el link de productos
        elif item == "pag":
            pag = []
            url = soup
            stop = False
            while not stop: 
                pag.append(url) #agrega el nuevo link de una pagina de paginacion
                soup = getUrl(url,client) 
                newLink = findItem(soup,'link','rel','next') #busca el siguiente pagina
                if newLink != None: url = newLink.get('href') # si lo tiene, nos asigna el nuevo url, y repite este proceso
                else: stop = True # si no tiene mas paginacion, detiene el ciclo y nos regresa la lista
            return pag 
    elif "Max" == store:
        if item == "cat":
            subcategorias = findItem(soup,'ul','class',['sub-cat-list' ,'slick-initialized' ,'slick-slider']) #Busca subcategorias primero
            if subcategorias != None: #Si tiene subcategorias, sacamos la lista de categorias en ese menu y retornamos
                list = findItems(subcategorias,'li',None,None)
                categorias = [i.a for i in list]
            else:#Si no tiene subcategorias, buscamos las categorias principales, ya que esta en todas las paginas
                menu = findItem(soup,'div','class','content-mega')
                cat = findItems(menu,'li','class','level2')
                categorias = [c.a for c in cat]
            return categorias
        elif item == "prod":
            #busca todos los productos en la pagina, si tiene paginacion, se va a la condicion "pag" para iterar este proceso
            container = findItem(soup,'ol','class',['products','list','items','product-items'])
            products = findItems(container,'a','class','product-item-link')
            return products
        elif item == "name": return soup.text.strip() #Busca nombre de categoria
        elif item == "linkCat": return soup.get('href') #Busca link de categoria
        elif item == "nameProd": return soup.text.strip() #Busca nombre del producto
        elif item == "linkProd": return soup.get('href') #Busca el link del producto
        elif item == "pag":
            links = []
            souptemp = getUrl(soup,client)
            #Max tiene el numero de productos, etnonces solo conseguimos el numero y lo dividimos entre 30 que es lo maximo que quieren desplegar, esto son las paginas que vamos a recorrer
            num = findItem(souptemp,'span','class','toolbar-number')
            if num != None:
                noProductos = int(num.text.replace("Productos"," ").replace("Producto"," "))
                paginas = 0
                if noProductos >= 30: paginas = noProductos//30
                else: paginas = 0

                if (noProductos % 30) >= 1: paginas += 1
                for iter in range(1,paginas+1): links.append(format(soup+"?p=" + format(iter) + "&product_list_limit=30"))
                return links
            else: return [soup]
    elif "Click" == store:
        if item == "cat":
            lists = [] #Solo hay un menu, no hay subcategorias o submenu
            menu = findItem(soup,'ul','class',['justify-content-center','container','d-flex','align-items-center','mb-0','mt-0','pr-4'])
            lists = findItems(menu,'li','class','nav-item')
            for l in lists:
                name = l.a.get('href')
                if name == None:
                    name = l.a.text.strip("(current)",).lower().replace("??","o")
                    ul = findItem(soup,'div','aria-labelledby',name)
                    listar = findItems(ul,'li',None,None)
                    lists.extend(listar)
            return lists
        elif item == "prod": return findItems(soup,'div','class','pt-2') #Busca todos los productos de la pagina, si tiene paginacion, entonces se repite este proceso
        elif item == "name":  #Nombre de categoria
            name = soup.a.get('href')
            if name == None:
                name = soup.a.text.strip("(current)",).lower().replace("??","o")
                ul = findItem(soup,'div','aria-labelledby',name)
                listar = findItems(ul,'li',None,None)
                for l in listar: return l.a.get('href').replace("/productos/","")
            else: return name.replace("/productos/","")
        elif item == "linkCat": #Link de categoria
            link = soup.a.get('href')
            if link == None:
                name = soup.a.text.strip("(current)",).lower().replace("??","o")
                ul = findItem(soup,'div','aria-labelledby',name)
                listar = findItems(ul,'li',None,None)
                for l in listar:
                    linkl = base + l.a.get('href')
                    return linkl
            return base + link
        elif item == "nameProd": return soup.h5.text +'-'+soup.textarea.text #Nombre de Producto
        elif item == "linkProd": return base + soup.a.get('href') #Link de producto
        elif item == "pag": #busca el numero de paginas que tiene, y nos da el parametro "page" del link
            tempsoup = getUrl(soup,client)
            links =[]
            pagination = findItems(tempsoup,'button','class','page-link')
            if len(pagination) == 0: res = soup; links.append(res)
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
            #Busca subcategorias primero, si no tiene, busca categorias principales
            categorias = findItems(soup,'div','class','vertical-separator')
            if not categorias:
                categorias = findItems(soup,'li','class','vm-categories-wall-catwrapper')
            return categorias
        elif item == "prod":
            #busca todos los productos en la pagina, si tiene paginacion, itera varias veces
            productos = findItems(soup,'a','class','item-title')
            return productos
        elif item == "name":
            #Busca nombre de las categorias
            name = soup.a.text.strip()
            return name
        elif item == "linkCat":
            #Busca link de las categorias
            link = base + soup.a.get('href')
            return link
        elif item == "nameProd":
            #Busca nombre de productos
            name = soup.text.strip().replace("\n","").replace(" ","-")
            return name
        elif item == "linkProd":
            #Busca link de productos
            link = base + soup.get('href')
            return link
        elif item == "pag":
            links = []
            tempsoup = getUrl(soup,client)
            # paginacion = findItem(tempsoup,'div','class',['vm-pagination','vm-pagination-bottom'])
            #Busca la paginacion
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
            if subcategorias != None: categorias = findItems(subcategorias,'a',None,None)
            else: menu = findItem(soup,'ul','id','menu_footer'); categorias = findItems(menu,'a',None,None)
            return categorias
        elif item == "prod": return findItems(soup,'div','class','product-inner')
        elif item == "name": return soup.text
        elif item == "linkCat": return base + format(soup.get('href'))
        elif item == "nameProd": return findItem(soup,'a','class','item-title')
        elif item == "linkProd": return base + findItem(soup,'a','class','item-title').get('href')
        elif item == "pag":
            tempsoup = getUrl(soup,client)
            divpag = findItem(tempsoup,'div','class','vm-pagination')
            if divpag == None: numeroPag = 1
            else:
                paginacion = findItem(divpag,'span','class','vm-page-counter')
                if paginacion.text=="": numeroPag = 1
                else: numeroPag = int(paginacion.text[-2:])
            links = []
            for pag in range(1,(numeroPag+1)):
                if pag == 1: links.append(format(soup)+"?start=0")
                elif pag >1: links.append(format(soup)+"?start="+str((pag-1)*24))
            return links
    elif "Funky" == store:        
        if item == "cat":
            menu = soup.find('ul',{'class':'sub-menu'})
            categorias = menu.find_all('li')
            cat = [c.a for c in categorias]
            return cat
        elif item == "prod": lista = findItem(soup,'ul','class','tablet-columns-2'); return findItems(lista,'div','class','product-loop-content')
        elif item == "name": return soup.text
        elif item == "linkCat": return soup.get('href')
        elif item == "nameProd": return soup.h2.text.strip()
        elif item == "linkProd": return soup.h2.a.get('href')
        elif item == "pag":
            lista = findItem(soup,'ul','class','page-numbers')
            if lista != None:
                links = findItems(lista,'a','class','page-numbers')
                newList = [l.get('href') for l in links]
                newList.insert(0,newList[-1][:-2]+'1/')
                newList.pop(-1)
                return newList
            else: return [soup]    
    elif "Elektra" == store:
        if item == "cat": return findItems(soup,'div','class','vtex-store-components-3-x-infoCardTextContainer--homeImgCategorias')
        elif item == "prod": return findItems(soup,'section','class','vtex-product-summary-2-x-container--shelfPLP')
        elif item == "name": return soup.text
        elif item == "linkCat":link = soup.a.get('href'); return base + link
        elif item == "nameProd": return soup.h1.text.strip()
        elif item == "linkProd": link = soup.a.get('href'); return base + link
        elif item == "pag":
            links = []
            page = 1
            running = True
            link = soup
            while running:
                links.append(link)
                tempsoup = getUrl(link,client)
                nextPage = tempsoup.find('div',{'class':'vtex-search-result-3-x-buttonShowMore--layout'})
                if nextPage.button != None: page+=1; link = soup +"?page="+str(page)
                else: running = False
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
    elif "TecnoFacil" == store:
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
                tempsoup = getUrl(link,client)
                nextPage = findItem(tempsoup,'a','title','Siguiente')
                if nextPage != None: link = nextPage["href"]
                else: running = False
            return links
    elif "Pacifiko" == store:
        if item == "cat":
            lists = findItems(soup,'div','class','responsiveS')
            if not lists :
                lists = []
                try: lists.extend(findItems(soup,'a','class','clearfix')[:-1])
                except: pass
                try: lists.extend(findItems(soup,'a','class','main-menu'))
                except: pass
                return [base + l["href"] for l in lists]
            else: return [l.a["href"] for l in lists]
        elif item == "prod":
            try: lists = findItems(soup,'div','class','product-image-container'); return [l.a for l in lists]
            except: return None
        elif item == "name": name = soup.replace("-"," "); return name[name.rfind("/")+1:]
        elif item == "linkCat": return soup
        elif item == "nameProd": return soup["title"]
        elif item == "linkProd": return soup["href"]
        elif item == "pag":
            links = []
            link = getUrl(soup,client)
            ul = findItem(soup,'ul','class','pagination')
            if ul == None: return [soup]
            else:
                pagination = findItems(ul,'a',None,None)
                totalpage = pagination[-1]["href"][pagination[-1]["href"].rfind("page=")+5:]
                for tp in range(int(totalpage),0,-1):
                    link = pagination[-1]["href"][:pagination[-1]["href"].rfind("page=")+5] + str(tp)
                    links.append(link)
            return links
    elif "Guateclic" == store:
        if item == "cat":
            cat = []
            ul = findItem(soup,'ul','class','navbar-nav')
            for l in ul.contents:
                if findItem(l,'ul',None,None) != None: li = [l.a for l in findItems(l.ul,'li',None,None)]; cat.extend(li)
                elif findItem(l,'a',None,None) != None and findItem(l,'ul',None,None) == None: cat.append(l.a)
            return cat[1:]
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
    elif  "Imeqmo"== store:
        if item == "cat":
            cat = []
            lists = findItem(soup,'ul','class','nav-pills')
            if not lists: return None
            else:
                for l in lists.contents:
                    if findItem(l,'ul',None,None) != None: li = [l.a for l in findItems(l.ul,'li',None,None)]; cat.extend(li)
                    elif findItem(l,'a',None,None) != None and findItem(l,'ul',None,None) == None: cat.append(l.a)
                return cat
        elif item == "prod": return [p.h6.a for p in findItems(soup,'td','class',['oe_product','oe_grid','te_t_image'])]
        elif item == "name": return soup.text
        elif item == "linkCat": return base[:-5] + soup["href"]
        elif item == "nameProd": return soup.text
        elif item == "linkProd": return base[:-5] + soup["href"]
        elif item == "pag":
            running = True
            links = []
            while running:
                links.append(soup)
                tempsoup = getUrl(soup,client)
                ul = findItem(tempsoup,'ul','class','pagination')
                if ul != None:
                    li = findItem(ul,'li','class',['page-item','disabled'])
                    if li != None: running = False; return links
                    else: soup = base + li.a["href"]
                else: running = False; return links
            return links     
    elif "Office Depot" == store:
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
    elif "Zukko" == store:
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
                return categorias
            else: return cat
        elif item == "prod": return findItems(soup,'div','class','zoom_info')
        elif item == "name":
            name = (findItem(soup,'div','class','image-area'))
            if name == None: return soup.text
            else: return name.get('title')
        elif item == "linkCat":
            if soup.get('href') == None: link = base+ "/" + soup.a['href']
            else: link = base+ "/" + soup.get('href')
            return link
        elif item == "nameProd": return (findItem(soup,'button','class','btn_cotiza')).get('name')
        elif item == "linkProd": return base + "/" + (findItem(soup,'button','class','btn_mas_info')).get('name')
        elif item == "pag": return [soup]
 
#=========Funciones para Productos=======#
def instr2(store,opcion):
    start = perf_counter()
    today = date.today()
    print("Starting with...",store)
    client = HTMLSession()
    base = categories[store]
    productos.update(parseProd(base,"",store,client))
    productos["fechaAct"] = today.strftime("%d-%b-%Y")
    productos["Duration"] = str(perf_counter() -start)
    jsonFile(dirProducts,"writeJson",productos)
    client.close()
    stop = perf_counter()
    return store + " Finished || Duration: " +  str(stop-start)

def parseProd(jsonData,cat,store,client):
    product={}
    if "-categorias-" in cat: cate = cat.removeprefix("-categorias-")
    else: cate = cat
    for i in jsonData:
        if isinstance(jsonData[i],dict): temp = parseProd(jsonData[i],format(cate+"-"+i),store,client); product.update(temp)
        else:
            codigos = jsonData.get("codigo")
            link = jsonData.get("link")
            if codigos != None and link != None: product[codigos] = buscarProd(link,cate.removesuffix(i),store,client)
    return product

def buscarProd(link,cat,store,client):
    #Done
    if store == "Kemik":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try: codigo = findItem(soup,'span','class','sku').text
        except: codigo = "N/A"
        #------Nombre del Producto-------#
        try: nombre = findItem(soup,'h1','class','product_title').text
        except: nombre = "N/A"
        #------Precio Viejo-------#
        try: precio = findItem(soup,'div','class','old-price').contents[2].text.strip("Q")
        except: precio = "N/A"
        #------Precio de Ofertas-------#
        try: oferta = findItem(soup,'div','id','price-after').contents[1].text.strip("Q")
        except: oferta = precio
        #------Detalles de Productos-------#
        detalles = []
        try: detalles.append(findItem(soup,'div','class','woocommerce-product-details__short-description'))
        except:  pass
        try: detalles.append(findItem(soup,'div','id','prduct-long-description').ul.text.strip())
        except: pass
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        try: garantia = findItem(soup,'ul','class','kemik-ul-msg-container').li.next_sibling.next_sibling.text.lstrip()
        except: garantia = "N/A"
    elif store == "Intelaf":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try: codigo = findItem(soup,'span','class','codigo').text[16:]
        except: codigo = "N/A"
        #------Nombre del Producto-------#
        try: nombre = findItem(soup,'h1',"class","descripcion_p").text
        except: nombre = "N/A"
        #------Precio Viejo-------#
        try: precio = findItem(soup,'span','class','precio_normal').strong.text.replace("Q","")
        except: precio = "N/A"
        #------Precio de Ofertas-------#
        try: oferta = findItem(soup,'span','class','beneficio_efectivo').text[20:]
        except: oferta = "N/A"
        #------Detalles de Productos-------#
        try:
            detalles = []
            cuerpo = findItem(soup,'div','id','esp_tec')
            des = findItems(cuerpo,'p',None,None)
            detalles.extend([d.text for d in des])
        except: detalles = "No se encontro descripcion de este producto en particular"    
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        try: garantia = findItem(soup,'span','class','garantia').text[9:-1]
        except: garantia = "N/A"
    elif store == "Click":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        codigo = link[(link.find("id")+3):]           
        #------Nombre del Producto-------#
        try: nombre = findItem(soup,"h2",None,None).text.strip() + ": " + findItem(soup,"h5",None,None).text.strip()
        except: nombre = "N/A"
        #------Precio Viejo-------#
        try: precio = findItem(soup,'span','class','grey-text').text
        except: precio = "N/A"
        #------Precio de Ofertas-------#
        try: oferta = findItem(soup,'span','class','red-text').text
        except: oferta = precio
        #------Detalles de Productos-------#
        try: detalles = findItem(soup,"div","class","card").text.replace("\n","")
        except: detalles = "N/A"
        #------Categorias-------#
        categoria = cat
        #------Garantias-------#
        try: garantia = "Cartuchos y Tinta: 0 meses, cables y adaptadores: 3 meses,drones varian y los demas productos se estima que son de 12 meses"
        except: garantia = "N/A"
    elif store == "Max":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try: codigo = findItem(soup, 'div', 'itemprop', 'sku').text
        except: codigo ="N/A"
        #------Nombre del Producto-------#
        try: nombre = findItem(soup, 'h1', 'class', 'page-title').text.strip()
        except: nombre ="N/A"
        #------Precio Viejo-------#
        try: precio = findItem(soup, 'span', 'data-price-type', 'oldPrice').text.strip("Q")
        except: precio ="N/A"
        #------Precio de Ofertas-------#
        try: oferta = findItem(soup, 'span', 'data-price-type', 'finalPrice').text.strip("Q")
        except: oferta = precio
        #------Detalles de Productos-------#
        detalles = []
        try: des = findItem(soup,'div','itemprop','description').text.strip()
        except: pass
        try: table = findItem(soup,'table','id','product-attribute-specs-table');rows = findItems(table,'td',"class","col data");detalles.extend([format(r["data-th"] + r.text) for r in rows])
        except: pass
        try:
            des = findItem(soup,'div','id','yt_tab_decription')
            parrafos = findItems(des,'p',None,None)
            descrip = [p.text.strip() for p in parrafos]
            descrip.remove(" "); descrip.remove("")
            detalles.extend(descrip)
        except: pass
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        try:
            if findItem(soup, 'td', 'data-th', 'garant??a') != None:
                garantia = findItem(soup, 'td', 'data-th', 'garant??a').text
            elif findItem(soup, 'td', 'data-th', 'Tiempo de garant??a') != None:
                garantia = findItem(soup, 'td', 'data-th', 'Tiempo de garant??a').text
            elif findItem(soup, 'td', 'data-th', 'A??os de garant??a totales') != None:
                garantia = findItem(soup, 'td', 'data-th', 'A??os de garant??a totales').text
            else:
                garantia = "N/A"
        except:
            garantia ="N/A"
    elif store == "Goat":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try: codigo = findItem(soup,'span','class','sku').text.strip()
        except: codigo = "N/A"
        #------Nombre del Producto-------#
        try: nombre = findItem(soup,'h1','class','product_title').text.strip()
        except: nombre = "N/A"
        #------Precio Viejo-------#
        try: precio = findItem(soup,'del',None,None).span.text.replace("Q","")
        except: precio = "N/A"
        #------Precio de Ofertas-------#
        try: oferta = findItem(soup,'bdi',None,None).span.text.replace("Q","")
        except: oferta = precio
        #------Detalles de Productos-------#
        try:
            detalles = []
            des = findItem(soup,'div','class','woocommerce-product-details__short-description')
            punto = findItems(des,'li',None,None)
            detalles.extend([p.text.strip() for p in punto])
        except: detalles = "N/A"
        #------Categorias-------#
        categoria = (cat)
        #---------Garantias---------#
        garantia ="De acuerdo a la tienda, todos los productos tienen 1 a??o de garantia"
    elif store == "Spirit":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try: codigo = findItem(soup,'div','class','sku').text.strip().replace("C??digo: ","")
        except: codigo ="N/A"
        #------Nombre del Producto-------#
        try: nombre = soup.find('h3',{'class':'title-product'})
        except: nombre = "N/A"
        #------Precio Viejo-------#
        try: precio = findItem(soup,'span','class','PricesalesPrice').text.replace("Q ","")
        except: precio = "N/A"
        #------Precio de Ofertas-------#
        try: oferta = findItem(soup,'div','class','cashprice').text[23:]
        except: oferta = "N/A"
        #------Detalles de Productos-------#
        try:
            detalles = []
            descripcion = findItem(soup,'div','class','product-description')
            fila = findItems(descripcion,'p',None,None)
            detalles = [f.text.strip() for f in fila]
        except: detalles = "N/A"
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantia = "De acuerdo a la tienda, nos muestra que debe reportar alguna falla o da??o del articulo en los 24 desde que se recibio el paquete"
    elif store == "Elektra":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try: codigo = findItem(soup,'div','class','ektguatemala-ektgt-components-0-x-pdpSku').text.replace("SKU: ","")
        except: codigo = "N/A"
        #------Nombre del Producto-------#
        try: nombre = findItem(soup,'h1','class','vtex-store-components-3-x-productNameContainer').text
        except: nombre = "N/A"
        #------Precio Viejo-------#
        try: precio = findItem(soup,'span','class','vtex-store-components-3-x-currencyContainer').span.text.replace("Q ","")
        except: precio = "N/A"
        #------Precio de Ofertas-------#
        try: oferta = findItem(soup,'span','class','vtex-store-components-3-x-sellingPrice').span.span.text.replace("Q ","")
        except: oferta = precio
        #------Detalles de Productos-------#
        try: detalles = []; detalles.append(findItem(soup,'div','class','vtex-store-components-3-x-productDescriptionText').text)
        except: pass
        #------Categorias-------#
        categoria = (cat)
        #---------Garantias---------#
        garantia = "De acuerdo a la tienda, todos los productos tienen 12 meses de garantia"
    elif store == "MacroSistemas":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try: codigo = findItem(soup,'div','class','sku').text.strip()[8:]
        except: codigo = "N/A"
        #------Nombre del Producto-------#
        try: nombre = findItem(soup,'h1','class','title-product').text.strip()
        except: nombre = "N/A"
        #------Precio Viejo-------#
        try: precio = findItem(soup,'span','class','PricesalesPrice').text.replace("Q ","")
        except: precio = "N/A"
        #------Precio de Ofertas-------#
        try:  oferta = findItem(soup,'div','class','cash').text[15:]
        except: oferta = precio
        #------Detalles de Productos-------#
        try:
            desTable = findItem(soup,'div','id','product-description-d')
            rows = findItems(desTable,'tr',None,None)
            detalles = [r.text.strip().replace("\n",": ") for r in rows]
        except: detalles = "N/A"
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantia = "N/A"
    elif store == "TecnoFacil":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try:  codigo = findItem(soup,'h6','class','sku').text
        except: codigo = "N/A"
        #------Nombre del Producto-------#
        try: nombre = findItem(soup,'div','class','product-name').text.strip()
        except: nombre = "N/A"
        #------Precio Viejo-------#
        #------Precio de Ofertas-------#
        try:
            precio = findItem(soup,'span','class','regular-price').text.strip()
            oferta = "N/A"
        except:
            try:
                precio = findItem(soup,'span','class','p_total').text.replace("Q","")
                oferta = "N/A"
            except:
                try:
                    precio = findItem(soup,'p','class','old-price').span.next_sibling.next_sibling.text.strip()
                except:
                    precio = "N/A"
                try:
                    oferta = findItem(soup,'p','class','special-price').span.next_sibling.next_sibling.text.strip()
                except:
                    oferta = "N/A"
                
        #------Detalles de Productos-------#
        detalles = []
        try: detalles.append(findItem(soup,'div','class','std').text.strip())
        except: pass
        try:
            table = findItems(soup,'tr',None,None)
            details = [format(t.th.text+": " + t.td.text) for t in table]
            detalles.extend(details)
        except: pass
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        garantia = "N/A"
    elif store == "Pacifiko":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'meta','name','external_id')["content"]
        except:
            codigo = "N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'div','class','title-product').text.strip()
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'span','id','price-old').text.strip().replace("Q","")
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'span','id','price-special').text.strip().replace("Q","")
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        detalles = []
        try:
            detalles.append(findItem(soup,'span','class','product-features').text.strip())
        except:
            pass
        try:
            detalles.append(findItem(soup,'div','id','tab-description').text.strip())
        except:
            pass
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantia = "N/A"
    elif store == "Guateclic":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'div','class','deal-content').p.text[findItem(soup,'div','class','deal-content').p.text.find('Cod.')+5:-1]
        except:
            codigo ="N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'div','class','deal-content').h3.text
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'p','class','value').text.replace("Q","")
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'h1',None,None).text.replace("Q","")
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        detalles = []
        try:
            detalles.append(findItem(soup,'div','class','deal-content').p.text)
        except:
            pass
        try:
            detalles.append(findItem(soup,'div','id','home0').ul.text.strip().replace("\n",", "))
        except:
            pass
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantia = "De acuerdo a la tienda, El tiempo de gesti??n de tu garant??a puede ser de 4 a 8 d??as h??biles despu??s de recibir el producto f??sicamente"
    elif store == "Imeqmo":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try: codigo = findItem(soup,'p','class','mt-3').text
        except: codigo ="N/A"
        #------Nombre del Producto-------#
        try:  nombre = findItem(soup,'div','class','deal-content').h3.text
        except: nombre = "N/A"
        #------Precio Viejo-------#
        try:  precio = findItem(soup,'span','class','oe_default_price').span.text
        except:  precio = "N/A"
        #------Precio de Ofertas-------#
        try: oferta = findItem(soup,'b','class','oe_price').span.text
        except: oferta = precio
        #------Detalles de Productos-------#
        detalles = []
        detalles.append(findItem(soup,'p','class','te_prod_desc').text.replace("\n-",","))
        detalles.append(findItem(soup,'div','id','product_full_description').text.strip().replace("\n",""))
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        try:
            garantia= findItem(soup,'p','class','mt-3').next_sibling.next_sibling.text.replace("Garant??a: ","")
        except:
            garantia = "N/A"
    elif store == "Office Depot":
        soup = getUrl(link,client)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'span','class','productCode').text
        except:
            codigo ="N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'h1','class','p-name').text.strip()
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'span','class','pricebefore').text.replace("Q","")
        except:
            precio = findItem(soup,'div','class','priceData').text.strip().replace("Q","")
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'div','id','priceFormato').text.replace("Q","").strip()
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        detalles = []
        try:
            findItem(soup,'input','id','descripcion')["value"].strip().replace("\n",", ")
        except: pass
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantia = "Revise la descripcion si muestra garantia"
    
    #Postponed
    elif store == "Zukko":
       pass
    elif store == "Funky":
        pass
    productInfo = {"codigo": codigo,"nombre": nombre,"precio": precio,"oferta": oferta,"categoria": categoria,"detalles": detalles,"garantia": garantia,"link" : link}
    return productInfo

#=========Funciones para Comparar============#
def compareProd():
    productos.pop("fechaAct")
    productos.pop("Duration")
    result = {}
    for p in productos: result[p] =  p + "|" + productos[p]["nombre"]
    matches = {}; count = 0; apercent = 0; bpercent = apercent
    for r in result:
        matches[r]= gcm(result[r],result.values(),cutoff=0.6)
        count+=1
        apercent = round(count/len(result)*100,None)
        if apercent != bpercent: print(f"Current percentage {apercent}%"); bpercent = apercent
    jsonFile(dirComparacion,"writeJson",matches)

#=================Menu===================#
def menu():
    tienda = [c.strip() for c in categories]
    opcion = 0
    while opcion != 3:
        opcion = int(input("Seleccione una opcion:\n1.Conseguir las categorias y productos de una pagina \n2.Conseguir informacion de todos los productos de una pagina\n3.Salir\n"))
        if opcion == 1:
            print("Elige una opcion:")
            for i in range(0,len(tienda)): print(str(i+1),tienda[i])
            ingreso = input("Escoge las tiendas que desee ver, presionando un numero separado por un espacio\n")
            opciones = ingreso.split(" ")
            store = []
            for o in opciones:
                if int(o) < 16: store.append(tienda[int(o)-1])
                else: print(o + " no es una opcion valida, se ira a la siguiente"); opciones.remove(o)
            #categories.clear()
            with cf.ThreadPoolExecutor() as executor:
                run = [executor.submit(instr1, o, opciones[int(store.index(o))]) for o in store ]
                for r in cf.as_completed(run): print(r.result())
        elif opcion == 2:
            print("Elige una opcion:")
            for i in range(0,len(tienda)): print(str(i+1),tienda[i])
            ingreso = input("Escoge las tiendas que desee ver, presionando un numero separado por un espacio\n")
            opciones = ingreso.split(" ")
            store = []
            for o in opciones:
                if int(o) < 16: store.append(tienda[int(o)-1])
                else: print(o + " no es una opcion valida, se ira a la siguiente"); opciones.remove(o)
            #categories.clear()
            with cf.ThreadPoolExecutor() as executor:
                run = [executor.submit(instr2, o, opciones[int(store.index(o))]) for o in store ]
                for r in cf.as_completed(run): print(r.result())
            compareProd()
        elif opcion == 3: pass
        else: pass

#=========Setup para Programa========#
#Entrada de Datos
dirProducts = "C:/Users/javie/Desktop/ecommerceScraper/products.json"
dirCategories = "C:/Users/javie/Desktop/ecommerceScraper/categories.json"
dirComparacion = "C:/Users/javie/Desktop/ecommerceScraper/comparison.json"

productos = jsonFile(dirProducts,"getJson",None)
categories = jsonFile(dirCategories,"getJson",None)
comparacion = jsonFile(dirComparacion,"getJson",None)
#Salida de Datos

#========Inicio del Programa============#
if __name__ == "__main__":
    start = perf_counter()
    print("Webscraper comparison project")
    menu()
    stop = perf_counter()
    print("Duration of Program:", stop-start)
