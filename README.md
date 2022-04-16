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


