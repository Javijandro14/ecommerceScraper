# ecommerceScraper
Prueba de webscraping, donde probamos varias paginas web de USA, China y Guatemala, posiblemente otros paises, si quieres ver el resultado, deberia estar la pagina activo aqui: 

### https://javijandro14.github.io/ecommerceScraper/searchingProd.html 

No todos los links sirven, mas que todo sirve esta y la de descripcion de productos.

El codigo lo pueden ver, manipular y reutilizar, pero dejo claro que no seria responsable de cualquier daño que usted haya causado a su maquina o cualquier daño que cause a otros. Tenga cuidado y primero analice el codigo antes de depurarlo. Estoy dispuesto a ver si hay personas que quieran mejorar le codigo, pero quisiera tener el codigo sin modificaciones a menos que fuera una solucion a un problema grave. Pero no es problema si me mandan mensaje, que se tomara en consideracion.

# ¿Como se utiliza?
Estamos probando generar una tabla de datos para TODA la pagina, pero podemos hacerlo en donde no es necesario, quiza solo necesites una sola area, eso se programara en el futuro, mientras tanto, estaremos haciendo toda la pagina. Tengan en cuenta que "Webscraping" NO es ilegal, pero empresas pondrian en los terminos y condiciones que no es permitido el uso de spiders, crawlers, automatizaciones, entre otros; si se llegaran a enterar que tu ip esta mandando muchos mensajes de conseguir datos en su servidor, o te ponen lento la conexion con ellos, o te bloquean la ip por completo, que cuesta para que obtengas una nueva IP. Si llegaran a tener daños en sus servidores, entonces alli si podran ver lo que son daños y prejuicios, por lo que si pueden tomar accion legal. Asi que toman precaucion, se sugiere uso de una VPN y posiblemente un servicio proxy para evitar problemas.

# Datos Extraidos:
¿Que pasa con los datos que han sido extraidos? ¿Que hacemos con ellos? Pues podemos hacer muchas cosas, pero en este caso, queremos hacer una pagina web en donde muestran los datos en el momento que se extrajo, entonces tenemos dos archivos JSON: uno para organizarlos en categorias y subcategorias y otra para conseguir los datos del producto en si. No esta perfecto la pagina, ya que hay problemas de diseño y tambien, para tener todos los precios como lo tiene la pagina web, tendriamos que mandar muchos requests a su respectivo pagina por lo cual seria muy dificil hacerlo todos los dias y que las empresas no se vayan a enojar por quemar sus servidores. Se puede ver si hay un sistema mejor que la que tenemos.

# ¿Quienes son interesados este programa?
Cualquier persona quien le interese el tema, ya sea para estudiar python, o que trabajen en una area donde le es necesario conseguir datos. Muchas empresas utilizan esta informacion para comparar los precios con su empresa, esto para que tengan una idea de que precio esta cada producto en el mercado, si es posible ganarlo. Otra forma de verlo es que un cliente puede comparar precios entre varias paginas y pues el que tiene menos valor es el mas probable en comprarlo, o que se mire las ventajas y desventajas de comprar en tal empresa

## Paginas a probar:
Ahorita solo tenemos paginas de guatemala, pero queremos hacer que nos sirva en cualquier pagina, nuestras metas serian primero con las de guatemala(Intelaf, Kemik, Pacifiko, Max, etc), luego con las de China(Alibaba, Aliexpress, etc.) y por ultimo las de USA(Best Buy, Amazon, Walmart, etc). La razon de porque se puso guatemala primero es que la tecnologia no es muy avanzada en terminos de envio de requests o bloqueos de ip, tengan en cuenta que NO es ilegal usar metodos "Webscraping" en paginas web, pero no es vista de buena manera a estas empresas, ya que esto implica mandar miles y miles de requests, cargando mas el servidor/es, que tienen, que si todos lo fueran a hacer, se caeria la pagina por completo, costando a la empresa posibles millones.

# Funciones Comunes
Funciones que se han creado para evitar redundancia de codigo y variables complejas diferentes en cada pagina. La ventaja es que la mayoria de paginas E-commerce, es que su estructura es parecida, con algunas diferencias. Ahora puede que hayan paginas que son especiales en ciertas cosas que se nos complica.

## 1. getUrl(url):
Esto nos sirve para que podamos conseguir el tipo de variable 'Soup' del modulo de 'BeautifulSoup', primero usamos un request para abrir una session, luego probamos nuestra Url, si este no sirve, nos tira un mensaje con el url fallido, si es exitoso, entonces nos retorna un valor soup el cual ya podemos extraer cualquier datos que desee

## 2. findItem(soup, item, attType, attName):
Soup: es el codigo html que se guardo al hacer el request del link. No necesariamente tiene que ser todo el codigo html, aveces se quiere buscar el articulo dentro de otro articulo que se habia buscado el html.

item: es el articulo que queremos buscar, si es un link, un parrafo, div, cualquier elemento.

attType: si tiene atributos el elemento, se nos puede hacer mucho mas facil encontrar el elemento, puede ser 'class', 'id', u otras, no necesariamente que etiqueta, sino atributos que tiene el elemento como data-type, arialLabelby, y otras.

attName: La descripcion del atributo, si tiene mas de un nombre por ejemplo en la clase, se recomienda hacer un objeto lista [], esto es si la clase tiene espacios que se sabe si hay mas (Ej. class="className1 className2", deberia ser asi: ['className1','className2'])

Tenga en cuenta que nuestra funcion sirve para buscar 1 elemento, para buscar una lista de elementos que cumplen nuestros requisitos, se usa la otra funcion similar.

## 3. findItems(soup, item, attType, attName):
Es lo mismo que 'findItem', pero regresa una lista [], todos los elementos son iguales. Esto me ha servido mucho para que se pueda hacer un ciclo entre todos los elementos y buscar lo que quiero

## 4. data(jsonData,store):
jsonData: nos da un objeto JSON con el nombre del producto y su link para mandar un request.

store: es la tienda que queremos buscar el producto, la estructura es igual en ciertas paginas, pero no todos tienen la clase igual en los elementos o que tengan el diseño

El proceso es el siguiente: se hace un ciclo que ira por el primer nivel, buscara cada elemento que tiene, si el objeto es un link a un producto, hara un request a la pagina para conseguir datos como precio, codigo, descripcion, etc, si dentro del dict(o Json), hay otro dict, entonces se hara un ciclo dentro del ciclo que estamos para buscar mas a fondo, osea de nivel 1 --> 2, este proceso se dara hasta que no hay mas niveles que buscar, osea que puede ir a nivel 1-->2-->3-->4-->5
## 5. buscarProd(link,cat,store):
link: link del producto encontrado

cat: cateogira que se busco el producto en el JSON

store: la tienda que se esta buscando el producto

La funcion de esta es que al recibir el link, se manda un request a la pagina, nos regresa el html del producto, y dependiendo de la tienda, tiene codigo especifico para encontrar caracteristicas del producto, como nombre, codigo, precio, si hay oferta, tiene garantia, detalles, etc. Una vez tenemos esto, lo guarda en un dict y se ira al siguiente producto

## 6. getCategorias(link,store):
link: es el link base de la pagina que queremos buscar productos y categorias

store: es la tienda que queremos buscar categorias y productos

Es parecido a la funcion a la funcion data(), solo que esto es para buscar todos los productos y categorias primero y lo vuelve JSON. Buscamos categorias, luego se manda request y luego hay una condicion que nos dice, si hay  sub-categorias repite el proceso, pero si no hay mas subcategorias, entonces que empiece a buscar los productos, esto es donde obtenemos el JSON que tiene varios niveles de datos

## 7. getProdInfo(soup,store,item):
soup: html de la pagina de contenedor de productos de la categoria que se encontro.

store: tienda que estamos buscando productos

item: aqui tenemos ciertos estados que nos indica que queremos buscar: cat, prod, name, linkcat, prodname, prodlink, etc. Puedes ver el codigo para tener una idea de para que son cada estados


