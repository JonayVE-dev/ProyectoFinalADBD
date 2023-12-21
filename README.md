# Proyecto Final ADBD
## Integrantes
-Gabriel Jonay Vera Estévez
-Muhammad Campos Preira
-Daniel González de Chaves González

> [!IMPORTANT]
> El archivo [tablas_base_de_datos](tablas_base_de_datos.sql) contiene el script para crear la base de datos, las tablas y los triggers necesarios.
> Despues de ejecutarlo con
> ```psql
> \i tablas_base_de_datos.sql
> ```
> debemos ejecutar [inserciones](inserciones.sql) con
>  ```psql
> \i inserciones.sql
>  ```
>  para realizar la carga inicial de datos
>
> Para iniciar la API debemos ejecutar lo siguiente
> ```bash
> flask --app app run --host 0.0.0.0 --port=8080
> ```
> esto ejecutará el [código](app.py)

> [!NOTE]
> En el [informe](ADDBD_Tiendas_Videojuegos_GameLand.pdf) hemos añadido los casos de ejemplos solicitados.
> Estos se encuentran en el apartado 7 del informe.

## Modelo Entidad Relación

![Modelo Entidad Relación](entidad-relacion.png)

## Modelo Relacional

![Modelo Relacional](relacional-proyecto.png)
