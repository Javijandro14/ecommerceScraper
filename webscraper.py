# =============================================================== #
#             Project Name: WebScraping Website service           #
#               Author: Javier Alejandro Diaz Portillo            #
#   Descripcion: Programa sirve para extraer links necesarios,    #
#       y tambien para extaer los datos de cada productos         #
# =============================================================== #

# Mi forma de resolver este problema es hacer 2 tipos de archivos JSON: uno para conseguir los links, otra para los datos de productos #

from bs4 import BeautifulSoup
import requests
import json
import time


def getUrl(url):
    try:
        send = requests.get(url)
        # send = requests.get(format(base)+"tienda/", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
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

def data(jsonData,store):
    intentosExitosos = 0
    intentosFallidos = 0
    for j in jsonData:
        print("Current Category:" + format(j))
        if isinstance(jsonData[j],dict):
            for k in jsonData[j]:
                if isinstance(jsonData[j][k],dict):
                    for l in jsonData[j][k]:
                        if isinstance(jsonData[j][k][l],dict):
                            for m in jsonData[j][k][l]:
                                if isinstance(jsonData[j][k][l][m],dict):
                                    for n in jsonData[j][k][l][m]:#jsonData[j][k][l][m][n]
                                        try:
                                            link = jsonData[j][k][l][m][n]
                                            cat = format(j)+"-"+format(k)+"-"+format(l)+"-"+format(m)
                                            productInfo = buscarProd(link,cat,store)
                                        except:
                                            print(format(link) + " --> Status: Fallido!")
                                            intentosFallidos += 1
                                        else:
                                            intentosExitosos += 1
                                            print(format(link) + " --> Status: Existoso!")
                                            jsonData[j][k][l][m][n] = productInfo
                                else:#jsonData[j][k][l][m]
                                    try:
                                        link = jsonData[j][k][l][m]
                                        cat = format(j)+"-"+format(k)+"-"+format(l)
                                        productInfo = buscarProd(link,cat,store)
                                    except:
                                        print(format(link) + " --> Status: Fallido!")
                                        intentosFallidos += 1
                                    else:
                                        intentosExitosos += 1
                                        print(format(link) + " --> Status: Existoso!")
                                        jsonData[j][k][l][m] = productInfo
                        else:#jsonData[j][k][l]
                            try:
                                link = jsonData[j][k][l]
                                cat = format(j)+"-"+format(k)
                                productInfo = buscarProd(link,cat,store)
                            except:
                                print(format(link) + " --> Status: Fallido!")
                                intentosFallidos += 1
                            else:
                                intentosExitosos += 1
                                print(format(link) + " --> Status: Existoso!")
                                jsonData[j][k][l] = productInfo
                else:#jsonData[j][k]
                    try:
                        link = jsonData[j][k]
                        cat = format(j)
                        productInfo = buscarProd(link,cat,store)
                    except:
                        print(format(link) + " --> Status: Fallido!")
                        intentosFallidos += 1
                    else:
                        intentosExitosos += 1
                        print(format(link) + " --> Status: Existoso!")
                        jsonData[j][k] = productInfo
        else:#jsonData[j]
            try:
                link = jsonData[j]
                cat = format(j)
                productInfo = buscarProd(link,cat,store)
            except:
                print(format(link) + " --> Status: Fallido!")
                intentosFallidos += 1
            else:
                intentosExitosos += 1
                print(format(link) + " --> Status: Existoso!")
                jsonData[j] = productInfo
    print("Exitosos:" + format(intentosExitosos))
    print("Fallidos:" + format(intentosFallidos))
    print("Porcentaje de Exito:" + format(intentosExitosos /(intentosFallidos+intentosExitosos)))
    return jsonData

def buscarProd(link,cat,store):
    if store == "Intelaf":
        soup = getUrl(link)
        paginaProducto = findItem(soup,'div','class','row cuerpo')
        #------Codigo del Producto-------#
        codigos = findItem(paginaProducto,'p','class','codigo')
        if codigos == None:
            return Exception
        else:            
            codigo = ((codigos.text)[16:])
        #------Nombre del Producto-------#
        title = findItem(paginaProducto,'h1',None,None).text
        if title == None:
            return Exception
        else:
            nombre = (title)
        #------Precio Viejo-------#
        precios = findItem(paginaProducto,'p','class','precio_normal')
        if precios == None:
            precios = "N/A"
            precio = (precios)
        else:
            precio = ((precios.text)[17:])
        #------Precio de Ofertas-------#
        precioOferta = findItem(paginaProducto,'p','class','beneficio_efectivo')
        if precioOferta == None:
            return Exception
        else:
            oferta = ((precioOferta.text)[21:])
        #------Detalles de Productos-------#
        detalle = paginaProducto.find_all('div',attrs = {'id' :'c1' , 'class':'col-xs-12'})
        if detalle == None:
            detalle = "N/A"
            detalles = (detalle)
        else:
            d = [i.text for i in detalle]
            detalles = (""+format(d)+"")
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        garantias = findItem(paginaProducto,'p','class','garantia')
        if garantias == None:
            garantias = "N/A"
            garantia = (garantias)
        else:
            garantia = (garantias.text[9:])  
    elif store == "Max":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        codigos = findItem(soup, 'div', 'itemprop', 'sku')
        if codigos == None:
            return Exception
        else:            
            codigo=(codigos.text)
        #------Nombre del Producto-------#
        title = findItem(soup, 'h1', 'class', 'page-title')
        if title == None:
            return Exception
        else:
            nombre = (title.text)
        #------Precio Viejo-------#
        precios = findItem(soup, 'span', 'data-price-type', 'oldPrice')
        if precios == None:
            precios = "N/A"
            precio = (precios)
        else:
            precio = ((precios.text)[1:])
        #------Precio de Ofertas-------#
        precioOferta = findItem(soup, 'span', 'data-price-type', 'finalPrice')
        if precioOferta == None:
            return Exception
        else:
            oferta = ((precioOferta.text)[1:])
        #------Detalles de Productos-------#
        detalle = findItems(soup, 'tr', None, None)
        d = [i.text for i in detalle]
        if detalle == None:
            detalles = "N/A"
        else:
            detalles = (""+format(d)+"")
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        garantias = findItem(soup, 'td', 'data-th', 'Garantía')
        if garantias == None:
            garantias = "N/A"
            garantia = (garantias)
        else:
            garantia = (garantias.text)
    elif store == "Goat":
        send = requests.get(link, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        soup = BeautifulSoup(send.text,'html.parser')
        #------Codigo del Producto-------#
        codigos = findItem(soup,'span','class','sku')
        if codigos == None:
            raise Exception
        else:            
            codigo = (codigos.text.strip())
        #------Nombre del Producto-------#
        title = soup.find('h1',{'class':'product_title'})
        if title == None:
            codigo.remove(codigos.text.strip())
            raise Exception
        else:
            nombre = (title.text)
        #------Precio Viejo-------#
        precioO = soup.find('del')
        if precioO == None:
            precioO="N/A"
            precio = (precioO)
        else:
            precio = (precioO.text)
        #------Precio de Ofertas-------#
        precioOferta = soup.find('bdi')
        if precioOferta == None:
            precioOferta = "N/A"
            oferta = (precioOferta)
        else:
            oferta = (precioOferta.text)
        #------Detalles de Productos-------#
        descripcion = soup.find('ul',{'class':'a-unordered-list'})
        if descripcion == None:
            descripcion = "N/A"
            detalles = (descripcion)
            
        else:
            detalles = (descripcion.text.strip())
        #------Categorias-------#
        categoria = (cat)
        #---------Garantias---------#
        garantiaP = "N/A"
        garantia = (garantiaP)
    elif store == "Elektra":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        codigos = (soup.find('div',{'class':'ektguatemala-ektgt-components-0-x-pdpSku'}))
        if codigos == None:
            raise Exception
        else:            
            codigo = (codigos.text.strip()[4:])
        #------Nombre del Producto-------#
        title = (soup.find('h1',{'class':'vtex-store-components-3-x-productNameContainer'}))
        if title == None:
            del codigo[-1]
            raise Exception
        else:
            nombre = (title.text.strip())
        divPrecio = findItems(soup,'div','class','vtex-flex-layout-0-x-flexRow--pdpTotal')
        precios = findItems(divPrecio[0],'span',None,None)
        #------Precio Viejo-------#
        precioO = precios[0].span.span.text
        precio = (precioO)
        #------Precio de Ofertas-------#
        precioOferta = precios[1].span.span
        if precioOferta == None:
            precioOferta = "N/A"
            oferta = (precioOferta)
        else:
            oferta = (precioOferta)
        #------Detalles de Productos-------#
        des = findItem(soup,'div','class','vtex-store-components-3-x-productDescriptionText')
        if des == None:
            descripcion = "N/A"
            detalles = (descripcion)
        else:
            detalles = (des.text)
        #------Categorias-------#
        categoria = (cat)
        #---------Garantias---------#
        garantiaP = "12 meses"
        garantia = (garantiaP)
    elif store == "Click":
        soup = getUrl(link)
        paginaProducto = findItem(soup,'section','class','text-center')
        #------Codigo del Producto-------#
        codigo = link[35:]           
        #------Nombre del Producto-------#
        marca = findItem(paginaProducto,"h2",None,None)
        des = findItem(paginaProducto,"h5",None,None)
        nombre = (marca.text).strip() + ": " + (des.text).strip()
        #------Precio de Ofertas-------#
        precioOferta = findItem(paginaProducto,'span','class','red-text')
        if precioOferta == None:
            precioOferta = "N/A"
            oferta = precioOferta
        else:
            oferta = precioOferta.text
        #------Precio Viejo-------#
        precios = findItem(paginaProducto,'span','class','grey-text')
        if precios == None:
            precios = "N/A"
            precio = precios
        else:
            precio = precios.text
        #------Categorias-------#
        categoria = cat
        #------Garantias-------#
        garantias = findItem(paginaProducto,"label",None,None)
        if garantias == None:
            garantias = "N/A"
            garantia = garantias
        else:
            garantia = garantias.text
        #------Detalles de Productos-------#
        especificar = findItem(paginaProducto,'div','id','collapseOne1')
        if especificar == None:
            raise
        else:
            detalles = (especificar.text).strip()
    elif store == "Spirit":
        base = "https://spiritcomputacion.com/"
        soup = getUrl(base + link)
        #------Codigo del Producto-------#
        codigos = findItem(soup,'div','class','sku')
        if codigos == None:
            raise Exception
        else:            
            codigo = (codigos.text)[7:]
        #------Nombre del Producto-------#
        title = soup.find('h3',{'class':'title-product'})
        if title == None:
            raise Exception
        else:
            nombre = title.text
        #------Precio Viejo-------#
        precioO = soup.find('span',{'class':'PricesalesPrice'})
        precio = precioO.text[2:]
        #------Precio de Ofertas-------#
        precioOferta = soup.find('div',{'class':'cashprice'})
        if precioOferta == None:
            precioOferta = "N/A"
            oferta = precioOferta
        else:
            oferta = (precioOferta.text)[22:]
        #------Detalles de Productos-------#
        descripcion = soup.find('div',{'class':'product-description'})
        if descripcion == None:
            descripcion = "N/A"
            detalles = descripcion
        else:
            detalles = descripcion.text
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantiaP = "N/A"
        garantia = garantiaP
    elif store == "Macro":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        codigos = (soup.find('div',{'class':'sku'}))
        if codigos == None:
            raise Exception
        else:            
            codigo = codigos.text.strip()[8:]
        #------Nombre del Producto-------#
        title = (soup.find('h1',{'class':'title-product'}))
        if title == None:
            raise Exception
        else:
            nombre = title.text.strip()
        #------Precio Viejo-------#
        precioO = (soup.find('span',{'class':'PricesalesPrice'})).text.strip()
        precio = precioO
        #------Precio de Ofertas-------#
        precioOferta = soup.find('div',{'class':'cash'})
        if precioOferta == None:
            precioOferta = "N/A"
            oferta = precioOferta
        else:
            oferta = precioOferta.text.strip()[13:]
        #------Detalles de Productos-------#
        des = soup.find('div',{'class':'product-description'})
        if des == None:
            descripcion = "N/A"
            detalles = descripcion
        else:
            descripcion = des.find_all('tr')
            detalles = [(i.text.strip()) for i in descripcion]
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantiaP = "N/A"
        garantia = garantiaP
    elif store == "Funky":
        send = requests.get(link, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        soup = BeautifulSoup(send.text,'html.parser')
        #------Codigo del Producto-------#
        codigos = findItem(soup,'span','class','sku')
        if codigos == None:
            raise Exception
        else:            
            codigo = codigos.text.strip()
        #------Nombre del Producto-------#
        title = soup.find('h1',{'class':'product_title'})
        if title == None:
            codigo.remove(codigos.text.strip())
            raise Exception
        else:
            nombre = title.text
        #------Precio Viejo-------#
        precioO = soup.find('del')
        if precioO == None:
            precioO="N/A"
            precio = precioO
        else:
            precio = precioO.text
        #------Precio de Ofertas-------#
        precioOferta = soup.find('bdi')
        if precioOferta == None:
            precioOferta = "N/A"
            oferta = precioOferta
        else:
            oferta = precioOferta.text
        #------Detalles de Productos-------#
        descripcion = soup.find('div',{'class':'woocommerce-product-details__short-description'})
        if descripcion == None:
            descripcion = "N/A"
            detalles = descripcion
        else:
            detalles = descripcion.text.strip()
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantiaP = "N/A"
        garantia = garantiaP
    productInfo = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "oferta": oferta,
            "categoria": categoria,
            "detalles": detalles,
            "garantia": garantia,
            "link" : link
    }
    return productInfo

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
                print("No hay productos en " + p)
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
                        print("No hay productos en " + p)
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
        pass
        # if item == "cat":
        #     send = requests.get(base+"tienda/", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        #     souptemp = BeautifulSoup(send.text,'html.parser')
        #     categorias = souptemp.find_all('div',{'class':['woocommerce','columns-1']})
        #     return categorias
        # elif item == "prod":
        #     pass
        # elif item == "name":
        #     name = cat .find('h2',{'class':'woocommerce-loop-category__title'})
        #     return name
        # elif item == "linkCat":
        #     link = cat .find('a').get('href')
        #     return link
        # elif item == "nameProd":
        #     pass
        # elif item == "linkProd":
        #     pass
        # elif item == "pag":
        #     pass
    elif "Elektra" == store:
        if item == "cat":
            categorias = findItems(soup,'div','class','vtex-store-components-3-x-infoCardTextContainer--homeImgCategorias')
            return categorias
        elif item == "prod":
            productos = findItems(soup,'section','class','vtex-product-summary-2-x-container--shelfPLP')
            return productos
        elif item == "name":
            name = soup.text
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
            link = soup.a.get('href')
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

# Estados Unidos(Expandir para mas info)
    # 1 Amazon(Expandir para mas info)
        # amazon = "https://www.amazon.com/"
        # send = requests.get(amazon)
        # soup = BeautifulSoup(send.text,'html.parser')
        # links = soup.find_all('')
        # for i in links:
        #     link = i
        #     print(link)
    # 2 Ebay(Expandir para mas info)
    # 3 Best Buy(Expandir para mas info)
    # 4 NewEgg(Expandir para mas info)
    # 5 Gearbest(Expandir para mas info)

# China(Expandir para mas info)

# Guatemala(Expandir para mas info)
opcion1 = 0
while opcion1 != 3:
    opcion1 = int(input("Ingrese el servicio que desee hacer: \n1.Actualizar lista de categorias y productos \n2.Actualizar informacion de productos \n3.Salir \n"))
    if opcion1 == 1: #Actualizar lista de categorias y productos
        opcion2 = 0
        while opcion2 != 9:
            categorias = {}
            opcion2 = int(input("Ingrese una opcion que desee ver: \n1.Intelaf \n2.Click \n3.Funky \n4.Max \n5.Goat \n6.Elektra \n7.Spirit \n8.MacroSistemas \n9.Salir \n"))
            #Intelaf
            if opcion2 == 1:
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
            elif opcion2 == 2:
                categorias = {}
                base = "https://www.click.gt"
                categorias = getCategorias(base,"Click")
                print(categorias)
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/click/click.json",'w') as file:
                    json.dump(categorias,file)
                file.close()
            #Funky
            elif opcion2 == 3:
                categorias = {}
                base = "https://storefunky.com"
                categorias = getCategorias(base,"Funky")
                #print(categorias)
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/funky/Funky.json",'w') as file:
                    json.dump(categorias,file)
                file.close()
            #Max
            elif opcion2 == 4:
                base = "https://www.max.com.gt/"
                categorias = getCategorias(base,"Max")
                print(categorias)
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/max/max.json",'w') as file:
                    json.dump(categorias,file)
                file.close()
            #Goat No esta terminado
            elif opcion2 == 5:
                categorias = {}
                base = "https://goatshopgt.com/"
                categorias = getCategorias(base,"Goat")
                print(categorias)
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/goatshop/Goat.json",'w') as file:
                    json.dump(categorias,file)
                file.close()
            #Elektra
            elif opcion2 == 6:
                base = "https://www.elektra.com.gt"
                categorias = getCategorias(base, "Elektra")
                print(categorias)
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/elektra/elektra.json",'w') as file:
                    json.dump(categorias,file)
                file.close()
            #Spirit
            elif opcion2 == 7:
                base = "https://spiritcomputacion.com"
                categorias = getCategorias(base, "Spirit")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/spiritcomputacion/spirit.json",'w') as file:
                    json.dump(categorias,file)
                file.close()
            #Macro
            elif opcion2 == 8:
                categorias = {}
                base = "https://www.macrosistemas.com"
                categorias = getCategorias(base,"Macro")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/macrosistemas/macro.json",'w') as file:
                    json.dump(categorias,file)
                file.close()
            #Salir
            elif opcion2 == 9:
                pass
    elif opcion1 == 2:
        opcion2 = 0
        while opcion2 != 9:
            opcion2 = int(input("Ingrese una opcion que desee ver: \n1.Intelaf \n2.Click \n3.Funky \n4.Max \n5.Goat \n6.Elektra \n7.Spirit \n8.MacroSistemas \n9.Salir \n"))
            #Intelaf
            if opcion2 == 1:
                file1 = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/intelaf/Intelaf.json",)
                jsonData = json.load(file)
                products = data(jsonData,"Intelaf")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/intelaf/IntelafProducts.json",'w') as file2:
                    json.dump(products,file2)
                file2.close()
            #Click
            elif opcion2 == 2:
                file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/click/Click.json",)
                jsonData = json.load(file)
                products = data(jsonData,"Click")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/click/ClickProducts.json",'w') as file:
                    json.dump(products,file)
                file.close()
            #Funky
            elif opcion2 == 3:
                file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/funky/Funky.json",)
                jsonData = json.load(file)
                products = data(jsonData,"Funky")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/funky/funkyProducts.json",'w') as file:
                    json.dump(products,file)
                file.close()
            #Max
            elif opcion2 == 4:
                file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/max/Max.json",)
                jsonData = json.load(file)
                products = data(jsonData,"Max")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/max/maxProducts.json",'w') as file:
                    json.dump(products,file)
                file.close()
            #Goat No esta terminado
            elif opcion2 == 5:
                file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/goatshop/Goatshop.json",)
                jsonData = json.load(file)
                products = data(jsonData,"Goat")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/goatshop/goatshopProducts.json",'w') as file:
                    json.dump(products,file)
                file.close()
            #Elektra
            elif opcion2 == 6:
                file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/elektra/Elektra.json",)
                jsonData = json.load(file)
                products = data(jsonData,"Elektra")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/elektra/elektraProducts.json",'w') as file:
                    json.dump(products,file)
                file.close()
            #Spirit
            elif opcion2 == 7:
                file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/spiritcomputacion/Spirit.json",)
                jsonData = json.load(file)
                products = data(jsonData,"Spirit")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/spiritcomputacion/spiritProducts.json",'w') as file:
                    json.dump(products,file)
                file.close()
            #Macro
            elif opcion2 == 8:
                file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/spiritcomputacion/Spirit.json",)
                jsonData = json.load(file)
                products = data(jsonData,"Spirit")
                with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/spiritcomputacion/spiritProducts.json",'w') as file:
                    json.dump(products,file)
                file.close()
            #Salir
            elif opcion2 == 9:
                pass
    elif opcion1 == 3:
        print("Adios")


            

            
            


    # Kemik
        # base = "https://www.kemik.gt"
        # soup = getUrl(base)
        # navbar = findItem(soup,'div','id','wide-nav')
        # menus = findItems(navbar,'li','class','menu-item-design-default')
        # level0 = { }

        # for menu in menus:
        #     name0 = format(findItem(menu,'a',None,None).text.strip()) + " lvl 0"
        #     link0 = findItem(menu,'a',None,None).get('href')
        #     level1 = {}
        #     submenu = findItem(menu,'ul','class','nav-dropdown-default')
        #     if submenu == None:# Si nivel 0 no tiene dropdown, entonces ira al unico link que tiene, y verifica si no tiene subcategorias
        #         soup = getUrl(link0)
        #         categorias = findItems(soup,'div','class','product-category')
        #         if not categorias:
        #             soup = getUrl(link0)
        #             productos = []
        #             productos = findItems(soup,'div','class','title-wrapper')
        #             level1 = {}
        #             for p in productos:
        #                 nameProd = findItem(p,'p','class','product-title').text
        #                 linkProd = findItem(p,'a',None,None).get('href')
        #                 level1["Prod:" + format(nameProd)] = linkProd
        #         else:
        #             for subcat in categorias:
        #                 name1 = findItem(subcat,'a',None,None)
        #                 link1 = findItem(subcat,'a',None,None)
        #                 if name1 == None or link1 == None: # Si tampoco tenemos subcategorias, entonces aqui tendremos codigo para conseguir todos los articulos
        #                     soup = getUrl(link1.get('href'))
        #                     productos = []
        #                     productos = findItems(soup,'div','class','title-wrapper')
        #                     level2 = {}
        #                     for p in productos:
        #                         nameProd = findItem(p,'p','class','product-title').text
        #                         linkProd = findItem(p,'a',None,None).get('href')
        #                         level2["Prod:" + format(nameProd)] = linkProd
        #                 else:# Si tenemos subcategorias, entonces los analizaremos y luego verificamos si no tiene subcategorias dentro de este hasta que lleguemos al nivel que debemos tener
        #                     soup = getUrl(link1.get('href'))
        #                     subcategorias1 = findItems(soup,'div','class','product-category')
        #                     level2 = {}
        #                     if not subcategorias1:
        #                         soup = getUrl(link0)
        #                         productos = []
        #                         productos = findItems(soup,'div','class','title-wrapper')
        #                         level1 = {}
        #                         for p in productos:
        #                             nameProd = findItem(p,'p','class','product-title').text
        #                             linkProd = findItem(p,'a',None,None).get('href')
        #                             level1["Prod:" + format(nameProd)] = linkProd
        #                     else:
        #                         for subcat1 in subcategorias1:
        #                             name2 = findItem(subcat1,'h5','class','header-title')
        #                             link2 = findItem(subcat1,'a',None,None)
        #                             if name2 == None or link2 == None:
        #                                 soup = getUrl(link2.get('href'))
        #                                 productos = []
        #                                 productos = findItems(soup,'div','class','title-wrapper')
        #                                 level3 = {}
        #                                 for p in productos:
        #                                     nameProd = findItem(p,'p','class','product-title').text
        #                                     linkProd = findItem(p,'a',None,None).get('href')
        #                                     level3["Prod:" + format(nameProd)] = linkProd
        #                             else:
        #                                 soup = getUrl(link2.get('href'))
        #                                 subcategorias2 = findItems(soup,'div','class','product-category')
        #                                 level3 ={}
        #                                 for subcat2 in subcategorias2:
        #                                     name3 = findItem(subcat2,'h5','class','header-title')
        #                                     link3 = findItem(subcat2,'a',None,None)
        #                                     if name3 == None or link3 == None:
        #                                         soup = getUrl(link3.get('href'))
        #                                         productos = []
        #                                         productos = findItems(soup,'div','class','title-wrapper')
        #                                         level4 = {}
        #                                         for p in productos:
        #                                             nameProd = findItem(p,'p','class','product-title').text
        #                                             linkProd = findItem(p,'a',None,None).get('href')
        #                                             level4["Prod:" + format(nameProd)] = linkProd
        #                                     else:
        #                                         soup = getUrl(link3.get('href'))
        #                                         subcategorias3 = findItems(soup,'div','class','product-category')
        #                                         level4 ={}
        #                                         for subcat3 in subcategorias3:
        #                                             name4 = findItem(subcat3,'h5','class','header-title')
        #                                             link4 = findItem(subcat3,'a',None,None)
        #                                             if name4 == None or link4 == None:
        #                                                 soup = getUrl(link4.get('href'))
        #                                                 productos = []
        #                                                 productos = findItems(soup,'div','class','title-wrapper')
        #                                                 level5 = {}
        #                                                 for p in productos:
        #                                                     nameProd = findItem(p,'p','class','product-title').text
        #                                                     linkProd = findItem(p,'a',None,None).get('href')
        #                                                     level5["Prod:" + format(nameProd)] = linkProd
        #                                                 level4[format(name4.text.strip()) + " lvl 4"] = level5
        #                                             else:
        #                                                 #Por si debemos seguir buscando mas niveles, se repite el codigo
        #                                                 level4[format(name4.text.strip()) + " lvl 4"] = link4.get('href') 
        #                                     level3[format(name3.text.strip()) + " lvl 3"] = level4        
        #                         level2[format(name2.text.strip()) + " lvl 2"] = level3
        #                 level1[format(name1.text.strip()) + " lvl 1"] = level2
        #     else:
        #         smlist = findItems(submenu,'li',None,None)
        #         for sml in smlist:
        #             name1 = format(sml.text.strip()) + " lvl 1"
        #             link1 = findItem(sml,'a',None,None).get('href')
        #             soup = getUrl(link1)
        #             categorias = findItems(soup,'div','class','product-category')
        #             level2 = {}
        #             for subcat in categorias:
        #                 name2 = findItem(subcat,'h5','class','header-title')
        #                 link2 = findItem(subcat,'a',None,None)
        #                 if name2 == None or link2 == None:
        #                     soup = getUrl(link2.get('href'))
        #                     productos = []
        #                     productos = findItems(soup,'div','class','title-wrapper')
        #                     level3 = {}
        #                     for p in productos:
        #                         nameProd = findItem(p,'p','class','product-title').text
        #                         linkProd = findItem(p,'a',None,None).get('href')
        #                         level3["Prod:" + format(nameProd)] = linkProd
        #                 else:
        #                     soup = getUrl(link2.get('href'))
        #                     subcategorias1 = findItems(soup,'div','class','product-category')
        #                     level3 ={}
        #                     for subcat1 in subcategorias1:
        #                         name3 = findItem(subcat,'h5','class','header-title')
        #                         link3 = findItem(subcat,'a',None,None)
        #                         if name3 == None or link3 == None:
        #                             soup = getUrl(link3.get('href'))
        #                             productos = []
        #                             productos = findItems(soup,'div','class','title-wrapper')
        #                             level4 = {}
        #                             for p in productos:
        #                                 nameProd = findItem(p,'p','class','product-title').text
        #                                 linkProd = findItem(p,'a',None,None).get('href')
        #                                 level4["Prod:" + format(nameProd)] = linkProd
        #                         else:
        #                             soup = getUrl(link3.get('href'))
        #                             subcategorias2 = findItems(soup,'div','class','product-category')
        #                             level4 = {}
        #                             for subcat2 in subcategorias2:
        #                                 name4 = findItem(subcat,'h5','class','header-title')
        #                                 link4 = findItem(subcat,'a',None,None)
        #                                 if name4 == None or link4 == None:
        #                                     soup = getUrl(link4.get('href'))
        #                                     productos = []
        #                                     productos = findItems(soup,'div','class','title-wrapper')
        #                                     level5 = {}
        #                                     for p in productos:
        #                                         nameProd = findItem(p,'p','class','product-title').text
        #                                         linkProd = findItem(p,'a',None,None).get('href')
        #                                         level5["Prod:" + format(nameProd)] = linkProd
        #                                     level4[format(name4.text.strip()) + " lvl 4"] = level5
        #                                 else:
        #                                     #Por si debemos seguir buscando mas niveles, se repite el codigo
        #                                     level4[format(name4.text.strip()) + " lvl 4"] = link4.get('href')
        #                         level3[format(name3.text.strip()) + " lvl 3"] = level4
        #                     #level2[name2.text.strip()] = link2.get('href')
        #                 level2[format(name2.text.strip()) + " lvl 2"] = level3
        #             level1[name1] = level2
        #     level0[name0] = level1
        # print("Se termino el proceso, revise si hay un documento json")

        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/kemik/kemikJson.json",'w') as file:
        #     json.dump(level0,file)
        # file.close()
                # file = open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/click/clickJson.json",)
                # jsonData = json.load(file)

                # intentosExitosos = 0
                # intentosFallidos = 0

                # directory = 'C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/click/clickProducts.xlsx'
                # sheetName = []
                # df = []

                # for j in jsonData:
                #     codigo = []
                #     nombre = []
                #     precio = []
                #     oferta = []
                #     categoria = []
                #     detalles = []
                #     garantia = []
                #     for k in jsonData[j]:
                #         for l in jsonData[j][k]:
                #             link = jsonData[j][k][l]
                #             try:
                #                 soup = getUrl(link)
                #                 paginaProducto = findItem(soup,'section','class','text-center')
                #                 #------Codigo del Producto-------#
                #                 codigos = link[35:]           
                #                 #------Nombre del Producto-------#
                #                 marca = findItem(paginaProducto,"h2",None,None)
                #                 des = findItem(paginaProducto,"h5",None,None)
                #                 nombre.append((marca.text).strip() + ": " + (des.text).strip())
                #                 #------Precio de Ofertas-------#
                #                 precioOferta = findItem(paginaProducto,'span','class','red-text')
                #                 if precioOferta == None:
                #                     precioOferta = "N/A"
                #                     oferta.append(precioOferta)
                #                 else:
                #                     oferta.append(precioOferta.text)
                #                 #------Precio Viejo-------#
                #                 precios = findItem(paginaProducto,'span','class','grey-text')
                #                 if precios == None:
                #                     precios = "N/A"
                #                     precio.append(precios)
                #                 else:
                #                     precio.append(precios.text)
                #                 #------Categorias-------#
                #                 categoria.append(format(k))
                #                 #------Garantias-------#
                #                 garantias = findItem(paginaProducto,"label",None,None)
                #                 if garantias == None:
                #                     garantias = "N/A"
                #                     garantia.append(garantia)
                #                 else:
                #                     garantia.append(garantias.text)
                #                 #------Detalles de Productos-------#
                #                 especificar = findItem(paginaProducto,'div','id','collapseOne1')
                #                 if especificar == None:
                #                     continue
                #                 else:
                #                     detalles.append((especificar.text).strip())
                #             except:
                #                 print(link + " --> Status: Fallido!")
                #                 intentosFallidos += 1
                #                 break
                #             else:
                #                 intentosExitosos += 1
                #                 print(link + " --> Status: Existoso!")
                #                 codigo.append(codigos)
                #                 soup.decompose()
                #         productInfo = {
                #         "codigo": codigo,
                #         "nombre": nombre,
                #         "precio": precio,
                #         "oferta": oferta,
                #         "categoria": categoria,
                #         "detalles": detalles,
                #         "garantia": garantia
                #         }
                #     sheetName.append(format(j))
                #     df.append(pd.DataFrame(productInfo, columns = ["codigo", "nombre", "precio","oferta", "categoria", "detalles", "garantia"]))
                #     gc.collect()

                # writer = pd.ExcelWriter(directory, engine='xlsxwriter')
                # for i in range(1, len(df)):
                #    df[i-1].to_excel(writer, sheetName[i-1])
                # writer.save()

                # print("Exitosos:" + format(intentosExitosos))
                # print("Fallidos:" + format(intentosFallidos))
                # print("Porcentaje de Exito:" + format(intentosExitosos /(intentosFallidos+intentosExitosos)))
    #No terminado(Postponer)

    #Tecnofacil(Expandir para mas info)
    #No terminado



    # Pacifiko(Expandir para mas info)
        # def getUrl(url):
        #     try:
        #         request = requests.Session()
        #         send = request.get(url)
        #     except:
        #         print("Revise el url, no se proceso correctamente")
        #         print("Url Fallido:" + url)
        #     else:
        #         soup = BeautifulSoup(send.text, 'html.parser')
        #         return soup

        # base = "https://www.pacifiko.com/"

        # test = "https://www.pacifiko.com/compras-en-linea/bateria-de-reemplazo-para-samsung-s6-edge-steren&pid=MGFkZjNhOT"

        # soup = getUrl(test)

        # codigo = soup.find('span',{'class':'propery-des'})
        # print(codigo.text)

        # title = soup.find('h1')
        # print(title.text)

        # precioO = soup.find('span',{'id':'price-old'})
        # print((precioO.text).strip())

        # oferta = soup.find('span',{'id':'price-special'})
        # if oferta == None:
        #     oferta = "N/A"
        #     print(oferta)
        # else:
        #     print((oferta.text).strip())
    #No terminado

   


    #Terminado

    #Zukko
        #base = "https://zukko.store/"
        #soup = getUrl("https://app.ecwid.com/categories.js?ownerid=50367225&lang=es_419&jsonp=menu.fill")
    #No terminado

    

    #Guateclic
# base = "https://www.guateclic.com"
# soup = getUrl(base)
# menu = findItems(soup,'div','class','col-sm-3')
# categorias = findItems(menu[1],'a','class','whitetext')
# level0 = {}
# for cat in categorias:
#     name0 = cat.text
#     link0 = base + cat.get('href')
#     level0[name0] = link0
# print(level0)  
    #No terminado

    #Imeqmo
#https://www.imeqmo.com/
    #No terminado

    #Office Depot
#https://www.officedepot.com.gt/
    #No terminado

        # Existencias del Producto
            # Falta terminar esta parte
            #     disp = soup.find('div',{'class':'col-xs-12 col-md-3 columna_existencias'})
            #     tiendas = disp.find_all('div',{'class':'div_stock_sucu'})
            #     existencias = {}
            #     existencias["codigo"] = (paginaProducto.find('p',{'class':'codigo'}).text)[16:]
            #     existencias["VentaLinea"] = disp.find('div',{'class':'col-xs-1'}).text
            # for j in tiendas:
            #     tienda = j.find_all('div')
            #     existencias[tienda[0].text] = tienda[1] .text
            # print(existencias)
    #Terminado(Faltan Existencias, pero eso se vera luego)