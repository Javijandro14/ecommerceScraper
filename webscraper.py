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
                                            cat = format(j)+"-"+format(k)+"-"+format(l)+"-"+format(m)+"-"+format(n)
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
                                        cat = format(j)+"-"+format(k)+"-"+format(l)+"-"+format(m)
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
                                cat = format(j)+"-"+format(k)+"-"+format(l)
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
                        cat = format(j)+"-"+format(k)
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
                cat = format(j)+"-"+format(k)
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
    # Intelaf(Expandir para comentarios)
        # def getCategorias(menu):
        #     categorias = {}
        #     for info in menu:
        #         area = info['Area']
        #         url = info['url']
        #         categorias[area] = url
        #     return categorias

        # #Getting Json file
        # url = "https://www.intelaf.com/js/menu_productos22112021091955.json"
        # res = getUrl(url)
        # data = json.loads(res.text)
        # menu = data['menu_sub_1s']
        # categorias = getCategorias(menu)

        # base = "https://www.intelaf.com"
        # level0 = {}
        # for cat in categorias:
        #     print(cat)
        #     link = base + categorias[cat]
        #     soup = getUrl(link)
        #     res1 = findItems(soup,'a','class','hover_effect')
        #     if not res1:
        #         #level0[cat] = link  
        #         res1 = findItems(soup,'div','class','zoom_info')
        #         level1 = {}
        #         for r1 in res1:
        #             nombre = (findItem(r1,'button','class','btn_cotiza')).get('name')
        #             link = base + "/" + (findItem(r1,'button','class','btn_mas_info')).get('name')
        #             level1[nombre] = link
        #         level0[cat] = level1
        #     else:
        #         level1 = {}
        #         for r1 in res1:
        #             #print((findItem(r1,'div','class','image-area')).get('title'))
        #             link = base+ "/" + r1.get('href')
        #             soup = getUrl(link)
        #             res2 = findItems(soup,'a','class','hover_effect')
        #             if not res2:
        #                 res2 = findItems(soup,'div','class','zoom_info')
        #                 if not res2:
        #                     print("No hay productos en: " + r1.get('href'))
        #                 else:
        #                     level2 = {}
        #                     for r2 in res2:
        #                         nombre = (findItem(r2,'button','class','btn_cotiza')).get('name')
        #                         link = base + "/" + (findItem(r2,'button','class','btn_mas_info')).get('name')
        #                         level2[nombre] = link
        #                     level1[(findItem(r1,'div','class','image-area')).get('title')] = level2
        #             else:
        #                 level2 = {}
        #                 for r2 in res2:
        #                     #print(r2.text)
        #                     link = base + "/" + r2.get('href')
        #                     soup = getUrl(link)
        #                     res3 = findItems(soup,'a','class','hover_effect')
        #                     if not res3:
        #                         res3 = findItems(soup,'div','class','zoom_info')
        #                         if not res3:
        #                             print("No hay productos en: " + r2.get('href'))
        #                         else:
        #                             level3 = {}
        #                             for r3 in res3:
        #                                 nombre = (findItem(r3,'button','class','btn_cotiza')).get('name')
        #                                 link = base + "/" + (findItem(r3,'button','class','btn_mas_info')).get('name')
        #                                 level3[nombre] = link
        #                         level2[r2.text] = level3    
        #                     else:
        #                         level3 = {}
        #                         for r3 in res3:
        #                             #print(r3.text)
        #                             link = base + "/" + r3.get('href')
        #                             soup = getUrl(link)
        #                             res4 = findItems(soup,'div','class','zoom_info')
        #                             if not res4:
        #                                 print("No hay productos en: " + r3.get('href'))
        #                             else:
        #                                 level4 = {}
        #                                 for r4 in res4:
        #                                     nombre = (findItem(r4,'button','class','btn_cotiza')).get('name')
        #                                     link = base + "/" + (findItem(r4,'button','class','btn_mas_info')).get('name')
        #                                     level4[nombre] = link
        #                                 level3[r3.text] = level4
        #                         level2[r2.text] = level3
        #                 level1[(findItem(r1,'div','class','image-area')).get('title')] = level2
        #         level0[cat] = level1  

        # #Se imprime 2 archivos, uno de texto y otro JSON, solo es de preuba el de txt, para ver que si nos sale el resultado deseado, la que nos importa seria JSON
        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/intelaf/intelafJson.json",'w') as file:
        #     json.dump(level0,file)
        # file.close()
        #Cerramos este fragmento de codigo porque lo queremos volver como funcion si es posible, porque queremos dar la opcion de solo analizar los links
        #y de ponerlo en un archivo por separado y no tener que consultar cada vez que se entra a la pagina

file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/intelaf/intelafJson.json",)
jsonData = json.load(file)
products = data(jsonData,"Intelaf")
with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/intelaf/IntelafProducts.json",'w') as file:
    json.dump(products,file)
file.close()

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

    # Click(Expandir para mas info)
        # base = "https://www.click.gt"
        # soup = getUrl(base)
        # menu = findItem(soup,'ul','class',['justify-content-center','container','d-flex','align-items-center','mb-0','mt-0','pr-4'])
        # list = findItems(menu,'a','class',['nav-link','waves-effect','waves-light'])
        # cat = []
        # for l in list:
        #     if l.get('id')== None:
        #         pass
        #     else:
        #         cat.append(l.get('id'))
        # cat.append('otro')
        # level0 = {}
        # categorias = []
        # for c in cat:
        #     level1 = {}
        #     if c != 'otro':
        #         ul = findItem(menu,'div','aria-labelledby',c)
        #         listar = findItems(ul,'li',None,None)
        #         for l in listar:
        #             links_1 = []
        #             l1 = (findItem(l,'a',None,None)).text
        #             l2 = base + (findItem(l,'a',None,None)).get('href')
        #             soup = getUrl(l2)
        #             pagination = soup.find_all('button', {'class': 'page-link'})
        #             if len(pagination) == 0:
        #                 res = l2
        #                 #print(l2)
        #                 links_1.append(res)
        #             elif len(pagination) == 2:
        #                 paginas = int(pagination[0].text)
        #                 for i in range(1, paginas+1):
        #                     res = l2+"?page="+format(i)
        #                     #print(l2+"?page="+format(i))
        #                     links_1.append(res)
        #             elif len(pagination) == 3:
        #                 paginas = int(pagination[-2].text)
        #                 for i in range(1, paginas+1):
        #                     res = l2+"?page="+format(i)
        #                     #print(l2+"?page="+format(i))
        #                     links_1.append(res)
        #             else:
        #                 paginas = int(pagination[-2].text)
        #                 for i in range(1, paginas+1):
        #                     res = l2+"?page="+format(i)
        #                     #print(l2+"?page="+format(i))
        #                     links_1.append(res)
        #             level1[l1] = links_1
        #         level0[c] = level1
        #     else:
        #         for li in list:
        #             links_1 = []
        #             if li.get('href') == None:
        #                 continue
        #             else:
        #                 if "\n" in li.text:
        #                     l1 = str(li.get('href')).replace("/productos/","")
        #                 else:
        #                     l1 = li.text
        #                 l2 = base + li.get('href')
        #                 soup = getUrl(l2)
        #                 pagination = findItems(soup,'button','class','page-link')
        #                 if len(pagination) == 0:
        #                     res = l2
        #                     #print(l2)
        #                     links_1.append(res)
        #                 elif len(pagination) == 2:
        #                     paginas = int(pagination[0].text)
        #                     for i in range(1, paginas):
        #                         res = l2+"?page="+format(i)
        #                         #print(l2+"?page="+format(i))
        #                         links_1.append(res)
        #                 elif len(pagination) == 3:
        #                     paginas = int(pagination[-2].text)
        #                     for i in range(1, paginas):
        #                         res = l2+"?page="+format(i)
        #                         #print(l2+"?page="+format(i))
        #                         links_1.append(res)
        #                 else:
        #                     paginas = int(pagination[-2].text)
        #                     for i in range(1, paginas):
        #                         res = l2+"?page="+format(i)
        #                         #print(l2+"?page="+format(i))
        #                         links_1.append(res)
        #                 level1[l1] = links_1
        #             level0[c] = level1
                    
        # for l0 in level0:
        #     level2 = {}
        #     for l1 in level0[l0]:
        #         links_2 = level0[l0][l1]
        #         for link2 in links_2:
        #             soup = getUrl(link2)
        #             print(link2)
        #             productos = findItems(soup,'div','class','col-lg-3')
        #             for p in productos:
        #                 n1 = findItem(p,'h5',None,None)
        #                 n2 = findItem(p,'textarea',None,None)
        #                 if n1 == None or n2 == None:
        #                     continue
        #                 else:
        #                     nombre = n1.text + "-" +n2.text
        #                     #print(nombre)
        #                     link = (findItem(p,'a',None,None)).get('href')
        #                     #print(link)
        #                     level2[nombre] = base + link
        #         level0[l0][l1] = level2
        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/click/clickJson.json",'w') as file:
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
    #Terminado

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
    # Macrosistemas(Expandir para mas info)

        #base = "https://www.macrosistemas.com"
        # soup = getUrl(base)
        # menu = findItem(soup,'ul','id','menu_footer')
        # categorias = findItems(menu,'a',None,None)
        # level0 = {}
        # for cat in categorias:
        #     name0 = cat.text
        #     link0 = base + format(cat.get('href'))
        #     soup = getUrl(link0)
        #     leftmenu = soup.find('ul',{'id':'menu_left'})
        #     level1 = {}
        #     if leftmenu == None:
        #         divpag = findItem(soup,'div','class','vm-pagination')
        #         if divpag == None:
        #             numeroPag = 1
        #         else:
        #             paginacion = findItem(divpag,'span','class','vm-page-counter')
        #             if paginacion.text=="":
        #                 numeroPag = 1
        #             else:
        #                 numeroPag = int(paginacion.text[-2:])
        #         links_2 = []
        #         for pag in range(1,(numeroPag+1)):
        #             if pag == 1:
        #                 links_2.append(format(link0)+"?start=0")
        #             elif pag >1:
        #                 links_2.append(format(link0)+"?start="+str((pag-1)*24))
                
        #         for link2 in links_2:
        #             soup = getUrl(link2)
        #             productos = findItems(soup,'div','class','product-inner')    
        #             for p in productos:
        #                 item = findItem(p,'a','class','item-title')
        #                 level1[item.text.strip()] = base + item.get('href')
        #     else:
        #         subcat = leftmenu.find_all('li')
        #         for sub in subcat:
        #             name1 = sub.text.strip()
        #             link1 = base + (findItem(sub,'a',None,None).get('href'))
        #             soup = getUrl(link1)
        #             divpag = findItem(soup,'div','class','vm-pagination')
        #             if divpag == None:
        #                 numeroPag = 1
        #             else:
        #                 paginacion = findItem(divpag,'span','class','vm-page-counter')
        #                 if paginacion.text=="":
        #                     numeroPag = 1
        #                 else:
        #                     numeroPag = int(paginacion.text[-2:])
        #             links_2 = []
        #             for pag in range(1,(numeroPag+1)):
        #                 if pag == 1:
        #                     links_2.append(format(link0)+"?start=0")
        #                 elif pag >1:
        #                     links_2.append(format(link0)+"?start="+str((pag-1)*24))
                    
        #             level2 = {}
        #             for link2 in links_2:
        #                 soup = getUrl(link2)
        #                 productos = findItems(soup,'div','class','product-inner')    
        #                 for p in productos:
        #                     item = findItem(p,'a','class','item-title')
        #                     level2[item.text.strip()] = base + item.get('href')
        #             level1[name1] = level2
        #     level0[name0] = level1
        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/macrosistemas/macroJson.json",'w') as file:
        #     json.dump(level0,file)
        # file.close()

        # file = open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/macrosistemas/macroJson.json",)
        # jsonData = json.load(file)
        # intentosFallidos = 0
        # intentosExistosos = 0
        # directory = 'C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/macrosistemas/macroProducts.xlsx'
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
        #         if isinstance(jsonData[j][k],dict):
        #             for l in jsonData[j][k]:
        #                 try:
        #                     soup = getUrl(jsonData[j][k][l])
        #                     #------Codigo del Producto-------#
        #                     codigos = (soup.find('div',{'class':'sku'}))
        #                     if codigos == None:
        #                         continue
        #                     else:            
        #                         codigo.append(codigos.text.strip()[8:])
        #                     #------Nombre del Producto-------#
        #                     title = (soup.find('h1',{'class':'title-product'}))
        #                     if title == None:
        #                         continue
        #                     else:
        #                         nombre.append(title.text.strip())
        #                     #------Precio Viejo-------#
        #                     precioO = (soup.find('span',{'class':'PricesalesPrice'})).text.strip()
        #                     precio.append(precioO)
        #                     #------Precio de Ofertas-------#
        #                     precioOferta = soup.find('div',{'class':'cash'})
        #                     if precioOferta == None:
        #                         precioOferta = "N/A"
        #                         oferta.append(precioOferta)
        #                     else:
        #                         oferta.append(precioOferta.text.strip()[13:])
        #                     #------Detalles de Productos-------#
        #                     des = soup.find('div',{'class':'product-description'})
        #                     if des == None:
        #                         descripcion = "N/A"
        #                         detalles.append(descripcion)
        #                     else:
        #                         descripcion = des.find_all('tr')
        #                         detalles.append([(i.text.strip()) for i in descripcion])
        #                     #------Categorias-------#
        #                     categoria.append(format(j)+"-"+format(k))
        #                     #---------Garantias---------#
        #                     garantiaP = "N/A"
        #                     garantia.append(garantiaP)
        #                 except:
        #                     print(format(jsonData[j][k][l]) + " --> Status: Fallido!")
        #                     intentosFallidos+=1
        #                 else:
        #                     intentosExistosos+=1
        #                     print(format(jsonData[j][k][l]) + " --> Status: Existoso!")
        #                     soup.decompose()
        #         else:
        #             try:
        #                 soup = getUrl(jsonData[j][k])
        #                 #------Codigo del Producto-------#
        #                 codigos = (soup.find('div',{'class':'sku'}))
        #                 if codigos == None:
        #                     continue
        #                 else:            
        #                     codigo.append(codigos.text.strip()[8:])
        #                 #------Nombre del Producto-------#
        #                 title = (soup.find('h1',{'class':'title-product'}))
        #                 if title == None:
        #                     continue
        #                 else:
        #                     nombre.append(title.text.strip())
        #                 #------Precio Viejo-------#
        #                 precioO = (soup.find('span',{'class':'PricesalesPrice'})).text.strip()
        #                 precio.append(precioO)
        #                 #------Precio de Ofertas-------#
        #                 precioOferta = soup.find('div',{'class':'cash'})
        #                 if precioOferta == None:
        #                     precioOferta = "N/A"
        #                     oferta.append(precioOferta)
        #                 else:
        #                     oferta.append(precioOferta.text.strip()[13:])
        #                 #------Detalles de Productos-------#
        #                 des = soup.find('div',{'class':'product-description'})
        #                 if des == None:
        #                     descripcion = "N/A"
        #                     detalles.append(descripcion)
        #                 else:
        #                     descripcion = des.find_all('tr')
        #                     detalles.append([(i.text.strip()) for i in descripcion])
        #                 #------Categorias-------#
        #                 categoria.append(format(j)+"-"+format(k))
        #                 #---------Garantias---------#
        #                 garantiaP = "N/A"
        #                 garantia.append(garantiaP)
        #             except:
        #                 print(format(jsonData[j][k]) + " --> Status: Fallido!")
        #                 intentosFallidos+=1
        #             else:
        #                 intentosExistosos+=1
        #                 print(format(jsonData[j][k]) + " --> Status: Existoso!")
        #                 soup.decompose()
        #     productInfo = {
        #         "codigo": codigo,
        #         "nombre": nombre,
        #         "precio": precio,
        #         "oferta": oferta,
        #         "categoria": categoria,
        #         "detalles": detalles,
        #         "garantia": garantia
        #     }
        #     sheetName.append(format(j).replace(" / ","_"))
        #     df.append(pd.DataFrame(productInfo, columns = ["codigo", "nombre", "precio","oferta", "categoria", "detalles", "garantia"]))
        #     gc.collect()

        # writer = pd.ExcelWriter(directory, engine='xlsxwriter')
        # for i in range(1, len(df)):
        #    df[i-1].to_excel(writer, sheetName[i-1])
        # writer.save()
        # print("Exitosos:" + format(intentosExistosos))
        # print("Fallidos:" + format(intentosFallidos))
        # print("Porcentaje de Exito:" + format(intentosExistosos/(intentosFallidos+intentosExistosos)))
    #Terminado

    # Elektra(Expandir para mas info)
        #base = "https://www.elektra.com.gt"
        # soup = getUrl(base)
        # categorias = findItems(soup,'div','class','vtex-store-components-3-x-infoCardTextContainer--homeImgCategorias')
        # level0 = {}
        # for cat in categorias:
        #     name0 = cat.text
        #     link0 = findItem(cat,'a',None,None).get('href')
        #     soup = getUrl(base + link0)
        #     level1 = {}
        #     nextPage = soup.find('div',{'class':'vtex-search-result-3-x-buttonShowMore--layout'})
        #     iter = 1

        #     while iter!=0:
        #         link = format(base + link0) +"?page="+ str(iter)
        #         soup = getUrl(link)
        #         productos = findItems(soup,'section','class','vtex-product-summary-2-x-container')
        #         for p in productos:
        #             name1 = findItem(p,'h1',None,None).text.strip()
        #             link1 = findItem(p,'a',None,None).get('href')
        #             level1[name1] = base + link1
        #         nextPage = soup.find('div',{'class':'vtex-search-result-3-x-buttonShowMore--layout'})
        #         if nextPage == None:
        #             iter = 0
        #         else:
        #             if nextPage.text == '':
        #                 iter = 0
        #             else:
        #                 iter+=1
        #     level0[name0] = level1
        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/elektra/elektraJson.json",'w') as file:
        #     json.dump(level0,file)
        # file.close()

        # file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/elektra/elektraJson.json",)
        # jsonData = json.load(file)
        # products = data(jsonData,"Elektra")
        # with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/elektra/elektraProducts.json",'w') as file:
        #     json.dump(products,file)
        # file.close()
    #Terminado

    # Tecnofacil(Expandir para mas info)
    #No terminado

    # SpiritComputacion(Expandir para mas info)
        #base = "https://spiritcomputacion.com"
        # soup = getUrl(base)
        # categorias = findItems(soup,'li','class',['vm-categories-wall-catwrapper','floatleft','width25'])
        # level0 = {}
        # for cat in categorias:
        #     name0 = (findItem(cat,'a',None,None).text).strip("\n")
        #     link0 = (findItem(cat,'a',None,None).get('href'))
        #     soup = getUrl(base + link0)
        #     res0 = findItems(soup,'div','class','spacer')
        #     level1 = {}
        #     for r0 in res0:
        #         name1 = (findItem(r0,'a',None,None).get('title'))
        #         link1 = (findItem(r0,'a',None,None).get('href'))
        #         soup = getUrl(base+link1)
        #         div = findItem(soup,'div','class',['vm-pagination','vm-pagination-bottom'])
        #         paginacion = findItems(div,'li',None,None)
        #         level2={}
        #         if not paginacion:
        #             soup = getUrl(base+link1)
        #             res = soup.find_all('a',{'class':'item-title'})
        #             for r in res:
        #                 name2 = r.text
        #                 link2 = r.get('href')
        #                 level2[name2] = link2
        #         else:
        #             for p in paginacion[2:-3]:
        #                 a = findItem(p,'a',None,None)
        #                 if a == None:
        #                     soup = getUrl(base+link1)
        #                     res = soup.find_all('a',{'class':'item-title'})
        #                     for r in res:
        #                         name2 = r.text
        #                         link2 = r.get('href')
        #                         level2[name2] = link2
        #                 else:
        #                     soup = getUrl(base+a.get('href'))
        #                     res = soup.find_all('a',{'class':'item-title'})
        #                     for r in res:
        #                         name2 = r.text
        #                         link2 = r.get('href')
        #                         level2[name2] = link2
        #         level1[name1] = level2        
        #     level0[name0] = level1

        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/spiritcomputacion/spiritJson.json",'w') as file:
        #     json.dump(level0,file)
        # file.close()

        # file = open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/spiritcomputacion/spiritJson.json",)
        # jsonData = json.load(file)

        # intentosFallidos = 0
        # intentosExistosos = 0
        # directory = 'C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/spiritcomputacion/spiritProducts.xlsx'
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
        #             try:
        #                 soup = getUrl(base+jsonData[j][k][l])
        #                 #------Codigo del Producto-------#
        #                 codigos = findItem(soup,'div','class','sku')
        #                 if codigos == None:
        #                     continue
        #                 else:            
        #                     codigo.append((codigos.text)[7:])
        #                 #------Nombre del Producto-------#
        #                 title = soup.find('h3',{'class':'title-product'})
        #                 if title == None:
        #                     continue
        #                 else:
        #                     nombre.append(title.text)
        #                 #------Precio Viejo-------#
        #                 precioO = soup.find('span',{'class':'PricesalesPrice'})
        #                 precio.append(precioO.text[2:])
        #                 #------Precio de Ofertas-------#
        #                 precioOferta = soup.find('div',{'class':'cashprice'})
        #                 if precioOferta == None:
        #                     precioOferta = "N/A"
        #                     oferta.append(precioOferta)
        #                 else:
        #                     oferta.append((precioOferta.text)[22:])
        #                 #------Detalles de Productos-------#
        #                 descripcion = soup.find('div',{'class':'product-description'})
        #                 if descripcion == None:
        #                     descripcion = "N/A"
        #                     detalles.append(descripcion)
        #                 else:
        #                     detalles.append(descripcion.text)
        #                 #------Categorias-------#
        #                 categoria.append(format(k)+"-"+format(l))
        #                 #---------Garantias---------#
        #                 garantiaP = "N/A"
        #                 garantia.append(garantiaP)
        #             except:
        #                 print(format(base+jsonData[j][k][l]) + " --> Status: Fallido!")
        #                 intentosFallidos+=1
        #             else:
        #                 intentosExistosos+=1
        #                 print(format(base+jsonData[j][k][l]) + " --> Status: Existoso!")
        #                 soup.decompose()
        #     productInfo = {
        #         "codigo": codigo,
        #         "nombre": nombre,
        #         "precio": precio,
        #         "oferta": oferta,
        #         "categoria": categoria,
        #         "detalles": detalles,
        #         "garantia": garantia
        #     }
        #     sheetName.append(format(j))
        #     df.append(pd.DataFrame(productInfo, columns = ["codigo", "nombre", "precio","oferta", "categoria", "detalles", "garantia"]))
        #     gc.collect()

        # writer = pd.ExcelWriter(directory, engine='xlsxwriter')
        # for i in range(1, len(df)):
        #    df[i-1].to_excel(writer, sheetName[i-1])
        # writer.save()
        # print("Exitosos:" + format(intentosExistosos))
        # print("Fallidos:" + format(intentosFallidos))
        # print("Porcentaje de Exito:" + format(intentosExistosos/(intentosFallidos+intentosExistosos)))
    #Terminado

    # Max(Expandir para mas info)
        # Aqui estamos buscando todos los links que se haya posible, en algunas paginas no tienen JSON files, entonces este fragemento busca links y luego
        # lo vamos a meter en varios diccionarios para luego hacer nuestro propio archivo JSON, esto es porque se nos hace mas facil hacerlo de esta forma que hacer todo junto
        # ya que si consume bastante memoria buscar todos los datos de las paginas

        # base = "https://www.max.com.gt"
        # soup = getUrl(base)
        # menu = findItem(soup,'div','class','content-mega')
        # cat = findItems(menu,'li','class','level2')
        # categorias = [(findItem(c,'a',None,None)) for c in cat]
        # products ={}
        # level0 = { }#Categoria Principal
        # for c in categorias:
        #     soup = getUrl(c.get('href'))
        #     subcategorias = findItem(soup,'ul','class',['sub-cat-list' ,'slick-initialized' ,'slick-slider'])
        #     list = findItems(subcategorias,'li',None,None)
        #     res = [(findItem(i,'a',None,None)) for i in list] #no poner text o get('href'), llamar funcion si necesario
        #     if None in res:
        #         level0[(c.text).strip()] = c.get('href') #Algunos no tienen sub categorias, entocnes se pone su link original
        #     else:
        #         level0[(c.text).strip()] = res

        # for m in level0:
        #     links_0 = level0[m]
        #     level1 = {} #Subcategoria de cada Categoria
        #     for link0 in links_0:
        #         try:
        #             soup = getUrl(link0.get('href'))
        #             noProductos = int((findItem(soup,'span','class','toolbar-number').text)[:-10])
        #             print("No productos: " + format(noProductos))
        #             paginas = 0
        #             if noProductos >= 30:
        #                 paginas = noProductos//30
        #             else:
        #                 paginas = 0
        #             if (noProductos % 30) >= 1:
        #                 paginas += 1
        #             level2 = {}
        #             for iter in range(1,paginas+1):
        #                 link = (format(link0.get('href'))+"?p=" + format(iter) + "&product_list_limit=30")
        #                 soup = getUrl(link)
        #                 links = findItems(soup,'a','class','product-item-link')
        #                 for l in links:
        #                     # l.text es nivel2 y l.get('href') es nivel 3, que son Nombres de productos y links
        #                     level2[(l.text).strip()] = l.get('href')
        #                 level1[link0.text] = level2
        #             print("Productos agregados:" + format(len(level2)))
        #             #area[link0.text] = level1
        #         except:
        #             print("Hubo un error, puede ser que la url este mal o no hay productos")
        #             print("Url fallido:" + link0.get('href'))
        #     products[m] = level1

        # #Se imprime 2 archivos, uno de texto y otro JSON, solo es de preuba el de txt, para ver que si nos sale el resultado deseado, la que nos importa seria JSON
        # # file =open("newfile.txt",mode="w",encoding="utf-8")
        # # file.write(products)
        # # file.close()
        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/max/maxJson.json",'w') as file:
        #     json.dump(products,file)
        # file.close()
        # # Cerramos este fragmento de codigo porque lo queremos volver como funcion si es posible, porque queremos dar la opcion de solo analizar los links
        # # y de ponerlo en un archivo por separado y no tener que consultar cada vez que se entra a la pagina

        # file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/max/maxJson.json",)
        # jsonData = json.load(file)
        # products = data(jsonData,"Max")
        # with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/max/maxProducts.json",'w') as file:
        #     json.dump(products,file)
        # file.close()
    #Terminado

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

    #GoatShop
        #base = "https://goatshopgt.com/"
        # send = requests.get(format(base)+"tienda/", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        # soup = BeautifulSoup(send.text,'html.parser')
        # categorias = soup.find_all('div',{'class':['woocommerce','columns-1']})
        # level0 = {}
        # for cat in categorias[:-1]:
        #     name0 = cat.find('h2',{'class':'woocommerce-loop-category__title'})
        #     link0 = cat.find('a').get('href')
        #     send = requests.get(link0, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        #     soup = BeautifulSoup(send.text,'html.parser')
        #     productos = soup.find_all('li',{'class':'ast-grid-common-col'})
        #     level1 = {}
        #     for p in productos:
        #         name1 = p.find('h2',{'class':'woocommerce-loop-product__title'}).text
        #         link1 = p.find('a',{'class':'ast-loop-product__link'})
        #         level1[name1] = link1.get('href')
        #     level0[name0.contents[0].strip()] = level1

        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/goatshop/goatshopJson.json",'w') as file:
        #     json.dump(level0,file)
        # file.close()

        # file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/goatshop/goatshopJson.json",)
        # jsonData = json.load(file)
        # products = data(jsonData,"Goat")
        # with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/goatshop/goatshopProducts.json",'w') as file:
        #     json.dump(products,file)
        # file.close()

    #Terminado

    #Zukko
        #base = "https://zukko.store/"
        #soup = getUrl("https://app.ecwid.com/categories.js?ownerid=50367225&lang=es_419&jsonp=menu.fill")
    #No terminado
    #Funky
        # base = "https://storefunky.com/"
        # soup = getUrl(base)
        # menu = soup.find('ul',{'class':'sub-menu'})
        # categorias = menu.find_all('li')
        # level0 ={}
        # for cat in categorias:
        #     name0 = cat.text
        #     link0 = cat.a.get('href')
        #     soup = getUrl(link0)
        #     lista = findItem(soup,'ul','class','tablet-columns-2')
        #     level1 = {}
        #     if lista==None:
        #         continue
        #     else:
        #         productos = findItems(lista,'div','class','product-loop-content text-center')
                
        #         for p in productos:
        #             name1 = p.h2.text.strip()
        #             link1 = p.h2.a.get('href')
        #             level1[name1] = link1
        #         level0[name0] = level1

        # with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/funky/funkyJson.json",'w') as file:
        #     json.dump(level0,file)
        # file.close()

        # file = open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/funky/funkyJson.json",)
        # jsonData = json.load(file)

        # intentosFallidos = 0
        # intentosExistosos = 0
        # directory = 'C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/funky/funkyProducts.xlsx'
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
        #         try:
        #             send = requests.get(jsonData[j][k], headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        #             soup = BeautifulSoup(send.text,'html.parser')
        #             #------Codigo del Producto-------#
        #             codigos = findItem(soup,'span','class','sku')
        #             if codigos == None:
        #                 continue
        #             else:            
        #                 codigo.append(codigos.text.strip())
        #             #------Nombre del Producto-------#
        #             title = soup.find('h1',{'class':'product_title'})
        #             if title == None:
        #                 codigo.remove(codigos.text.strip())
        #                 continue
        #             else:
        #                 nombre.append(title.text)
        #             #------Precio Viejo-------#
        #             precioO = soup.find('del')
        #             if precioO == None:
        #                 precioO="N/A"
        #                 precio.append(precioO)
        #             else:
        #                 precio.append(precioO.text)
        #             #------Precio de Ofertas-------#
        #             precioOferta = soup.find('bdi')
        #             if precioOferta == None:
        #                 precioOferta = "N/A"
        #                 oferta.append(precioOferta)
        #             else:
        #                 oferta.append(precioOferta.text)
        #             #------Detalles de Productos-------#
        #             descripcion = soup.find('div',{'class':'woocommerce-product-details__short-description'})
        #             if descripcion == None:
        #                 descripcion = "N/A"
        #                 detalles.append(descripcion)
                        
        #             else:
        #                 detalles.append(descripcion.text.strip())
        #             #------Categorias-------#
        #             categoria.append(format(j))
        #             #---------Garantias---------#
        #             garantiaP = "N/A"
        #             garantia.append(garantiaP)
        #         except:
        #             print(format(jsonData[j][k]) + " --> Status: Fallido!")
        #             intentosFallidos+=1
        #         else:
        #             intentosExistosos+=1
        #             print(format(jsonData[j][k]) + " --> Status: Existoso!")
                    
        #     productInfo = {
        #         "codigo": codigo,
        #         "nombre": nombre,
        #         "precio": precio,
        #         "oferta": oferta,
        #         "categoria": categoria,
        #         "detalles": detalles,
        #         "garantia": garantia
        #     }
        #     sheetName.append(j)
        #     df.append(pd.DataFrame(productInfo, columns = ["codigo", "nombre", "precio","oferta", "categoria", "detalles", "garantia"]))
        #     soup.decompose()
        #     gc.collect()

        # writer = pd.ExcelWriter(directory, engine='xlsxwriter')
        # for i in range(1, len(df)+1):
        #     df[i-1].to_excel(writer, sheetName[i-1])
        # writer.save()

        # print("Exitosos:" + format(intentosExistosos))
        # print("Fallidos:" + format(intentosFallidos))
        # print("Porcentaje de Exito:" + format(intentosExistosos/(intentosFallidos+intentosExistosos)))
    #Terminado (Falta poner paginaciones, debido a los pocos articulos que tiene)

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
