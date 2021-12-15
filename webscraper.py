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
        # Para la pagina de intelaf, se ve que consiste en el link siendo la URL original, seguido de un link que termina en .aspx, luego el codigo del producto
        # cuando se trata de una categoria, puede que se tiene que agregar algo mas para que veamos los productos del mismo
        # def getJson():
        #     url = "https://www.intelaf.com/js/menu_productos22112021091955.json"
        #     try:
        #         request = requests.Session()
        #         res = request.get(url)
        #     except:
        #         print("Error en la clase 'getJson()'")
        #         print("Url Fallido:"+ url)
        #     else:
        #         data = json.loads(res.text)
        #         menu = data['menu_sub_1s']
        #         return menu

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

        # def nivel0(url):
        #     try:
        #         soup = getUrl(url)
        #         menu = soup.find_all('a')
        #     except:
        #         print("hubo un error en clase 'Nivel0'")
        #         print("Url Fallido:" + url)
        #     else:
        #         temp = []
        #         for i in menu:
        #             if 'Menu_areas.aspx?' in i.get('href') and ("nivel=1" in i.get('href') or "Nivel=1" in i.get('href')):
        #                     temp.append(i.get('href'))
        #         return temp

        # def nivel1(url):
        #     try:
        #         soup = getUrl(url)
        #         menu = soup.find_all('a')
        #     except:
        #         print("hubo un error en clase 'Nivel1'")
        #         print("Url Fallido:" + url)
        #     else:
        #         temp = []
        #         for i in menu:
        #             if "Precios_stock_resultado.aspx?" in i.get('href') and not("nivel=1" in i.get('href') or "Nivel=1" in i.get('href')) :
        #                     temp.append(i.get('href'))
        #         return temp

        # def nivel2(url):
        #     try:
        #         soup = getUrl(url)
        #         menu = soup.find_all('a')
        #     except:
        #         print("hubo un error en clase 'Nivel2'")
        #         print("Url Fallido:" + url)
        #     else:
        #         temp = []
        #         for i in menu:
        #             if 'precios_stock_detallado.aspx?' in i.get('href'):
        #                     temp.append(i.get('href'))
        #         return temp

        # def getCategorias(menu):
        #     categorias = {}
        #     for info in menu:
        #         area = info['Area']
        #         url = info['url']
        #         categorias[area] = url
        #     return categorias

        # #Getting Json file
        # menu = getJson()
        # categorias = getCategorias(menu)
        # # # #print(menu[2]['Area']+": "+ categorias[menu[2]['Area']])

        # #Getting Menu
        # base = "https://www.intelaf.com/"
        # links_0 = [] #Nivel 0 de links
        # links_1 = [] #Nivel 1 de links
        # links_2 = [] #Nivel 2 de links
        # links_3 = [] #Nivel 3 o ya los links que nos dirigen a todos los articulos

        # productInfo={} #Descripcion de cada producto

        # #Listas de todos los articulos ingresados
        # codigo = []
        # nombre = []
        # precio = []
        # oferta = []
        # detalles = []
        # categoria = []
        # garantia = []

        # for i in categorias:
        #     if "Menu_areas.aspx?" in categorias[i]:
        #         links_0.append((categorias[i])[1:])
        #     else:
        #         links_2.append((categorias[i])[1:])

        # #for i in links_0:
        # #    print("Url Lvl 0: " + i)

        # for link0 in links_0:
        #     if "Menu_areas.aspx?" in link0 and ("nivel=0" in link0 or "Nivel=0" in link0):
        #         res = nivel0(base + link0)
        #         #print("URL Lvl 0->1: "+ link0)
        #         if not res:
        #              pass
        #         else:
        #             links_1.extend(res[:-1])
        #     else:
        #         #print("URL Lvl 0->2: "+ link0)
        #         links_2.append(link0)

        # # for i in links_1:
        # #     print("Url Lvl 1: " + i)

        # for link1 in links_1:
        #     if "Menu_areas.aspx?" in link1 and ("Nivel=1" in link1 or "nivel=1" in link1):
        #         res = nivel1(base + link1)
        #         #print("URL Lvl 1->2: "+ link1)
        #         if not res:
        #              pass
        #         else:
        #             links_2.extend(res[:-1])
        #     else:
        #         #print("URL Lvl 2->2: "+ link1)
        #         links_2.append(link1)

        # # for i in links_2:
        # #     print("Url Lvl 2: " + i)

        # for link2 in links_2[1:]:
        #     res = nivel2(base + link2)
        #     #print('Url Lvl 2->3:' + link2)
        #     if not res:
        #         print("No hay articulos en este link:" + link2)
        #     else:
        #         links_3.extend(res)

        # # for link3 in links_3:
        # #     print("Url Lvl 3: " + link3)

        # print("Total Links Lvl 0: "+format(len(links_0)))
        # print("Total Links Lvl 1: "+format(len(links_1)))
        # print("Total Links Lvl 2: "+format(len(links_2)))
        # print("Total Links Lvl 3: "+format(len(links_3)))

        # for link3 in links_3:
        #     try:
        #         soup = getUrl(base + link3)
        #         paginaProducto = soup.find('div',{'class':'row cuerpo'})
        #         pp = paginaProducto.find_all('div',attrs = {'id' :'c1' , 'class':'col-xs-12'})

        #         codigo.append((paginaProducto.find('p',{'class':'codigo'}).text)[16:])
        #         nombre.append( paginaProducto.find('h1').text)
        #         precio.append((paginaProducto.find('p',{'class':'precio_normal'}).text)[17:])
        #         oferta.append((paginaProducto.find('p',{'class':'beneficio_efectivo'}).text)[21:])
        #         detalles.append([j.text for j in pp])
        #         categoria.append((paginaProducto.find('p',{'class':'area'}).text)[23:])
        #         garantia.append((paginaProducto.find('p',{'class':'garantia'}).text)[9:])
        #     except:
        #         print(link3 + ' ---> Status: link Fallido!')
        #         continue
        #     else:
        #         print(link3 + ' ---> Status: link exitoso!')

        # productInfo = {
        #         "codigo":codigo,
        #         "nombre":nombre,
        #         "precio":precio,
        #         "oferta":oferta,
        #         "detalles":detalles,
        #         "categoria":categoria,
        #         "garantia":garantia
        #      }
        # try:
        #     df = pd.DataFrame(productInfo,columns=["codigo","nombre","precio","oferta","detalles","categoria","garantia"])
        #     df.to_excel(r'C:\Users\javie\Desktop\EcommerceWebscraper\prueba.xlsx')
        # except:
        #     print("No se exporto a excel, revise codigo")
        # else:
        #     print("Se proceso correctamente, mire si la informacion esta correcta")

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

    # Click(Expandir para mas info)
# def nivel1(url):
# try:
##        soup = getUrl(url)
##        links = soup.find_all('a')
# except:
##        print("Hubo un error en la clase 'nivel1()'")
# else:
##        temp = []
# for l in links:
# temp.append(l.get('href'))
# return temp

base = "https://www.click.gt"
soup = getUrl(base)
menu = findItem(soup,'ul','class',['justify-content-center','container','d-flex','align-items-center','mb-0','mt-0','pr-4'])
list = findItems(menu,'a','class',['nav-link','waves-effect','waves-light'])
cat = []
for l in list:
    if l.get('id')== None:
        pass
    else:
        cat.append(l.get('id'))
cat.append('otro')
level0 = {}
categorias = []
for c in cat:
    if c != 'otro':
        level1 = {}
        ul = findItem(menu,'div','aria-labelledby',c)
        listar = findItems(ul,'li',None,None)
        for l in listar:
            l1 = (findItem(l,'a',None,None)).text
            l2 = base + (findItem(l,'a',None,None)).get('href')
            level1[l1] = l2
        level0[c] = level1
    else:
        level1 = {}
        for li in list:
            if li.get('href') == None:
                continue
            else:
                if "\n" in li.text:
                    l1 = str(li.get('href')).replace("/productos/","")
                else:
                    l1 = li.text
                l2 = base + li.get('href')
                level1[l1] = l2
                level0[c] = level1

for lvl0 in level0:
    for lvl1 in level0[lvl0]:
            link = level0[lvl0][lvl1]
            print(link)

##with open("C:/Users/javie/Desktop/EcommerceWebscraper/Guatemala/click/clickJson.json",'w') as file:
##    json.dump(level0,file)
##file.close()

##
##links_0 = []
##links_1 = []
##links_2 = []
##
# for i in menu:
# print(i.get('href'))
# if i.get('href') == None:
# pass
# elif "/productos/" in i.get('href'):
# links_0.append(i.get('href'))
##
# for link0 in links_0:
##    soup = getUrl(base+link0)
##    pagination = soup.find_all('button', {'class': 'page-link'})
# if len(pagination) == 0:
##        res = base+link0
# print(base+link0)
# links_1.append(res)
# elif len(pagination) == 2:
##        paginas = int(pagination[0].text)
# for i in range(1, paginas):
##            res = base+link0+"?page="+format(i)
# print(base+link0+"?page="+format(i))
# links_1.append(res)
# elif len(pagination) == 3:
##        paginas = int(pagination[-2].text)
# for i in range(1, paginas):
##            res = base+link0+"?page="+format(i)
# print(base+link0+"?page="+format(i))
# links_1.append(res)
# else:
##        paginas = int(pagination[-2].text)
# for i in range(1, paginas):
##            res = base+link0+"?page="+format(i)
# print(base+link0+"?page="+format(i))
# links_1.append(res)
##
# for link1 in links_1:
##    res = nivel1(link1)
# for r in res:
# if r == None:
# pass
# elif "/single-product/" in r:
# links_2.append(r)
##
##print("Links Lvl 0: " + format(len(links_0)))
##print("Links Lvl 1: " + format(len(links_1)))
##print("Links Lvl 2: " + format(len(links_2)))
##
##codigo = []
##nombre = []
##precio = []
##oferta = []
##categoria = []
##detalles = []
##garantia = []
##
##intentosFallidos = 0
##intentosExistosos = 0
# for link2 in links_2:
# try:
##        soup = getUrl(base + link2)
##        paginaProducto = findItem(soup,'section','class','text-center')
##        codigos = link2[16:]
##
##        marca = findItem(paginaProducto,"h2",None,None)
##        des = findItem(paginaProducto,"h5",None,None)
##        nombre.append((marca.text).strip() + ": " + (des.text).strip())
##        ofertaP = findItem(paginaProducto,'span','class','red-text')
##        precioO = findItem(paginaProducto,'span','class','grey-text')
# if ofertaP == None:
##            ofertaP = "N/A"
# oferta.append(ofertaP)
# else:
# oferta.append(ofertaP.text)
# precio.append(precioO.text)
##        garant = findItem(paginaProducto,"label",None,None)
# categoria.append('N/A')
# if garant == None:
##            garant = "N/A"
# garantia.append(garant)
# else:
# garantia.append(garant.text)
##        especificar = findItem(paginaProducto,'div','id','collapseOne1')
# detalles.append((especificar.text).strip())
# except:
##        print(link2 + " --> Status: Fallido!")
# intentosFallidos+=1
# else:
# intentosExistosos+=1
# codigo.append(codigos)
##        print(link2 + " --> Status: Existoso!")
##
##print("Exitosos:" + format(intentosExistosos))
##print("Fallidos:" + format(intentosFallidos))
##print("Porcentaje de Exito:" + format(intentosExistosos/(intentosFallidos+intentosExistosos)))
##
# productInfo = {
# "codigo": codigo,
# "nombre": nombre,
# "precio": precio,
# "oferta": oferta,
# "categoria": categoria,
# "detalles": detalles,
# "garantia": garantia
# }
#df = pd.DataFrame(productInfo,columns=["codigo","nombre","precio","oferta","categoria","garantia"])
# df.to_excel(r'C:\Users\javie\Desktop\EcommerceWebscraper\clickProducts.xlsx')

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

        # base = "https://spiritcomputacion.com"
        # soup = getUrl(base+"/productos/")
        # menu = soup.find('ul',{'class':'nav-child'})
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
##                if nombre == None:
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
