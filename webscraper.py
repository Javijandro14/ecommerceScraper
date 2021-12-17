from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import gc


def getUrl(url):
    try:
        send = requests.get(url,stream=True)
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
        print("Item Fallido: " + item)
    else:
        return result

def findItems(soup, item, attType, attName):
    try:
        result = soup.find_all(item, {attType: attName})
    except:
        print("error en la funcion 'findItems'")
        print("Item Fallido: " + item)
    else:
        return result

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

        # file = open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/intelaf/intelafJson.json",)
        # jsonData = json.load(file)
        # intentosExitosos = 0
        # intentosFallidos = 0

        # directory = 'C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/intelaf/intelafProducts.xlsx'
        # sheetName = []
        # df = []
        # for j in jsonData:
        # print("Current Category:" + format(j))
        # codigo = []
        # nombre = []
        # precio = []
        # oferta = []
        # categoria = []
        # detalles = []
        # garantia = []
        # for k in jsonData[j]:
        #     if isinstance(jsonData[j][k],dict):
        #         for l in jsonData[j][k]:
        #             if isinstance(jsonData[j][k][l],dict):
        #                 for m in jsonData[j][k][l]:
        #                     if isinstance(jsonData[j][k][l][m],dict):
        #                         for n in jsonData[j][k][l][m]:#jsonData[j][k][l][m][n]
        #                             try:
        #                                 link = jsonData[j][k][l][m][n]
        #                                 soup = getUrl(link)
        #                                 paginaProducto = findItem(soup,'div','class','row cuerpo')
        #                                 #------Codigo del Producto-------#
        #                                 codigos = findItem(paginaProducto,'p','class','codigo')
        #                                 if codigos == None:
        #                                     continue
        #                                 else:            
        #                                     codigo.append((codigos.text)[16:])
        #                                 #------Nombre del Producto-------#
        #                                 title = findItem(paginaProducto,'h1',None,None).text
        #                                 if title == None:
        #                                     continue
        #                                 else:
        #                                     nombre.append(title)
        #                                 #------Precio Viejo-------#
        #                                 precios = findItem(paginaProducto,'p','class','precio_normal')
        #                                 if precios == None:
        #                                     precios = "N/A"
        #                                     precio.append(precios)
        #                                 else:
        #                                     precio.append((precios.text)[17:])
        #                                 #------Precio de Ofertas-------#
        #                                 precioOferta = findItem(paginaProducto,'p','class','beneficio_efectivo')
        #                                 if precioOferta == None:
        #                                     continue
        #                                 else:
        #                                     oferta.append((precioOferta.text)[21:])
        #                                 #------Detalles de Productos-------#
        #                                 detalle = paginaProducto.find_all('div',attrs = {'id' :'c1' , 'class':'col-xs-12'})
        #                                 if detalle == None:
        #                                     detalle = "N/A"
        #                                     detalles.append(detalle)
        #                                 else:
        #                                     d = [i.text for i in detalle]
        #                                     detalles.append(""+format(d)+"")
        #                                 #------Categorias-------#
        #                                 categoria.append(format(j)+"-"+format(k)+"-"+format(l)+"-"+format(m)+"-"+format(n))
        #                                 #------Garantias-------#
        #                                 garantias = findItem(paginaProducto,'p','class','garantia')
        #                                 if garantias == None:
        #                                     garantias = "N/A"
        #                                     garantia.append(garantia)
        #                                 else:
        #                                     garantia.append(garantias.text[9:])
        #                             except:
        #                                 print(format(link) + " --> Status: Fallido!")
        #                                 intentosFallidos += 1
        #                             else:
        #                                 intentosExitosos += 1
        #                                 print(format(link) + " --> Status: Existoso!")
        #                                 soup.decompose()
        #                     else:#jsonData[j][k][l][m]
        #                         try:
        #                             link = jsonData[j][k][l][m]
        #                             soup = getUrl(link)
        #                             paginaProducto = findItem(soup,'div','class','row cuerpo')
        #                             #------Codigo del Producto-------#
        #                             codigos = findItem(paginaProducto,'p','class','codigo')
        #                             if codigos == None:
        #                                 continue
        #                             else:            
        #                                 codigo.append((codigos.text)[16:])
        #                             #------Nombre del Producto-------#
        #                             title = findItem(paginaProducto,'h1',None,None).text
        #                             if title == None:
        #                                 continue
        #                             else:
        #                                 nombre.append(title)
        #                             #------Precio Viejo-------#
        #                             precios = findItem(paginaProducto,'p','class','precio_normal')
        #                             if precios == None:
        #                                 precios = "N/A"
        #                                 precio.append(precios)
        #                             else:
        #                                 precio.append((precios.text)[17:])
        #                             #------Precio de Ofertas-------#
        #                             precioOferta = findItem(paginaProducto,'p','class','beneficio_efectivo')
        #                             if precioOferta == None:
        #                                 continue
        #                             else:
        #                                 oferta.append((precioOferta.text)[21:])
        #                             #------Detalles de Productos-------#
        #                             detalle = paginaProducto.find_all('div',attrs = {'id' :'c1' , 'class':'col-xs-12'})
        #                             if detalle == None:
        #                                 detalle = "N/A"
        #                                 detalles.append(detalle)
        #                             else:
        #                                 d = [i.text for i in detalle]
        #                                 detalles.append(""+format(d)+"")
        #                             #------Categorias-------#
        #                             categoria.append(format(j)+"-"+format(k)+"-"+format(l)+"-"+format(m))
        #                             #------Garantias-------#
        #                             garantias = findItem(paginaProducto,'p','class','garantia')
        #                             if garantias == None:
        #                                 garantias = "N/A"
        #                                 garantia.append(garantia)
        #                             else:
        #                                 garantia.append(garantias.text[9:])
        #                         except:
        #                             print(format(link) + " --> Status: Fallido!")
        #                             intentosFallidos += 1
        #                         else:
        #                             intentosExitosos += 1
        #                             print(format(link) + " --> Status: Existoso!")
        #                             soup.decompose()
        #             else:#jsonData[j][k][l]
        #                 try:
        #                     link = jsonData[j][k][l]
        #                     soup = getUrl(link)
        #                     paginaProducto = findItem(soup,'div','class','row cuerpo')
        #                     #------Codigo del Producto-------#
        #                     codigos = findItem(paginaProducto,'p','class','codigo')
        #                     if codigos == None:
        #                         continue
        #                     else:            
        #                         codigo.append((codigos.text)[16:])
        #                     #------Nombre del Producto-------#
        #                     title = findItem(paginaProducto,'h1',None,None).text
        #                     if title == None:
        #                         continue
        #                     else:
        #                         nombre.append(title)
        #                     #------Precio Viejo-------#
        #                     precios = findItem(paginaProducto,'p','class','precio_normal')
        #                     if precios == None:
        #                         precios = "N/A"
        #                         precio.append(precios)
        #                     else:
        #                         precio.append((precios.text)[17:])
        #                     #------Precio de Ofertas-------#
        #                     precioOferta = findItem(paginaProducto,'p','class','beneficio_efectivo')
        #                     if precioOferta == None:
        #                         continue
        #                     else:
        #                         oferta.append((precioOferta.text)[21:])
        #                     #------Detalles de Productos-------#
        #                     detalle = paginaProducto.find_all('div',attrs = {'id' :'c1' , 'class':'col-xs-12'})
        #                     if detalle == None:
        #                         detalle = "N/A"
        #                         detalles.append(detalle)
        #                     else:
        #                         d = [i.text for i in detalle]
        #                         detalles.append(""+format(d)+"")
        #                     #------Categorias-------#
        #                     categoria.append(format(j)+"-"+format(k)+"-"+format(l))
        #                     #------Garantias-------#
        #                     garantias = findItem(paginaProducto,'p','class','garantia')
        #                     if garantias == None:
        #                         garantias = "N/A"
        #                         garantia.append(garantia)
        #                     else:
        #                         garantia.append(garantias.text[9:])
        #                 except:
        #                     print(format(link) + " --> Status: Fallido!")
        #                     intentosFallidos += 1
        #                 else:
        #                     intentosExitosos += 1
        #                     print(format(link) + " --> Status: Existoso!")
        #                     soup.decompose()
        #     else:#jsonData[j][k]
        #         try:
        #             link = jsonData[j][k]
        #             soup = getUrl(link)
        #             paginaProducto = findItem(soup,'div','class','row cuerpo')
        #             #------Codigo del Producto-------#
        #             codigos = findItem(paginaProducto,'p','class','codigo')
        #             if codigos == None:
        #                 continue
        #             else:            
        #                 codigo.append((codigos.text)[16:])
        #             #------Nombre del Producto-------#
        #             title = findItem(paginaProducto,'h1',None,None).text
        #             if title == None:
        #                 continue
        #             else:
        #                 nombre.append(title)
        #             #------Precio Viejo-------#
        #             precios = findItem(paginaProducto,'p','class','precio_normal')
        #             if precios == None:
        #                 precios = "N/A"
        #                 precio.append(precios)
        #             else:
        #                 precio.append((precios.text)[17:])
        #             #------Precio de Ofertas-------#
        #             precioOferta = findItem(paginaProducto,'p','class','beneficio_efectivo')
        #             if precioOferta == None:
        #                 continue
        #             else:
        #                 oferta.append((precioOferta.text)[21:])
        #             #------Detalles de Productos-------#
        #             detalle = paginaProducto.find_all('div',attrs = {'id' :'c1' , 'class':'col-xs-12'})
        #             if detalle == None:
        #                 detalle = "N/A"
        #                 detalles.append(detalle)
        #             else:
        #                 d = [i.text for i in detalle]
        #                 detalles.append(""+format(d)+"")
        #             #------Categorias-------#
        #             categoria.append(format(j)+"-"+format(k))
        #             #------Garantias-------#
        #             garantias = findItem(paginaProducto,'p','class','garantia')
        #             if garantias == None:
        #                 garantias = "N/A"
        #                 garantia.append(garantia)
        #             else:
        #                 garantia.append(garantias.text[9:])
        #         except:
        #             print(format(link) + " --> Status: Fallido!")
        #             intentosFallidos += 1
        #         else:
        #             intentosExitosos += 1
        #             print(format(link) + " --> Status: Existoso!")
        #             soup.decompose()
        # productInfo = {
        #     "codigo": codigo,
        #     "nombre": nombre,
        #     "precio": precio,
        #     "oferta": oferta,
        #     "categoria": categoria,
        #     "detalles": detalles,
        #     "garantia": garantia
        # }
        # sheetName.append((format(j))[:29])#Hubo un error de pasar a una hoja excel porque excedia de los 31 caracteres, puse esto para todas las hojas excel
        # df.append(pd.DataFrame(productInfo, columns = ["codigo", "nombre", "precio","oferta", "categoria", "detalles", "garantia"]))
        # gc.collect()


        # writer = pd.ExcelWriter(directory, engine='xlsxwriter')
        # for i in range(1, len(df)):
        # df[i-1].to_excel(writer, sheetName[i-1])
        # writer.save()

        # print("Exitosos:" + format(intentosExitosos))
        # print("Fallidos:" + format(intentosFallidos))
        # print("Porcentaje de Exito:" + format(intentosExitosos /(intentosFallidos+intentosExitosos)))

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
        # base = "https://www.kemik.gt/"
        # soup = getUrl(base)
        # links_0 = soup.find_all('a')
        # for link0 in links_0:
        #     print(link0.get('href'))

    # Macrosistemas(Expandir para mas info)

    # Elektra(Expandir para mas info)

    # Tecnofacil(Expandir para mas info)

    # SpiritComputacion(Expandir para mas info)
# base = "https://spiritcomputacion.com"
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

file = open("maxJson.json",)
jsonData = json.load(file)

# categorias = menu.find_all('li',{'class':'parent'})
# subMenu = menu.find_all('ul',{'class':'unstyled'})

# #Nivel de Links
# links_0 = []
# links_1 = []
# links_2 = []

# #Listas de todos los articulos ingresados
# codigo = []
# nombre = []
# precio = []
# oferta = []
# detalles = []
# categoria = []
# garantia = []

# productInfo ={}

# for c in categorias:
#     link0 =(c.find('a')).get('href')
#     links_0.append(link0)
# for s in subMenu:
#     subCategorias = s.find_all('li')
#     for sc in subCategorias:
#         link1 = (sc.find('a')).get('href')
#         #print(link1)
#         links_1.append(link1)

# print("Url Lvl 0:" + format(len(links_0)))
# print("Url Lvl 1:" + format(len(links_1)))

# for link1 in links_1:
#     soup = getUrl(base+link1)
#     res = soup.find_all('a',{'class':'item-title'})
#     print("Url Lvl 2:" + format(len(links_2)))
#     for r in res:
#         #print(r.get('href'))
#         links_2.append(r.get('href'))

# print("Url Lvl 0:" + format(len(links_0)))
# print("Url Lvl 1:" + format(len(links_1)))
# print("Url Lvl 2:" + format(len(links_2)))

# intentosFallidos = 0
# intentosExistosos = 0

# for link2 in links_2:
#     try:
#         soup = getUrl(base+link2)
#         codigos = soup.find('div',{'class':'sku'})
#         titulo = soup.find('h3',{'class':'title-product'})
#         nombre.append(titulo.text)
#         #print(titulo.text)
#         precioO = soup.find('span',{'class':'PricesalesPrice'})
#         precioOferta = soup.find('div',{'class':'cashprice'})
#         #print((precioO.text)[2:])
#         precio.append(precioO.text[2:])
#         if precioOferta == None:
#             precioOferta = "N/A"
#             #print(precioOferta)
#             oferta.append(precioOferta)
#         else:
#             #print((precioOferta.text)[1:])
#             oferta.append((precioOferta.text)[22:])

#         descripcion = soup.find('div',{'class':'product-description'})
#         if descripcion == None:
#             descripcion = "N/A"
#             detalles.append(descripcion)
#         else:
#             #print((descripcion.text))
#             detalles.append(descripcion.text)

#         garantiaP = "N/A"
#         categoriaP = link2.split("/")
#         #print(categoriaP[2])
#         categoria.append(categoriaP[2])
#         garantia.append(garantiaP)
#     except:
#         print(link2 + " --> Status: Fallido!")
#         intentosFallidos+=1
#     else:
#         intentosExistosos+=1
#         codigo.append((codigos.text)[7:])
#         print(link2 + " --> Status: Existoso!")

# print("codigo: " + format(len(codigo)))
# print("nombre: " + format(len(nombre)))
# print("precio: " + format(len(precio)))
# print("oferta: " + format(len(oferta)))
# print("detalles: " + format(len(detalles)))
# print("categoria: " + format(len(categoria)))
# print("garantia: " + format(len(garantia)))

# print("Exitosos:" + format(intentosExistosos))
# print("Fallidos:" + format(intentosFallidos))
# print("Porcentaje de Exito:" + format(intentosExistosos/(intentosFallidos+intentosExistosos)))

        # productInfo = {
        #     "codigo" : codigo,
        #     "nombre" : nombre,
        #     "precio" : precio,
        #     "oferta" : oferta,
        #     "detalles" : detalles,
        #     "categoria" : categoria,
        #     "garantia" : garantia
        # }
        # try:
        #     df = pd.DataFrame(productInfo,columns=["codigo","nombre","precio","oferta","categoria","garantia"])
        #     df.to_excel(r'C:\Users\javie\Desktop\EcommerceWebscraper\SpiritCompProducts.xlsx')
        # except:
        #     print("No se exporto a excel, revise codigo")
        # else:
        #     print("Se proceso correctamente, mire si la informacion esta correcta")
    #No terminado

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

        ##
        ##file = open("maxJson.json",)
        ##jsonData = json.load(file)
        ### print(jsonData['Televisores'])
        ##intentosExitosos = 0
        ##intentosFallidos = 0
        ##
        ##directory = 'C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/max/MaxProducts.xlsx'
        ##sheetName = []
        ##df = []
        ##for j in jsonData:
        ##        codigo = []
        ##        nombre = []
        ##        precio = []
        ##        oferta = []
        ##        categoria = []
        ##        detalles = []
        ##        garantia = []
        ##    for k in jsonData[j]:
        ##
        ##        
        ##
        ##        for l in jsonData[j][k]:
        ##            link = jsonData[j][k][l]
        ##
        ##            try:
        ##                soup = getUrl(link)
        ##
        ##                #------Codigo del Producto-------#
        ##                codigos = findItem(soup, 'div', 'itemprop', 'sku')
        ##                if codigos == None:
        ##                    continue
        ##                else:            
        ##                    codigo.append(codigos.text)
        ##                #------Nombre del Producto-------#
        ##                title = findItem(soup, 'h1', 'class', 'page-title')
        ##                if title == None:
        ##                    continue
        ##                else:
        ##                    nombre.append(title.text)
        ##
        ##                #------Precio Viejo-------#
        ##                precios = findItem(soup, 'span', 'data-price-type', 'oldPrice')
        ##                if precios == None:
        ##                    precios = "N/A"
        ##                    precio.append(precios)
        ##                else:
        ##                    precio.append((precios.text)[1:])
        ##
        ##                #------Precio de Ofertas-------#
        ##                precioOferta = findItem(soup, 'span', 'data-price-type', 'finalPrice')
        ##                if precioOferta == None:
        ##                    continue
        ##                else:
        ##                    oferta.append((precioOferta.text)[1:])
        ##
        ##                #------Detalles de Productos-------#
        ##                detalle = findItems(soup, 'tr', None, None)
        ##                d = [i.text for i in detalle]
        ##                if detalles == None:
        ##                    detalles = "N/A"
        ##                else:
        ##                    detalles.append(""+format(d)+"")
        ##
        ##                #------Categorias-------#
        ##                categoria.append(format(j) + "/" + format(k))
        ##
        ##                #------Garantias-------#
        ##                garantias = findItem(soup, 'td', 'data-th', 'Garantía')
        ##                if garantias == None:
        ##                    garantias = "N/A"
        ##                    garantia.append(garantia)
        ##                else:
        ##                    garantia.append(garantias.text)
        ##            except:
        ##                print(link + " --> Status: Fallido!")
        ##                intentosFallidos += 1
        ##                break
        ##            else:
        ##                intentosExitosos += 1
        ##                print(link + " --> Status: Existoso!")
        ##                soup.decompose()
        ##
        ##    productInfo = {
        ##        "codigo": codigo,
        ##        "nombre": nombre,
        ##        "precio": precio,
        ##        "oferta": oferta,
        ##        "categoria": categoria,
        ##        "detalles": detalles,
        ##        "garantia": garantia
        ##    }
        ##    sheetName.append(format(j))
        ##    df.append(pd.DataFrame(productInfo, columns = ["codigo", "nombre", "precio","oferta", "categoria", "detalles", "garantia"]))
        ##    gc.collect()
        ##
        ##
        ##writer = pd.ExcelWriter(directory, engine='xlsxwriter')
        ##for i in range(1, len(df)):
        ##    df[i-1].to_excel(writer, sheetName[i-1])
        ##writer.save()
        ##
        ##print("Exitosos:" + format(intentosExitosos))
        ##print("Fallidos:" + format(intentosFallidos))
        ##print("Porcentaje de Exito:" + format(intentosExitosos /
        ##      (intentosFallidos+intentosExitosos)))
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

    #Zukko
    #base = "https://zukko.store/"

    #Funky
    #base = "https://storefunky.com/"

