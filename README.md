# ecommerceScraper
Prueba de webscraping, donde probamos varias paginas web de USA, China y Guatemala, posiblemente otros paises

## ¿Como se utiliza?
Estamos probando generar una tabla de datos para TODA la pagina, pero podemos hacerlo en donde no es necesario, quiza solo necesites una sola area, eso se programara en el futuro, mientras tanto, estaremos haciendo toda la pagina. Tengan en cuenta que "Webscraping" NO es ilegal, pero empresas pondrian en los terminos y condiciones que no es permitido el uso de spiders, crawlers, automatizaciones, entre otros; si se llegaran a enterar que tu ip esta mandando muchos mensajes de conseguir datos en su servidor, o te ponen lento la conexion con ellos, o te bloquean la ip por completo, que cuesta para que obtengas una nueva IP. Si llegaran a tener daños en sus servidores, entonces alli si podran ver lo que son daños y prejuicios, por lo que si pueden tomar accion legal. Asi que toman precaucion, se sugiere uso de una VPN y posiblemente un servicio proxy para evitar problemas.

## ¿Quienes son interesados este programa?
Cualquier persona quien le interese el tema, ya sea para estudiar python, o que trabajen en una area donde le es necesario conseguir datos. Muchas empresas utilizan esta informacion para comparar los precios con su empresa, esto para que tengan una idea de que precio esta cada producto en el mercado, si es posible ganarlo. Otra forma de verlo es que un cliente puede comparar precios entre varias paginas y pues el que tiene menos valor es el mas probable en comprarlo, o que se mire las ventajas y desventajas de comprar en tal empresa

### Paginas a probar:
Ahorita solo tenemos paginas de guatemala, pero queremos hacer que nos sirva en cualquier pagina, nuestras metas serian primero con las de guatemala(Intelaf, Kemik, Pacifiko, Max, etc), luego con las de China(Alibaba, Aliexpress, etc.) y por ultimo las de USA(Best Buy, Amazon, Walmart, etc). La razon de porque se puso guatemala primero es que la tecnologia no es muy avanzada en terminos de envio de requests o bloqueos de ip, tengan en cuenta que NO es ilegal usar metodos "Webscraping" en paginas web, pero no es vista de buena manera a estas empresas, ya que esto implica mandar miles y miles de requests, cargando mas el servidor/es, que tienen, que si todos lo fueran a hacer, se caeria la pagina por completo, costando a la empresa posibles millones.

### Funciones Comunes
Aqui tenemos las funciones que nos van a servir, ya que cada pagina esta parecido para sacar datos
#### 1. 'getUrl(url)':
Esto nos sirve para que podamos conseguir el tipo de variable 'Soup' del modulo de 'BeautifulSoup', primero usamos un request para abrir una session, luego probamos nuestra Url, si este no sirve, nos tira un mensaje con el url fallido, si es exitoso, entonces nos retorna un valor soup el cual ya podemos extraer cualquier datos que desee
### 2. 'getJson(url)':
Es lo mismo que 'getUrl', pero la diferencia es que si tenemos un archivo .json que la pagina recibe(por ejemplo, de intelaf), entonces lo podemos extraer y tener ya casi toda la informacion del producto o categoria. No todas las paginas lo tienen, y si lo tienen, muchas veces no es de los productos en si, sino que de otra informacion que puede ser o no util a nuestra situacion
### 3. 


