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

def areas(url):
    try:
        soup = getUrl(url)
        menu = soup.find_all('a')
    except:
        print("hubo un error en clase 'areas'")
        print("Url Fallido:" + url)
    else:
        temp = []
        for i in menu:
            if "Precios_stock_resultado.aspx?" in i.get('href') or 'Menu_areas.aspx?' in i.get('href'):
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
base = "https://www.intelaf.com"
nivel0 = []
links = []
productInfo={}
codigo = []
nombre = []
precio = []
oferta = []
detalles = []
categoria = []
garantia = []


for iter in range(len(categorias)):
     intelaf = base + categorias[menu[iter]['Area']]
     res = list(areas(intelaf))
     # print(res)
     if res is None:
         pass
     else:
         nivel0.extend(res[:-1])
 
for i in nivel0:
     if "Precios_stock_resultado.aspx?area=" in i:
         links.append(i)
     elif "Menu_areas.aspx?" in i:
         intelaf = base + "/" + i
         res = list(areas(intelaf))
         # print(res)
         if res is None:
             pass
         else:
            links.extend(res[:-1])
            #break

for i in links:
    intelaf = base +"/"+ i
    soup = getUrl(intelaf)
    producto = getProducts()
#informacion del producto


for i in producto:
    intelaf = base + "/" + producto[i]
    #intelaf = base + "/" + 'precios_stock_detallado.aspx?codigo=AUDIF-XT-XTH710'
    #print(intelaf)
    soup = getUrl(intelaf)
    paginaProducto = soup.find('div',{'class':'row cuerpo'})
    pp = paginaProducto.find_all('div',attrs = {'id' :'c1' , 'class':'col-xs-12'})
    
    codigo.append((paginaProducto.find('p',{'class':'codigo'}).text)[16:])
    nombre.append( paginaProducto.find('h1').text)
    precio.append((paginaProducto.find('p',{'class':'precio_normal'}).text)[17:])
    oferta.append((paginaProducto.find('p',{'class':'beneficio_efectivo'}).text)[21:])
    detalles.append([j.text for j in pp])
    categoria.append((paginaProducto.find('p',{'class':'area'}).text)[23:])
    garantia.append((paginaProducto.find('p',{'class':'garantia'}).text)[9:])

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
productInfo = {
        "codigo":codigo,
        "nombre":nombre,
        "precio":precio,
        "oferta":oferta,
        "detalles":detalles,
        "categoria":categoria,
        "garantia":garantia
     }
#print(productInfo)
print(len(codigo))

#df = pd.DataFrame(productInfo,columns=["codigo","nombre","precio","oferta","detalles","categoria","garantia"])
#df.to_excel(r'C:\Users\javie\Desktop\EcommerceWebscraper\prueba.xlsx')    






