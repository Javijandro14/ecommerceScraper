function loads(json) {
  datos = json
  iter = 3
  var table = document.createElement("table");
  table.setAttribute("class", "products");
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
    link.innerHTML = i
    cat.append(link)
    fila.append(cat)
    iter += 1;

  }
  res = JSON.stringify(json);
  document.getElementsByClassName("content")[0].append(table);
  // document.getElementsByClassName("products")[0].innerHTML = res;
}

function loadJson(tienda) {
  resp = "Intelaf"
  // switch (resp) {
  //   case "Intelaf":
  fetch('EcommerceData/Guatemala/intelaf/intelafJson.json').then(resp => resp.json()).then(resp => loads(resp))
  // break;
  // case "Intelaf":
  fetch('EcommerceData/Guatemala/click/clickJson.json').then(resp => resp.json()).then(resp => loads(resp))
  //   // break;
  // // case "Intelaf":
  fetch('EcommerceData/Guatemala/elektra/elektraJson.json').then(resp => resp.json()).then(resp => loads(resp))
  //   // break;
  // case "Intelaf":
  fetch('EcommerceData/Guatemala/spiritcomputacion/spiritJson.json').then(resp => resp.json()).then(resp => loads(resp))
  // break;
  // case "Intelaf":
  fetch('EcommerceData/Guatemala/max/maxJson.json').then(resp => resp.json()).then(resp => loads(resp))
  // break;
  // case "Intelaf":
  fetch('EcommerceData/Guatemala/macrosistemas/macroJson.json').then(resp => resp.json()).then(resp => loads(resp))
  // break;
  // case "Intelaf":
  fetch('EcommerceData/Guatemala/kemik/kemikJson.json').then(resp => resp.json()).then(resp => loads(resp))
  // break;
  // case "Intelaf":
  fetch('EcommerceData/Guatemala/goatshop/goatshopJson.json').then(resp => resp.json()).then(resp => loads(resp))
  // break;
  // case "Intelaf":
  fetch('EcommerceData/Guatemala/funky/funkyJson.json').then(resp => resp.json()).then(resp => loads(resp))
  // break;
  // case "Intelaf":
  fetch('EcommerceData/Guatemala/click/clickJson.json').then(resp => resp.json()).then(resp => loads(resp))
  // break;
  //}

}