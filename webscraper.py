from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

from requests.sessions import session

# Estados Unidos(Expandir para mas info)
# 1 Amazon
# amazon = "https://www.amazon.com/"
# send = requests.get(amazon)
# soup = BeautifulSoup(send.text,'html.parser')
# links = soup.find_all('')
# for i in links:
#     link = i
#     print(link)
# 2 Ebay
# 3 Best Buy
# 4 NewEgg
# 5 Gearbest

# China(Expandir para mas info)

# Guatemala(Expandir para mas info)
# Intelaf(Expandir para comentarios)
# Para la pagina de intelaf, se ve que consiste en el link siendo la URL original, seguido de un link que termina en .aspx, luego el codigo del producto
# cuando se trata de una categoria, puede que se tiene que agregar algo mas para que veamos los productos del mismo


def getJson():
    url = "https://www.intelaf.com/js/menu_productos22112021091955.json"
    try:
        request = requests.Session()
        res = request.get(url)
    except:
        print("Error en la clase 'getJson()'")
        print("Url Fallido:"+ url)
    else:
        data = json.loads(res.text)
        menu = data['menu_sub_1s']
        return menu

def getUrl(url):
    try:
        request = requests.Session()
        send = request.get(url)
    except:
        print("Revise el url, no se proceso correctamente")
        print("Url Fallido:" + url)
    else:
        soup = BeautifulSoup(send.text, 'html.parser')
        return soup

def nivel0(url):
    try:
        soup = getUrl(url)
        menu = soup.find_all('a')
    except:
        print("hubo un error en clase 'Nivel0'")
        print("Url Fallido:" + url)
    else:
        temp = []
        for i in menu:
            if 'Menu_areas.aspx?' in i.get('href') and ("nivel=1" in i.get('href') or "Nivel=1" in i.get('href')):
                    temp.append(i.get('href'))
        return temp

def nivel1(url):
    try:
        soup = getUrl(url)
        menu = soup.find_all('a')
    except:
        print("hubo un error en clase 'Nivel1'")
        print("Url Fallido:" + url)
    else:
        temp = []
        for i in menu:
            if "Precios_stock_resultado.aspx?" in i.get('href') and not("nivel=1" in i.get('href') or "Nivel=1" in i.get('href')) :
                    temp.append(i.get('href'))
        return temp

def nivel2(url):
    try:
        soup = getUrl(url)
        menu = soup.find_all('a')
    except:
        print("hubo un error en clase 'Nivel2'")
        print("Url Fallido:" + url)
    else:
        temp = []
        for i in menu:
            if 'precios_stock_detallado.aspx?' in i.get('href'):
                    temp.append(i.get('href'))
        return temp

def getCategorias(menu):
    categorias = {}
    for info in menu:
        area = info['Area']
        url = info['url']
        categorias[area] = url
    return categorias

def getProducts():
    try:
        containers = soup.find_all('div', {'class': 'descripcion'})
    except:
        print("Error en 'getProducts()'")
    else:
        producto = {}
        for i in containers:
            try:
                a = i.find_all('a')
            except:
                print("Error en 'getProducts'")
            else:
                codigo = ""
                for j in a:
                    link = j.get('href')
                    codigo = link[36:]
                    producto[codigo] = link
                    break
                #print(codigo +":"+producto[codigo])
        return producto


#Getting Json file
menu = getJson()
categorias = getCategorias(menu)
# # #print(menu[2]['Area']+": "+ categorias[menu[2]['Area']])

#Getting Menu
base = "https://www.intelaf.com/"
links_0 = [] #Nivel 0 de links
links_1 = [] #Nivel 1 de links
links_2 = [] #Nivel 2 de links
links_3 = [] #Nivel 3 o ya los links que nos dirigen a todos los articulos

productInfo={} #Descripcion de cada producto

#Listas de todos los articulos ingresados
codigo = [] 
nombre = []
precio = []
oferta = []
detalles = []
categoria = []
garantia = []

for i in categorias:
    if "Menu_areas.aspx?" in categorias[i]:
        links_0.append((categorias[i])[1:])
    else:
        links_2.append((categorias[i])[1:])

#for i in links_0:
#    print("Url Lvl 0: " + i)

for link0 in links_0:
    if "Menu_areas.aspx?" in link0 and ("nivel=0" in link0 or "Nivel=0" in link0):
        res = nivel0(base + link0)
        #print("URL Lvl 0->1: "+ link0)
        if not res:
             pass
        else:
            links_1.extend(res[:-1])
    else:
        #print("URL Lvl 0->2: "+ link0)
        links_2.append(link0)

# for i in links_1:
#     print("Url Lvl 1: " + i)

for link1 in links_1:
    if "Menu_areas.aspx?" in link1 and ("Nivel=1" in link1 or "nivel=1" in link1):
        res = nivel1(base + link1)
        #print("URL Lvl 1->2: "+ link1)
        if not res:
             pass
        else:
            links_2.extend(res[:-1])
    else:
        #print("URL Lvl 2->2: "+ link1)
        links_2.append(link1)

# for i in links_2:
#     print("Url Lvl 2: " + i)

for link2 in links_2[1:]:
    res = nivel2(base + link2)
    #print('Url Lvl 2->3:' + link2)
    if not res:
        print("No hay articulos en este link:" + link2)
    else:
        links_3.extend(res)

# for link3 in links_3:
#     print("Url Lvl 3: " + link3)

print("Total Links Lvl 0: "+format(len(links_0)))
print("Total Links Lvl 1: "+format(len(links_1)))
print("Total Links Lvl 2: "+format(len(links_2)))
print("Total Links Lvl 3: "+format(len(links_3)))


for link3 in links_3:
    try:
        soup = getUrl(base + link3)
        paginaProducto = soup.find('div',{'class':'row cuerpo'})
        pp = paginaProducto.find_all('div',attrs = {'id' :'c1' , 'class':'col-xs-12'})

        codigo.append((paginaProducto.find('p',{'class':'codigo'}).text)[16:])
        nombre.append( paginaProducto.find('h1').text)
        precio.append((paginaProducto.find('p',{'class':'precio_normal'}).text)[17:])
        oferta.append((paginaProducto.find('p',{'class':'beneficio_efectivo'}).text)[21:])
        detalles.append([j.text for j in pp])
        categoria.append((paginaProducto.find('p',{'class':'area'}).text)[23:])
        garantia.append((paginaProducto.find('p',{'class':'garantia'}).text)[9:])
    except:
        print(link3 + '---> Status: link Fallido!')
        continue
    else:
        print(link3 + '---> Status: link exitoso!')

#Existencias del Producto
#     disp = soup.find('div',{'class':'col-xs-12 col-md-3 columna_existencias'})
#     tiendas = disp.find_all('div',{'class':'div_stock_sucu'})
#     existencias = {}
#     existencias["codigo"] = (paginaProducto.find('p',{'class':'codigo'}).text)[16:]
#     existencias["VentaLinea"] = disp.find('div',{'class':'col-xs-1'}).text
# for j in tiendas:
#     tienda = j.find_all('div')
#     existencias[tienda[0].text] = tienda[1] .text
    #print(existencias)

# productInfo = {
#         "codigo":codigo,
#         "nombre":nombre,
#         "precio":precio,
#         "oferta":oferta,
#         "detalles":detalles,
#         "categoria":categoria,
#         "garantia":garantia
#      }
#print(productInfo)
#print(len(codigo))
try:
    df = pd.DataFrame(productInfo,columns=["codigo","nombre","precio","oferta","detalles","categoria","garantia"])
    df.to_excel(r'C:\Users\javie\Desktop\EcommerceWebscraper\prueba.xlsx')    
except:
    print("No se exporto a excel, revise codigo")
else:
    print("Se proceso correctamente, mire si la informacion esta correcta")






