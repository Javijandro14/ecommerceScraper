from datetime import date
from bs4 import BeautifulSoup
import requests
import json
import time


def getUrl(url):
    try:
        send = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
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

# def data(jsonData,store,intentosFallidos,intentosExitosos):
    #     for j in jsonData:
    #         if isinstance(jsonData[j],dict):
    #             print("Current Category:" + format(j))
    #             data(jsonData[j],store,intentosFallidos,intentosExitosos)
    #         else:#jsonData
    #             try:
    #                 link = jsonData[j]
    #                 cat = format(j)
    #                 #productInfo = buscarProd(link,cat,store)
    #             except:
    #                 #print(format(link) + " --> Status: Fallido!")
    #                 intentosFallidos += 1
    #             else:
    #                 intentosExitosos += 1
    #                 #print(format(link) + " --> Status: Existoso!")
    #                 #jsonData[j] = productInfo
    #     # print("Exitosos:" + format(intentosExitosos))
    #     # print("Fallidos:" + format(intentosFallidos))
    #     # print("Porcentaje de Exito:" + format(intentosExitosos /(intentosFallidos+intentosExitosos)))
    #     return jsonData

def buscarProd(link,cat,store):
   #Revisar Intelaf
    if store == "Intelaf":
        soup = getUrl(link)
        paginaProducto = findItem(soup,'div','class','row cuerpo')
        #------Codigo del Producto-------#
        codigos = findItem(paginaProducto,'p','class','codigo')
        if codigos == None:
            codigo = "N/A"
        else:            
            codigo = ((codigos.text)[16:])
        #------Nombre del Producto-------#
        title = findItem(paginaProducto,'h1',None,None)
        if title == None:
            nombre = "N/A"
        else:
            nombre = (title.text)
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
            oferta = "N/A"
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
            codigo = "N/A"
        else:            
            codigo=(codigos.text)
        #------Nombre del Producto-------#
        title = findItem(soup, 'h1', 'class', 'page-title')
        if title == None:
            nombre = "N/A"
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
            oferta = "N/A"
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
            codigo =  "N/A"
        else:            
            codigo = (codigos.text.strip())
        #------Nombre del Producto-------#
        title = soup.find('h1',{'class':'product_title'})
        if title == None:
            nombre = "N/A"
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
            codigo = "N/A"
        else:            
            codigo = (codigos.text.strip()[4:])
        #------Nombre del Producto-------#
        title = (soup.find('h1',{'class':'vtex-store-components-3-x-productNameContainer'}))
        if title == None:
            nombre = "N/A"
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
        if marca != None and des != None:
            nombre = (marca.text).strip() + ": " + (des.text).strip()
        else:
            nombre = "N/A"
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
            detalles = "N/A"
        else:
            detalles = (especificar.text).strip()
    elif store == "Spirit":
        base = "https://spiritcomputacion.com/"
        soup = getUrl(base + link)
        #------Codigo del Producto-------#
        codigos = findItem(soup,'div','class','sku')
        if codigos == None:
            codigo = "N/A"
        else:            
            codigo = (codigos.text)[7:]
        #------Nombre del Producto-------#
        title = soup.find('h3',{'class':'title-product'})
        if title == None:
            nombre = "N/A"
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
            codigo = "N/A"
        else:            
            codigo = codigos.text.strip()[8:]
        #------Nombre del Producto-------#
        title = (soup.find('h1',{'class':'title-product'}))
        if title == None:
            nombre = "N/A"
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
            codigo = "N/A"
        else:            
            codigo = codigos.text.strip()
        #------Nombre del Producto-------#
        title = soup.find('h1',{'class':'product_title'})
        if title == None:
            nombre = "N/A"
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

def parseProd(jsonData,cat,store):
    product={}
    for i in jsonData:
        if isinstance(jsonData[i],dict):
            temp = parseProd(jsonData[i],format(cat+"-"+i),store)
            product.update(temp)
        else:
            codigos = jsonData.get("codigo")
            link = jsonData.get("link")
            if "-categorias-" in cat:
                cat.removesuffix(i).removeprefix("-categorias-")
            if codigos != None and link != None:
                product[codigos] = buscarProd(link,cat,store)
                #print(codigo + ": "+ link)
    print(cat)
    return product

        

def getProdInfo(soup,store,item):
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
            print(name)
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
                soup = getUrl(url)
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
                res = getUrl(url)
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
                if nextPage != None:
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


# Kemik
# Intelaf
# Click
# Funky
# Max
# Goat
# Elektra
# Spirit
# MacroSistemas
# TecnoFacil
# Pacifiko
# Zukko
# Guateclic
# Imeqmo
# Office Depot

file = open("C:/Users/javie/Desktop/ecommercescraper/testing.json","r")
product = json.load(file)
file.close()

today = date.today()
tienda = [i.strip() for i in product.keys()]
opcion = 0
print("Elige una opcion:")
file2 = open("C:/Users/javie/Desktop/ecommercescraper/res.json","r")
products = json.load(file2)
file2.close()

for i in range(0,len(tienda)):
    print(str(i+1),tienda[i])
ingreso = input("Escoge las tiendas que desee ver, presionando un numero separado por un espacio\n")
opciones = ingreso.split(" ")
for opcion in opciones:
    if int(opcion) < 16:
        store = tienda[int(opcion)-1]
        print(tienda[int(opcion)-1])
        products.update(parseProd(product[store],"",store))
        products["fechaAct"]= today.strftime("%d-%b-%Y")
    else:
        print(opcion + " no es una opcion valida, se ira a la siguiente")
else:
    print("Adios")

text = open("C:/Users/javie/Desktop/ecommercescraper/res.json","w")
json.dump(products,text)
text.close()
