# DomainInfo

La idea de este pequeño proyecto, es obtener los registros sobre el dominio a consultar
- NS
- MX
- TXT
- DMARC
- A
  
Adicionalmente gestionar información asociada a las IP que se puedan obtener de los registros A
Se pretende extender para gestionar informacion de los certificados SSL


### Instalación para desarrollo <a id="mvp-install" name="mvp-install"></a>
El proyecto está preparado para correr sobre contenedores docker, ya estan precargados los paquetes de python necesarios y preconfigurados los settings `develop` y así agilizar la instalación del entorno de desarrollo.


Pasos para instalar como entorno de desarrollo:

- Instalar docker y docker-compose
- Descargar las imagenes de python y mariadb
- Construir e inicializar los contenedores
- Completar segun se requiera los datos env
  
Dentro de la carpeta docker, debe crear un archivo .env y añadir las variables siguientes:
```
# docker/.env

DATABASE_ROOT_PASSWORD=Secur3PasswDdRoo7
DATABASE_NAME=db_name
DATABASE_USER=db_user
DATABASE_PASSWORD=Secur3PasswDdUseEr

#No modificar project name
PROJECT_NAME=domain_info 

DATABASE_HOST=domain_db
WEB_PANEL_HOSTNAME=domain_panel

SUB_NETWORK=120.25.1.0/24
DATABASE_IP=120.25.1.10
WEB_PANEL_IP=120.25.1.11

DEBUG=True
LOCAL_HOST_URL=localhost
PUBLIC_HOST_URL=example.com

```
Los datos del archivo .env pueden ser personalizados segun se requiera

(`importante revisar si es necesario adecuar la version de la imagen python en DockerfilePanel al salir nuevas versiones o si tiene una version diferente en su entorno local`)
Acceder a la carpeta docker y ejecutar
``` bash
$ docker-compose build
$ docker-compose up -d
```

Es posible que al levantar por primera vez no lea adecuadamente la base de datos, para esto se sugiere detener los contenedores y volver a levantar el servicio.

- Aplicar migraciones en la BD
``` bash
$ docker exec -it domain_panel bash
$ python manage.py makemigrations --settings=domain_info.settings.develop
$ python manage.py migrate --settings=domain_info.settings.develop
```

- Si requiere crear un superuser (en la linea de comandos dentro del contenedor)
``` bash
$ python manage.py createsuperuser --settings=domain_info.settings.develop
```

Si hubiera algun problema detener y reinicar los contenedores para que tomen los cambios de la migracion de la BD
``` bash
$ docker-compose stop
$ docker-compose start
```

- Para debuggin revisar log de los contenedores:
``` bash
$ docker logs -f domain_panel  # contenedor web
$ docker logs -f domain_db  # contenedor base de datos
```

En un navegador abrir el localhost:8000

Tambien está funcional la parte de administración de django en la url:

localhost:8000/admin

Si tú como desarrollador agregas o actualizas paquetes necesarios a un contenedor o dependencias de python, recuerda actualizar los archivos de docker para que el `build` de contenedores este al día y los demas miembros del equipo adopten el cambio sin mayores complicaciones.



### Como funciona

Toda la gestion de registros los realiza en este momento mediante terminal con comandos por ejemplo:
- dig txt example.com

Excepto por los datos referentes a las IP, estos al momento son gestionados mediante la API 
- https://ipwho.is/

¡Ready to code!