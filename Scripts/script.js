/*

# =============================================================== #
#             Project Name: WebScraping Website service           #
#               Author: Javier Alejandro Diaz Portillo            #
#          Descripcion: Script para mostrar las categorias        #
#                    y productos de cada tienda,                  #
#            tambien para mostrar los datos de productos          #
# =============================================================== #

*/

function getJson(json, item) {
  if (json == undefined || json == null) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "categories.json", false);
    //xhttp.open("GET", "EcommerceData/Guatemala/intelaf/Intelaf.json", false);
    xhttp.send();
    json = JSON.parse(xhttp.responseText);
    if (item != undefined || item != null) {
      return json[item];
    } else {
      return json;
    }
  } else {
    if (item != undefined || item != null) {
      return json[item];
    } else {
      return json;
    }
  }
}

function getParams(item) {
  var url_string = window.location.href;
  var url = new URL(url_string);
  var params = url.searchParams.get(item);
  if (params != null || params != undefined) {
    return params;
  }
  else {
    return null;
  }
}

function loadTable(json) {
  var table = document.getElementsByClassName("quick-table")[0];
  console.log(json);
  var iter = 3;
  for (var i in json) {
    var cat = document.createElement("td");
    cat.setAttribute("class", "categories");
    cat.style.height = "100%";
    if (iter == 3) {
      var fila = document.createElement("tr");
      iter = 0;
      table.append(fila);
    }
    cat.innerHTML = '<a class="store-options" href="searchingProd.html?json=' + i + '">' + i + '</a>';
    fila.append(cat);
    iter += 1;
  }
  loadList(json);
}

function loadList(json) {
  var list = document.getElementsByClassName("dropdown-menu")[0];
  for (var i in json) {
    var item = document.createElement("li");
    item.innerHTML = '<a class="links" href="searchingProd.html?json=' + i + '"> ' + i + '</a>';
    list.append(item);
  }
}

function getMenu() {
  var json = getJson(null, null);
  loadList(json);
  var item = getParams('json');
  //console.log(item);
  if (item != undefined || item != null) {
    loadFilters(getJson(json, item));
    loadCategoria(getJson(json[item], "categorias"));
  } else {
    loadFilters(getJson(json, null));
  }
}
function loadFilters(json) {
  var tabla = document.getElementsByClassName("lists")[0];
  if (typeof (tabla) != 'undefined') {
    tabla.remove();
  }

  var filter = document.createElement("div");
  filter.setAttribute("class", "lists");
  if (json["link"] == undefined || json["fechaAct"] == undefined) {
    for (var i in json) {
      var jsonRes = getJson(json, i);
      var button = document.createElement("button");
      button.setAttribute("class", "lists store-options");
      for (var j in jsonRes) {
        if (typeof (jsonRes[j]) == 'object') {
          if (j == 'categorias') {
            /*console.groupCollapsed(i); 
            console.log(jsonRes[j]);*/
            button.setAttribute("onclick", "loadCategoria(" + JSON.stringify(jsonRes[j]) + ")");
            //console.groupEnd();
          }
          else {
            // console.groupCollapsed(i); 
            // console.log(jsonRes);
            button.setAttribute("onclick", "loadCategoria(" + JSON.stringify(jsonRes) + ")");
            // console.groupEnd();
          }
        }
      }
      button.innerHTML = i;
      filter.append(button);
    }
  }

  document.getElementById("filters").append(filter);
}

function loadCategoria(json) {
  var tabla = document.getElementsByClassName("list")[0];
  if (typeof (tabla) != 'undefined') {
    tabla.remove();
  }
  var table = document.createElement("table");
  var iter = 3;
  table.setAttribute("class", "list quick-table");
  for (var i in json) {
    if (typeof (getJson(json, i)) == "string") {
      var cat = document.createElement("td");
      cat.setAttribute("class", "category-button")
      cat.innerHTML = "<a class='links'>" + (getJson(json, i)) + "</a>";
      table.append(cat);
    } else if (typeof (getJson(json, i)) == "object") {

      var link = document.createElement("a");
      var cat = document.createElement("td");

      if (iter == 3) {
        var fila = document.createElement("tr");
        iter = 0
        table.append(fila);
      }
      cat.setAttribute("class", "category-button")
      link.setAttribute("class", "links");
      //console.groupCollapsed(i);
      if (typeof (json) == "object") {
        //console.log(json[i]["codigo"]);
        if (json[i]["codigo"] != undefined) {
          url = "descriptionProd.html?item=" + json[i]["codigo"];
          link.setAttribute("href", url)
        }
        else {
          link.setAttribute("onclick", "loadFilters(" + JSON.stringify(json) + "); loadCategoria(" + JSON.stringify(json[i]) + ")");

        }
        link.innerHTML = i;
      }
      cat.append(link)
      fila.append(cat)
      iter += 1;
    }
    //console.groupEnd();
  }
  document.getElementById("products").append(table);
}

function loadProduct(codigo) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "products.json", false);
  xhttp.send();
  var products = JSON.parse(xhttp.responseText);

  search = false;
  for (var i in products) {
    if (codigo == i) {
      showProd(codigo, products[i]['codigo'], products[i]['nombre'], products[i]['precio'], products[i]['oferta'], products[i]['categoria'], products[i]['detalles'], products[i]['garantia'], products[i]['link']);
      findSimilarProd(codigo, products);
      break;
    }

  }
}

function showProd(codigo, sku, name, precio, oferta, cat, detalle, garantia, link) {
  document.getElementsByClassName("sku")[0].innerHTML = codigo
  document.getElementsByClassName("sku")[1].innerHTML = sku
  document.getElementsByClassName("product-title")[0].innerHTML = name
  document.getElementsByClassName("oldprice")[0].innerHTML = "Q" + precio
  document.getElementsByClassName("newprice")[0].innerHTML = "Q" + oferta.slice(oferta.lastIndexOf("Q") + 1);
  document.getElementsByClassName("cat")[0].innerHTML = cat
  document.getElementsByClassName("description")[0].innerHTML = detalle
  document.getElementsByClassName("garantia")[0].innerHTML = garantia
  var direct = document.getElementsByClassName("linktienda")[0]
  direct.setAttribute("href", link)
  direct.innerHTML = link;
  var tienda = document.querySelector("#tienda");
  tienda.innerHTML = listarTienda(codigo.slice(0, 2));
}
function findSimilarProd(codigo, product) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "comparison.json", false);
  xhttp.send();
  var comp = JSON.parse(xhttp.responseText);
  lista = comp[codigo]
  var tiendas = document.querySelector(".changeStore");
  tiendas.innerHTML = "";
  for (l in lista) {
    code = lista[l].split("|")[0]
    if (codigo != code) {
      var opcion = document.createElement("button");
      opcion.setAttribute("onclick", "loadProduct('" + code + "')")
      var itemprice = document.querySelector(".newprice").innerHTML;
      opcion.innerHTML = product[code].nombre + "<br>" + product[code].oferta + '<br> <label style="color:red;"> Differencia: Q' + (parseFloat(itemprice.slice(itemprice.lastIndexOf("Q") + 1).replace(",", "")) - parseFloat(product[code]["oferta"].slice(product[code]["oferta"].lastIndexOf("Q") + 1).replace(",", ""))) + "</label> <br> Tienda: <strong>" + listarTienda(code.slice(0, 2)) + "</strong>";
      tiendas.append(opcion);
    }
  }
}

function listarTienda(no) {
  var cat = getJson();
  var tienda = "Ninguno";
  for (i in cat) {
    if (no == cat[i]["codigo"]) {
      tienda = i;
      return tienda
    }
  }
}
