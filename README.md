# Proyecto Final ADBD
## Integrantes
- Gabriel Jonay Vera Estévez
- Muhammad Campos Preira
- Daniel González de Chaves González

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
> 
> En este [vídeo](https://www.youtube.com/watch?v=yOu4f1kMP2Q) está la explicación en inglés.

## Modelo Entidad Relación

![Modelo Entidad Relación](entidad-relacion.png)

## Modelo Relacional

![Modelo Relacional](relacional-proyecto.png)

## Consultas de ejemplo

### Consulta 1
    
```sql
INSERT INTO Devoluciones (id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades) VALUES ('TIENDA1', '2023-12-16', 45000000, 1, ARRAY['VLOL1', 'MCAM1'], ARRAY[1, 1]);

INSERT INTO Devoluciones (id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades) VALUES ('TIENDA2', '2023-12-16', 45000001, 2, ARRAY['PMOU1'], ARRAY[1]);

INSERT INTO Devoluciones (id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades) VALUES ('TIENDA2', '2023-12-16', 45000001, 2, ARRAY['PMOU1'], ARRAY[1]);
```

![consulta1](image10.png)

### Consulta 2

```sql
INSERT INTO Ventas (id_empleado, id_cliente, productos, cantidades) VALUES (99999999, 45000000, ARRAY['VLOL1', 'MCAM1'], ARRAY[1, 1]);

INSERT INTO Ventas (id_empleado, id_cliente, productos, cantidades) VALUES (99999998, 45000001, ARRAY['PMOU1'], ARRAY[2]);

INSERT INTO Ventas (id_empleado, id_cliente, productos, cantidades) VALUES (99999998, 45000001, ARRAY['PMOU1'], ARRAY[2]);
```

![consulta2](image6.png)

### Consulta 3

```sql
INSERT INTO Envios (id_proveedor, id_tienda, productos, fecha, cantidades) VALUES ('PROV1', 'TIENDA1', ARRAY['VLOL1', 'MCAM1'], '2021-01-01', ARRAY[10, 10]);
```	

![consulta3](image12.png)


```sql
INSERT INTO Ventas (id_empleado, id_cliente, productos, cantidades) VALUES (99999999, 45000000, ARRAY['VLOL1', 'MCAM1'], ARRAY[5, 25]);
```

![consulta3](image8.png)


```sql
INSERT INTO Ventas (id_empleado, id_cliente, productos, cantidades) VALUES (99999999, 45000000, ARRAY['VElDelAnillo'], ARRAY[25]);
```	

![consulta3](image15.png)

```sql
INSERT INTO Ventas (id_empleado, id_cliente, productos, cantidades) VALUES (99999999, 45000000, ARRAY['VLOL1', 'MCAM1'], ARRAY[20, 20]);
```

![consulta3](image7.png)


```sql
INSERT INTO Devoluciones (id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades) VALUES ('TIENDA2', '2023-12-20', 45000000, 2, ARRAY['VLOL1', 'MCAM1'], ARRAY[3, 3]);
```

![consulta3](image2.png)

```sql
INSERT INTO Devoluciones (id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades) VALUES ('TIENDA2', '2023-12-20', 45000000, 2, ARRAY['VLOL1', 'MCAM1'], ARRAY[18, 18]);
```

![consulta3](image19.png)


```sql
INSERT INTO Devoluciones (id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades) VALUES ('TIENDA2', '2023-12-20', 45000000, 1, ARRAY['VLOL2', 'MCAM1'], ARRAY[3, 3]);
```

![consulta3](image18.png)

### Consulta 4

```sql
INSERT INTO Contrato (id_provedor, fecha_inicio, duracion) VALUES ('PROV1', '2020-01-01', 365*5);
INSERT INTO Contrato (id_provedor, fecha_inicio, duracion) VALUES ('PROV2', '2020-01-01', 365*5);
INSERT INTO Contrato (id_provedor, fecha_inicio, duracion) VALUES ('PROV3', '2020-01-01', 365);
```

![consulta4](image3.png)


### Consulta 5

```sql
INSERT INTO Envios (id_proveedor, id_tienda, productos, fecha, cantidades) VALUES ('PROV3', 'TIENDA2', ARRAY['PMOU1'], '2020-01-01', ARRAY[20]);
```

![consulta5](image17.png)

### Consulta 6

```sql
INSERT INTO Trabaja (id_tienda, id_empleado, cargo, fecha_inicio, duracion) VALUES ('TIENDA2', 99999998, 'Cajero', '2020-05-01', 365);
```

![consulta6](image4.png)

### Consulta 7

```sql
DELETE FROM TIENDA WHERE id_tienda = 'TIENDA2';
```

![consulta7](image20.png)

### Consulta 8

```sql
DELETE FROM PROVEEDORES WHERE id_proveedor = 'PROV1';
```

![consulta8](image16.png)

### Consulta 9

```sql
-- salario NUMERIC(10,2) CHECK (salario >= 1000) NOT NULL
INSERT INTO Empleados (id_empleado, nombre, apellidos, salario) VALUES (99999997, 'Empleado 3', 'Apellido 1', 999);
```

![consulta9](image14.png)

### Consulta 10

```sql
--   fecha_inicio DATE CHECK (fecha_inicio >= DATE '2000-01-01') NOT NULL
INSERT INTO Proveedores (id_proveedor, nombre, direccion, telefonos) VALUES ('PROV4', 'Proveedor 4', 'Calle 4', ARRAY['444444444']);

INSERT INTO Contrato (id_provedor, fecha_inicio, duracion) VALUES ('PROV4', '1999-12-31', 365*5);
```

![consulta10](image13.png)

