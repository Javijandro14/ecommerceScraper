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
    xhttp.open("GET", "testing.json", false);
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

  document.getElementById("filters").append(filter);
}

function loadCategoria(json) {
  var tabla = document.getElementsByClassName("list")[0];
  if (typeof (tabla) != 'undefined') {
    tabla.remove();
  }
  var table = document.createElement("table");
  var iter = 3;
  table.setAttribute("class", "list");
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



/*
function loadFilters(json) {
  var tabla = document.getElementsByClassName("lists")[0]
  if (typeof (tabla) != 'undefined') {
    tabla.remove();
  }
  var jsonRes = json;


  var filter = document.createElement("div");
  filter.setAttribute("class", "lists");
  for (var i in jsonRes) {
    var button = document.createElement("button");
    button.setAttribute("class", "lists store-options");
    button.setAttribute("onclick", "loadCategoria(" + JSON.stringify(jsonRes[i]) +",'categorias')");
    //button.onclick(loadCategoria(jsonRes[item],item));
    //button.addEventListener("click", loadCategoria(JSON.stringify(jsonRes[i]), "categorias"));
    button.innerHTML = i;
    filter.append(button);
  }
  document.getElementById("filters").append(filter);
}
function loadCategoria(json, item) {
  var tabla = document.getElementsByClassName("list")[0]
  if (typeof (tabla) != 'undefined') {
    tabla.remove();
  }
  // if (json == null || json == undefined) {
  //   var jsonRes = getJson(null, item);
  // } else {
  var jsonRes = JSON.parse(json)[item];
  // }
  //console.log(json);
  var table = document.createElement("table");
  iter = 3
  table.setAttribute("class", "list");
  if (typeof (jsonRes) == "string") {
    var cat = document.createElement("td");
    cat.setAttribute("class", "category-button")
    cat.innerHTML = "<a class='links'>" + json + "</a>";
    table.append(cat);
  } else {
    for (var i in jsonRes) {
      console.log(i);
      var link = document.createElement("a");
      var cat = document.createElement("td");

      if (iter == 3) {
        var fila = document.createElement("tr");
        iter = 0
        table.append(fila);
      }
      cat.setAttribute("class", "category-button")
      link.setAttribute("class", "links");
      if (typeof (json[item]) == "object") {
        if (json[i]["codigo"] != undefined) {
          url = "descriptionProd.html?item=" + jsonRes[i]["codigo"];
          link.setAttribute("href", url)
          link.innerHTML = i
        }
        link.setAttribute("onclick", "loadFilters(" + JSON.stringify(json) + "); loadCategoria(" + JSON.stringify(json[i]) + ")")
        link.innerHTML = i
      }
      cat.append(link)
      fila.append(cat)
      iter += 1;

    }
  }
  document.getElementById("products").append(table);
}
*/
/*
function loadProduct(codigo, json) {
  var products = json;
  search = false;
  while (!search) {
    if (search == false) {
      for (var i in products) {
        if (codigo == i) {
          console.log("Product Found!");
          var codigos = products[i]["codigo"]
          var name = products[i]["nombre"]
          var precio = products[i]["precio"]
          var oferta = products[i]["oferta"]
          var cat = products[i]["categoria"]
          var detalle = products[i]["detalles"]
          var garantia = products[i]["garantia"]
          var link = products[i]["link"]
          showProd(codigos, name, precio, oferta, cat, detalle, garantia, link);
          search = true;
          break;
        } else {
          if (search == false) {
            for (var j in products[i]) {
              if (codigo == j) {
                console.log("Product Found!");
                var codigos = products[i][j]["codigo"]
                var name = products[i][j]["nombre"]
                var precio = products[i][j]["precio"]
                var oferta = products[i][j]["oferta"]
                var cat = products[i][j]["categoria"]
                var detalle = products[i][j]["detalles"]
                var garantia = products[i][j]["garantia"]
                var link = products[i][j]["link"]
                showProd(codigos, name, precio, oferta, cat, detalle, garantia, link);
                //console.log(codigos,name,precio,oferta,cat,detalle,garantia,link)
                search = true;
                break;
              } else {
                if (search == false) {
                  for (var k in products[i][j]) {
                    if (codigo == k) {
                      console.log("Product Found!");
                      var codigos = products[i][j][k]["codigo"]
                      var name = products[i][j][k]["nombre"]
                      var precio = products[i][j][k]["precio"]
                      var oferta = products[i][j][k]["oferta"]
                      var cat = products[i][j][k]["categoria"]
                      var detalle = products[i][j][k]["detalles"]
                      var garantia = products[i][j][k]["garantia"]
                      var link = products[i][j][k]["link"]
                      showProd(codigos, name, precio, oferta, cat, detalle, garantia, link);
                      search = true;
                      break;
                    } else {
                      if (search == false) {
                        for (var l in products[i][j][k]) {
                          if (codigo == l) {
                            console.log("Product Found!");
                            var codigos = products[i][j][k][l]["codigo"]
                            var name = products[i][j][k][l]["nombre"]
                            var precio = products[i][j][k][l]["precio"]
                            var oferta = products[i][j][k][l]["oferta"]
                            var cat = products[i][j][k][l]["categoria"]
                            var detalle = products[i][j][k][l]["detalles"]
                            var garantia = products[i][j][k][l]["garantia"]
                            var link = products[i][j][k][l]["link"]
                            showProd(codigos, name, precio, oferta, cat, detalle, garantia, link);
                            search = true;
                            break;
                          }
                        }
                      } else {
                        break;
                      }
                    }
                  }
                } else {
                  break;
                }
              }
            }
          } else {
            break;
          }
        }
      }
    } else {
      break;
    }
  }
  return products;
}

function showProd(codigos, name, precio, oferta, cat, detalle, garantia, link) {
  document.getElementsByClassName("sku")[1].innerHTML = codigos
  document.getElementsByClassName("product-title")[0].innerHTML = name
  document.getElementsByClassName("oldprice")[0].innerHTML = "Q" + precio
  document.getElementsByClassName("newprice")[0].innerHTML = "Q" + oferta
  document.getElementsByClassName("cat")[0].innerHTML = cat
  document.getElementsByClassName("description")[0].innerHTML = detalle
  document.getElementsByClassName("garantia")[0].innerHTML = garantia
  var direct = document.getElementsByClassName("linktienda")[0]
  direct.setAttribute("href", link)
  direct.innerHTML = "Link";

}
*/
//function findSimilarProd(){}
