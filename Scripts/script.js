function informacion(a) {
  var cliente = document.createElement("h1");
  cliente.innerHTML = a;
  //document.getElementsByClassName(a)[0].appendChild(cliente);
  console.log(a);
  cliente = "";
}

function nuevoTelefono() {
  var form = document.createElement("form");
  form.setAttribute("class", "formulario");

  var lbl1 = document.createElement("h3");
  lbl1.innerHTML = "Nuevo Telefono"

  var tel = document.createElement("input")
  tel.setAttribute("type", "text");
  tel.setAttribute("placeholder", "Numero de telefono");

  var cliente = document.createElement("input")
  cliente.setAttribute("type", "text");
  cliente.setAttribute("placeholder", "Nombre Cliente");

  var corte = document.createElement("select");
  var opcion = document.createElement("option");
  opcion.setAttribute("disabled", "true");
  opcion.setAttribute("selected", "true");
  opcion.innerHTML = "Dia de Corte";
  corte.appendChild(opcion);

  for (var i = 1; i <= 31; i++) {
    var opciones = document.createElement("option");
    opciones.setAttribute("value", i);
    opciones.innerHTML = i;
    corte.appendChild(opciones);
  }
  var s = document.createElement("button");
  s.setAttribute("type", "submit");

  form.append(lbl1, tel, cliente, corte);
  document.getElementsByTagName("body")[0].appendChild(form);
  form.append(s);
}