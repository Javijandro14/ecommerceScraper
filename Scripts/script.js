function loads(json) {
  var tabla = document.getElementsByClassName("lista")[0]
  if (typeof(tabla) != 'undefined'){
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
    if(typeof(datos[i]) == "object"){
    link.setAttribute("onclick","loads(datos['"+i+"'])")
    link.innerHTML = i
    }else if(typeof(datos[i]) == "string"){
      link.setAttribute("href","descriptionProd.html")
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

function loadJson(tienda) {
  resp = tienda;
  switch (resp) {
    case "Intelaf":
      fetch('EcommerceData/Guatemala/intelaf/intelafJson.json').then(resp => resp.json()).then(resp => loads(resp))
      break;
    case "Click":
      fetch('EcommerceData/Guatemala/click/clickJson.json').then(resp => resp.json()).then(resp => loads(resp))
      break;
    case "Elektra":
      fetch('EcommerceData/Guatemala/elektra/elektraJson.json').then(resp => resp.json()).then(resp => loads(resp))
      break;
    case "Spirit":
      fetch('EcommerceData/Guatemala/spiritcomputacion/spiritJson.json').then(resp => resp.json()).then(resp => loads(resp))
      break;
    case "Max":
      fetch('EcommerceData/Guatemala/max/maxJson.json').then(resp => resp.json()).then(resp => loads(resp))
      break;
    case "Macro":
      fetch('EcommerceData/Guatemala/macrosistemas/macroJson.json').then(resp => resp.json()).then(resp => loads(resp))
      break;
    case "Kemik":
      fetch('EcommerceData/Guatemala/kemik/kemikJson.json').then(resp => resp.json()).then(resp => loads(resp))
      break;
    case "Goat":
      fetch('EcommerceData/Guatemala/goatshop/goatshopJson.json').then(resp => resp.json()).then(resp => loads(resp))
      break;
    case "Funky":
      fetch('EcommerceData/Guatemala/funky/funkyJson.json').then(resp => resp.json()).then(resp => loads(resp))
      break;
  }

}

