from bs4 import BeautifulSoup
import requests
import json
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
            print(name1)
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
                    if not res3 or res3 == res1 or res3 == res2: #Si no hay Sub-SubCategorias, buscara productos
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
                            if not res4 or res4 == res1 or res4 == res2 or res4==res3:
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
                                    if not res5 or res5 == res4 or res5 == res3 or res5 == res2 or res5 == res1:
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
                        categorias.extend(findItems(name.next_sibling,'a',None,None))
                    else:
                        categorias.append(c)
                #print(categorias)
                return categorias
            else:
                #print(subcat)
                sc = [i.a for i in subcat]
                return sc

        elif item == "prod":
            productos = findItems(soup,'a','class','woocommerce-loop-product__link')
            return productos
        elif item == "name":
            name = soup.text.strip()
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


# Kemik
base = "https://www.kemik.gt"
categorias = getCategorias(base,"Kemik")
print(categorias)
with open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/kemik/Kemik.json",'w') as file:
    json.dump(categorias,file)
file.close()
       
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