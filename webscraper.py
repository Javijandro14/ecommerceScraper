# =============================================================== #
#             Project Name: WebScraping Website service           #
#               Author: Javier Alejandro Diaz Portillo            #
#   Descripcion: Programa sirve para extraer links necesarios,    #
#       y tambien para extaer los datos de cada productos         #
# =============================================================== #

# Mi forma de resolver este problema es hacer 2 tipos de archivos JSON: uno para conseguir los links, otra para los datos de productos #
from datetime import date
from bs4 import BeautifulSoup
import requests
import json
import time

#Fix the headers of the method, also add in sessions
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
 
#Edit
def buscarProd(link,cat,store):
    #Done
    if store == "Kemik":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'span','class','sku').text
        except:
            codigo = "N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'h1','class','product_title').text
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'div','class','old-price').contents[2].text.strip("Q")
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'div','id','price-after').contents[1].text.strip("Q")
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        detalles = []
        try:
            detalles.append(findItem(soup,'div','class','woocommerce-product-details__short-description'))
        except:
            pass
        try:
            detalles.append(findItem(soup,'div','id','prduct-long-description').ul.text.strip())
        except:
            pass
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        try:
            garantia = findItem(soup,'ul','class','kemik-ul-msg-container').li.next_sibling.next_sibling.text.lstrip()
        except:
            garantia = "N/A"
    elif store == "Intelaf":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'span','class','codigo').text[16:]
        except:
            codigo = "N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'h1',"class","descripcion_p").text
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'span','class','precio_normal').strong.text.replace("Q","")
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'span','class','beneficio_efectivo').text[20:]
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        try:
            detalles = []
            cuerpo = findItem(soup,'div','id','esp_tec')
            des = findItems(cuerpo,'p',None,None)
            detalles.extend([d.text for d in des])
        except:
            detalles = "No se encontro descripcion de este producto en particular"    
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        try:
            garantia = findItem(soup,'span','class','garantia').text[9:-1]
        except:
            garantia = "N/A"
    elif store == "Click":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        codigo = link[(link.find("id")+3):]           
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,"h2",None,None).text.strip() + ": " + findItem(soup,"h5",None,None).text.strip()
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'span','class','grey-text').text
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'span','class','red-text').text
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        try:
            detalles = findItem(soup,"div","class","card").text.replace("\n","")
        except:
            detalles = "N/A"
        #------Categorias-------#
        categoria = cat
        #------Garantias-------#
        try:
            garantia = "Cartuchos y Tinta: 0 meses, cables y adaptadores: 3 meses,drones varian y los demas productos se estima que son de 12 meses"
        except:
            garantia = "N/A"
    elif store == "Max":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup, 'div', 'itemprop', 'sku').text
        except:
            codigo ="N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup, 'h1', 'class', 'page-title').text.strip()
        except:
            nombre ="N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup, 'span', 'data-price-type', 'oldPrice').text.strip("Q")
        except:
            precio ="N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup, 'span', 'data-price-type', 'finalPrice').text.strip("Q")
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        detalles = []
        try:
            des = findItem(soup,'div','itemprop','description').text.strip()
        except:
            pass
        try:
            table = findItem(soup,'table','id','product-attribute-specs-table')
            rows = findItems(table,'td',"class","col data")
            detalles.extend([format(r["data-th"] + r.text) for r in rows])
        except:
            pass
        try:
            des = findItem(soup,'div','id','yt_tab_decription')
            parrafos = findItems(des,'p',None,None)
            descrip = [p.text.strip() for p in parrafos]
            descrip.remove(" ")
            descrip.remove("")
            detalles.extend(descrip)
        except:
            pass
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        try:
            if findItem(soup, 'td', 'data-th', 'garantía') != None:
                garantia = findItem(soup, 'td', 'data-th', 'garantía').text
            elif findItem(soup, 'td', 'data-th', 'Tiempo de garantía') != None:
                garantia = findItem(soup, 'td', 'data-th', 'Tiempo de garantía').text
            elif findItem(soup, 'td', 'data-th', 'Años de garantía totales') != None:
                garantia = findItem(soup, 'td', 'data-th', 'Años de garantía totales').text
            else:
                garantia = "N/A"
        except:
            garantia ="N/A"
    elif store == "Goat":
        send = requests.get(link, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        soup = BeautifulSoup(send.text,'html.parser')
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'span','class','sku').text.strip()
        except:
            codigo = "N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'h1','class','product_title').text.strip()
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'del',None,None).span.text.replace("Q","")
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'bdi',None,None).span.text.replace("Q","")
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        try:
            detalles = []
            des = findItem(soup,'div','class','woocommerce-product-details__short-description')
            punto = findItems(des,'li',None,None)
            detalles.extend([p.text.strip() for p in punto])
        except:
            detalles = "N/A"
        #------Categorias-------#
        categoria = (cat)
        #---------Garantias---------#
        garantia ="De acuerdo a la tienda, todos los productos tienen 1 año de garantia"
    elif store == "Spirit":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'div','class','sku').text.strip().replace("Código: ","")
        except:
            codigo ="N/A"
        #------Nombre del Producto-------#
        try:
            nombre = soup.find('h3',{'class':'title-product'})
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'span','class','PricesalesPrice').text.replace("Q ","")
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'div','class','cashprice').text[23:]
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        try:
            detalles = []
            descripcion = findItem(soup,'div','class','product-description')
            fila = findItems(descripcion,'p',None,None)
            detalles = [f.text.strip() for f in fila]
        except:
            detalles = "N/A"
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantia = "De acuerdo a la tienda, nos muestra que debe reportar alguna falla o daño del articulo en los 24 desde que se recibio el paquete"
    elif store == "Elektra":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'div','class','ektguatemala-ektgt-components-0-x-pdpSku').text.replace("SKU: ","")
        except:
            codigo = "N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'h1','class','vtex-store-components-3-x-productNameContainer').text
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'span','class','vtex-store-components-3-x-currencyContainer').span.text.replace("Q ","")
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'span','class','vtex-store-components-3-x-sellingPrice').span.span.text.replace("Q ","")
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        try:
            detalles = []
            detalles.append(findItem(soup,'div','class','vtex-store-components-3-x-productDescriptionText').text)
        except:
            pass
        #------Categorias-------#
        categoria = (cat)
        #---------Garantias---------#
        garantia = "De acuerdo a la tienda, todos los productos tienen 12 meses de garantia"
    elif store == "MacroSistemas":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'div','class','sku').text.strip()[8:]
        except:
            codigo = "N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'h1','class','title-product').text.strip()
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'span','class','PricesalesPrice').text.replace("Q ","")
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'div','class','cash').text[15:]
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        try:
            desTable = findItem(soup,'div','id','product-description-d')
            rows = findItems(desTable,'tr',None,None)
            detalles = [r.text.strip().replace("\n",": ") for r in rows]
        except:
            detalles = "N/A"
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantia = "N/A"
    elif store == "TecnoFacil":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'h6','class','sku').text
        except:
            codigo = "N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'div','class','product-name').text.strip()
        except:
            nombre = "N/A"
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
        try:
            detalles.append(findItem(soup,'div','class','std').text.strip())
        except:
            pass
        try:
            table = findItems(soup,'tr',None,None)
            details = [format(t.th.text+": " + t.td.text) for t in table]
            detalles.extend(details)
        except:
            pass
        #------Categorias-------#
        categoria = (cat)
        #------Garantias-------#
        garantia = "N/A"
    elif store == "Pacifiko":
        soup = getUrl(link)
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
        soup = getUrl(link)
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
        garantia = "De acuerdo a la tienda, El tiempo de gestión de tu garantía puede ser de 4 a 8 días hábiles después de recibir el producto físicamente"
    elif store == "Imeqmo":
        soup = getUrl(link)
        #------Codigo del Producto-------#
        try:
            codigo = findItem(soup,'p','class','mt-3').text
        except:
            codigo ="N/A"
        #------Nombre del Producto-------#
        try:
            nombre = findItem(soup,'div','class','deal-content').h3.text
        except:
            nombre = "N/A"
        #------Precio Viejo-------#
        try:
            precio = findItem(soup,'span','class','oe_default_price').span.text
        except:
            precio = "N/A"
        #------Precio de Ofertas-------#
        try:
            oferta = findItem(soup,'b','class','oe_price').span.text
        except:
            oferta = "N/A"
        #------Detalles de Productos-------#
        detalles = []
        detalles.append(findItem(soup,'p','class','te_prod_desc').text.replace("\n-",","))
        detalles.append(findItem(soup,'div','id','product_full_description').text.strip().replace("\n",""))
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        try:
            garantia= findItem(soup,'p','class','mt-3').next_sibling.next_sibling.text.replace("Garantía: ","")
        except:
            garantia = "N/A"
    elif store == "Office Depot":
        soup = getUrl(link)
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
        except:
            pass
        #------Categorias-------#
        categoria = cat
        #---------Garantias---------#
        garantia = "Revise la descripcion si muestra garantia"
    
    #Postponed
    elif store == "Zukko":
       pass
    elif store == "Funky":
        pass

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

def getCategorias(link,store,res,codigo):
    level0 = {}
    soup = getUrl(link)
    res1 = getProdInfo(soup,store,"cat")
    level1 = {}
    same = checkMenu(res,res1)
    if not res1 or same==True:#Si no tiene categorias, buscara paginacion y articulos
        pag = getProdInfo(link,store,"pag")
        for p in pag: #Lista links en la categorias
            soup = getUrl(p)
            res1 = getProdInfo(soup,store,"prod")
            if not res1: 
                print("no hay productos en " + p)
            else:
                codeProd = 0
                for r1 in res1:
                    name1 = getProdInfo(r1,store,"nameProd")
                    link1 = getProdInfo(r1,store,"linkProd")
                    codeProd +=1
                    #print(codigo+"{:02d}".format(codeProd))
                    level1[name1] = { "codigo": codigo+"{:02d}".format(codeProd),"link" : link1}
    else: # Si tiene categorias, buscara subcategorias
        res.extend(res1)
        code = 0
        for r1 in res1:
            name1 = getProdInfo(r1,store,"name").replace(" ","-")
            #print(name1)
            link1 = getProdInfo(r1,store,"linkCat")
            code+=1
            level1[name1] = getCategorias(link1,store,res,codigo+"{:02d}".format(code))
    level0 = level1  
    return level0

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
    


def parseProd(jsonData,cat,store):
    product={}
    if "-categorias-" in cat:
        cate = cat.removeprefix("-categorias-")
    else:
        cate = cat
    for i in jsonData:
        if isinstance(jsonData[i],dict):
            temp = parseProd(jsonData[i],format(cate+"-"+i),store)
            product.update(temp)
        else:
            codigos = jsonData.get("codigo")
            link = jsonData.get("link")
            if codigos != None and link != None:
                product[codigos] = buscarProd(link,cate.removesuffix(i),store)
                #print(codigo + ": "+ link)
    return product


def jsonFile(directory,action,jsonData):
    if action == "newCatJson":
        file = open(directory, 'w')
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
        return products
    elif action == "getJson":
        file = open(directory,"r")
        jsonData = json.load(file)
        file.close()
        return jsonData
    elif action == "writeJson":
        file = open(directory, 'w')
        json.dump(jsonData, file)
        file.close()



categories = jsonFile("C:/Users/javie/Desktop/ecommerceScraper/testing.json","getJson",None)
today = date.today()
tienda = [c.strip() for c in categories]
print("Webscraper comparison project")
opcion = 0
while opcion != 3:
    opcion = int(input("Seleccione una opcion:\n1.Conseguir las categorias y productos de una pagina \n2.Conseguir informacion de todos los productos de una pagina\n3.Salir\n"))
    if opcion == 1:
        #Menu to find Products
        print("Elige una opcion:")
        for i in range(0,len(tienda)):
            print(str(i+1),tienda[i])
        ingreso = input("Escoge las tiendas que desee ver, presionando un numero separado por un espacio\n")
        opciones = ingreso.split(" ")
        for o in opciones:
            if int(o) < 16:
                base = categories[tienda[int(o)-1]]["link"]
                store = tienda[int(o)-1]
                #print(base,store,today)
                categories[store]["categorias"] = getCategorias(base,store,[],"{:02d}".format(int(o)))
                categories[store]["fechaAct"]= today.strftime("%d-%b-%Y")
                jsonFile("C:/Users/javie/Desktop/ecommerceScraper/testing.json","writeJson",categories)
            else:
                print(o + " no es una opcion valida, se ira a la siguiente")

    elif opcion == 2:
        #Menu to find each product
        products = jsonFile("C:/Users/javie/Desktop/ecommerceScraper/res.json","getJson",None)
        
        for i in range(0,len(tienda)):
            print(str(i+1),tienda[i])
        ingreso = input("Escoge las tiendas que desee ver, presionando un numero separado por un espacio\n")
        opciones = ingreso.split(" ")
        for o in opciones:
            if int(o) < 16:
                store = tienda[int(o)-1]
                print(store)
                products.update(parseProd(categories[store],"",store))
                products["fechaAct"]= today.strftime("%d-%b-%Y")
                jsonFile("C:/Users/javie/Desktop/ecommerceScraper/res.json","writeJson",products)
            else:
                print(o + " no es una opcion valida, se ira a la siguiente")
    elif opcion == 3:
        print("Adios")
    else:
        print("Seleccione una opcion valida")




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