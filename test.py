from bs4 import BeautifulSoup
import requests
import json
import time


# def data(jsonData,store):
    #     intentosExitosos = 0
    #     intentosFallidos = 0
    #     for j in jsonData:
    #         print("Current Category:" + format(j))
    #         if isinstance(jsonData[j],dict):
    #             for k in jsonData[j]:
    #                 if isinstance(jsonData[j][k],dict):
    #                     for l in jsonData[j][k]:
    #                         if isinstance(jsonData[j][k][l],dict):
    #                             for m in jsonData[j][k][l]:
    #                                 if isinstance(jsonData[j][k][l][m],dict):
    #                                     for n in jsonData[j][k][l][m]:#jsonData[j][k][l][m][n]
    #                                         try:
    #                                             link = jsonData[j][k][l][m][n]
    #                                             cat = format(j)+"-"+format(k)+"-"+format(l)+"-"+format(m)
    #                                             productInfo = buscarProd(link,cat,store)
    #                                         except:
    #                                             print(format(link) + " --> Status: Fallido!")
    #                                             intentosFallidos += 1
    #                                         else:
    #                                             intentosExitosos += 1
    #                                             print(format(link) + " --> Status: Existoso!")
    #                                             jsonData[j][k][l][m][n] = productInfo
    #                                 else:#jsonData[j][k][l][m]
    #                                     try:
    #                                         link = jsonData[j][k][l][m]
    #                                         cat = format(j)+"-"+format(k)+"-"+format(l)
    #                                         productInfo = buscarProd(link,cat,store)
    #                                     except:
    #                                         print(format(link) + " --> Status: Fallido!")
    #                                         intentosFallidos += 1
    #                                     else:
    #                                         intentosExitosos += 1
    #                                         print(format(link) + " --> Status: Existoso!")
    #                                         jsonData[j][k][l][m] = productInfo
    #                         else:#jsonData[j][k][l]
    #                             try:
    #                                 link = jsonData[j][k][l]
    #                                 cat = format(j)+"-"+format(k)
    #                                 productInfo = buscarProd(link,cat,store)
    #                             except:
    #                                 print(format(link) + " --> Status: Fallido!")
    #                                 intentosFallidos += 1
    #                             else:
    #                                 intentosExitosos += 1
    #                                 print(format(link) + " --> Status: Existoso!")
    #                                 jsonData[j][k][l] = productInfo
    #                 else:#jsonData[j][k]
    #                     try:
    #                         link = jsonData[j][k]
    #                         cat = format(j)
    #                         productInfo = buscarProd(link,cat,store)
    #                     except:
    #                         print(format(link) + " --> Status: Fallido!")
    #                         intentosFallidos += 1
    #                     else:
    #                         intentosExitosos += 1
    #                         print(format(link) + " --> Status: Existoso!")
    #                         jsonData[j][k] = productInfo
    #         else:#jsonData[j]
    #             try:
    #                 link = jsonData[j]
    #                 cat = format(j)
    #                 productInfo = buscarProd(link,cat,store)
    #             except:
    #                 print(format(link) + " --> Status: Fallido!")
    #                 intentosFallidos += 1
    #             else:
    #                 intentosExitosos += 1
    #                 print(format(link) + " --> Status: Existoso!")
    #                 jsonData[j] = productInfo
    #     print("Exitosos:" + format(intentosExitosos))
    #     print("Fallidos:" + format(intentosFallidos))
    #     print("Porcentaje de Exito:" + format(intentosExitosos /(intentosFallidos+intentosExitosos)))
    #     return jsonData


#Esta sirve solo por si el usuario desee usar ciertas categorias, no todas
def elegirCat(jsonData):
    level = {}
    cat = []
    iter = 1
    for j in jsonData:
        if isinstance(jsonData[j],dict) and bool(jsonData[j]) != False:
            cat.append(j)
            print(str(iter) +". "+ j)
            iter+=1
        else:
            level[j] = jsonData[j]
            break
    if cat:
        ingreso = input("(Separe sus opciones por medio de espacios y luego ingrese enter) \n")
        opcion = {""}
        opcion.update(ingreso.split(" "))
        opcion.remove("")
        for op in opcion:
            if int(op) <= len(cat):
                level[cat[int(op)-1]] = elegirCat(jsonData[cat[int(op)-1]])
            else:
                print("'"+op+"' esta fuera de rango, por lo tanto no se tomara en cuenta")
    return level
                


file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/funky/Funky.json",)
jsonData = json.load(file)
print(elegirCat(jsonData))

# file = open("C:/Users/javie/Desktop/ecommerceScraper/EcommerceData/Guatemala/kemik/Kemik.json",)
# jsonData = json.load(file)
# print(elegirCat(jsonData))
