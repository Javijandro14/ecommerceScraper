function loads(json, tienda) {
  var tabla = document.getElementsByClassName("lista")[0]
  if (typeof (tabla) != 'undefined') {
    tabla.remove();
  }

  datos = json

  iter = 3
  var table = document.createElement("table");
  table.setAttribute("class", "lista");
  for (let i in datos) {
    var link = document.createElement("a");
    var cat = document.createElement("td");

    if (iter == 3) {
      var fila = document.createElement("tr");
      iter = 0
      table.append(fila);
    }
    cat.setAttribute("class", "category-button")
    link.setAttribute("class", "links");
    if (typeof (datos[i]) == "object") {
      link.setAttribute("onclick", "loads(datos['" + i + "'],'" + tienda + "')")
      link.innerHTML = i
    } else if (typeof (datos[i]) == "string") {
      url = "descriptionProd.html?tienda=" + tienda + "&codigo=" + i
      link.setAttribute("href", url)
      link.innerHTML = i
    }
    cat.append(link)
    fila.append(cat)
    iter += 1;

  }
  res = JSON.stringify(json);
  document.getElementsByClassName("products")[0].append(table);
  // document.getElementsByClassName("products")[0].innerHTML = res;
}

function loadCategoria(tienda) {
  switch (tienda) {
    case "Intelaf":
      var res = tienda;
      fetch('EcommerceData/Guatemala/intelaf/Intelaf.json').then(resp => resp.json()).then(resp => loads(resp, res))
      break;
    case "Click":
      var res = tienda;
      fetch('EcommerceData/Guatemala/click/Click.json').then(resp => resp.json()).then(resp => loads(resp, res))
      break;
    case "Elektra":
      var res = tienda;
      fetch('EcommerceData/Guatemala/elektra/Elektra.json').then(resp => resp.json()).then(resp => loads(resp, res))
      break;
    case "Spirit":
      var res = tienda;
      fetch('EcommerceData/Guatemala/spiritcomputacion/Spirit.json').then(resp => resp.json()).then(resp => loads(resp, res))
      break;
    case "Max":
      var res = tienda;
      fetch('EcommerceData/Guatemala/max/Max.json').then(resp => resp.json()).then(resp => loads(resp, res))
      break;
    case "Macro":
      var res = tienda;
      fetch('EcommerceData/Guatemala/macrosistemas/Macro.json').then(resp => resp.json()).then(resp => loads(resp, res))
      break;
    case "Kemik":
      var res = tienda;
      fetch('EcommerceData/Guatemala/kemik/Kemik.json').then(resp => resp.json()).then(resp => loads(resp, res))
      break;
    case "Goat":
      var res = tienda;
      fetch('EcommerceData/Guatemala/goatshop/Goatshop.json').then(resp => resp.json()).then(resp => loads(resp, res))
      break;
    case "Funky":
      var res = tienda;
      fetch('EcommerceData/Guatemala/funky/Funky.json').then(resp => resp.json()).then(resp => loads(resp, res))
      break;
  }

}

function getParams() {
  var url_string = window.location.href
  var url = new URL(url_string);
  var tienda = url.searchParams.get("tienda");
  var codigo = url.searchParams.get("codigo");
  switch (tienda) {
    case "Intelaf":
      fetch('EcommerceData/Guatemala/intelaf/intelafProducts.json').then(resp => resp.json()).then(resp => loadProduct(codigo, resp));
      break;
    case "Click":
      fetch('EcommerceData/Guatemala/click/clickProducts.json').then(resp => resp.json()).then(resp => loadProduct(codigo, resp));
      break;
    case "Elektra":
      fetch('EcommerceData/Guatemala/elektra/elektraProducts.json').then(resp => resp.json()).then(resp => loadProduct(codigo, resp));
      break;
    case "Spirit":
      fetch('EcommerceData/Guatemala/spiritcomputacion/spiritProducts.json').then(resp => resp.json()).then(resp => loadProduct(codigo, resp));
      break;
    case "Max":
      fetch('EcommerceData/Guatemala/max/maxProducts.json').then(resp => resp.json()).then(resp => loadProduct(codigo, resp));
      break;
    case "Macro":
      fetch('EcommerceData/Guatemala/macrosistemas/macroProducts.json').then(resp => resp.json()).then(resp => loadProduct(codigo, resp));
      break;
    case "Kemik":
      fetch('EcommerceData/Guatemala/kemik/kemikProducts.json').then(resp => resp.json()).then(resp => loadProduct(codigo, resp));
      break;
    case "Goat":
      fetch('EcommerceData/Guatemala/goatshop/goatshopProducts.json').then(resp => resp.json()).then(resp => loadProduct(codigo, resp));
      break;
    case "Funky":
      fetch('EcommerceData/Guatemala/funky/funkyProducts.json').then(resp => resp.json()).then(resp => loadProduct(codigo, resp));
      break;
  }
}
function loadProduct(codigo, json) {
  var products = json;
  search = false;
  while (!search) {
    if (search == false) {
      for (let i in products) {
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
            for (let j in products[i]) {
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
                  for (let k in products[i][j]) {
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
                        for (let l in products[i][j][k]) {
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

//function findSimilarProd(){}
