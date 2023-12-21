-- Insertar datos en la tabla de usuarios para probar cada unos de los triggers que hay en la base de datos
-- Tienen que estar en este orden para que no haya problemas con las claves foráneas, crea unos pocos de cada y divide las inserciones por trigger que se comprueba
INSERT INTO Productos (id_producto, nombre, precio) VALUES ('VLOL1', 'League of Legends', 5);
INSERT INTO Productos (id_producto, nombre, precio) VALUES ('MCAM1', 'Camiseta 1', 30.5);
INSERT INTO Productos (id_producto, nombre, precio) VALUES ('PMOU1', 'Ratón 1', 76.99);

INSERT INTO Videojuegos (id_videojuego, plataforma, genero) VALUES ('VLOL1', 'PC', 'MOBA');
INSERT INTO Merchandising (id_merchandising, tipo) VALUES ('MCAM1', 'Camiseta');
INSERT INTO Perifericos (id_periferico, tipo, marca) VALUES ('PMOU1', 'Ratón', 'Logitech');

INSERT INTO Proveedores (id_proveedor, nombre, direccion, telefonos) VALUES ('PROV1', 'Proveedor 1', 'Calle 1', ARRAY['111111111']);
INSERT INTO Proveedores (id_proveedor, nombre, direccion, telefonos) VALUES ('PROV2', 'Proveedor 2', 'Calle 2', ARRAY['222222222']);
INSERT INTO Proveedores (id_proveedor, nombre, direccion, telefonos) VALUES ('PROV3', 'Proveedor 3', 'Calle 3', ARRAY['333333333']);

INSERT INTO Contrato (id_provedor, fecha_inicio, duracion) VALUES ('PROV1', '2020-01-01', 365*5);
INSERT INTO Contrato (id_provedor, fecha_inicio, duracion) VALUES ('PROV2', '2020-01-01', 365*5);
INSERT INTO Contrato (id_provedor, fecha_inicio, duracion) VALUES ('PROV3', '2020-01-01', 365);

INSERT INTO Tiendas (id_tienda, nombre, direccion, telefonos) VALUES ('TIENDA1', 'Tienda 1', 'Calle 1', ARRAY['111111111']);
INSERT INTO Tiendas (id_tienda, nombre, direccion, telefonos) VALUES ('TIENDA2', 'Tienda 2', 'Calle 2', ARRAY['222222222']);

INSERT INTO Envios (id_proveedor, id_tienda, productos, fecha, cantidades) VALUES ('PROV1', 'TIENDA1', ARRAY['VLOL1', 'MCAM1'], '2020-01-01', ARRAY[10, 10]);
INSERT INTO Envios (id_proveedor, id_tienda, productos, fecha, cantidades) VALUES ('PROV2', 'TIENDA2', ARRAY['PMOU1'], '2020-01-01', ARRAY[20]);

INSERT INTO Clientes (id_cliente, nombre, direccion, telefono) VALUES (45000000, 'Cliente 1', 'Calle 1', '111111111');
INSERT INTO Clientes (id_cliente, nombre, direccion, telefono) VALUES (45000001, 'Cliente 2', 'Calle 2', '222222222');

INSERT INTO Empleados (id_empleado, nombre, apellidos, salario) VALUES (99999999, 'Empleado 1', 'Apellido 1', 1000);
INSERT INTO Empleados (id_empleado, nombre, apellidos, salario) VALUES (99999998, 'Empleado 2', 'Apellido 2', 1000);

INSERT INTO Trabaja (id_tienda, id_empleado, cargo, fecha_inicio, duracion) VALUES ('TIENDA1', 99999999, 'Cajero', '2020-01-01', 365);
INSERT INTO Trabaja (id_tienda, id_empleado, cargo, fecha_inicio, duracion) VALUES ('TIENDA2', 99999998, 'Cajero', '2020-01-01', 365);

INSERT INTO Ventas (id_empleado, id_cliente, productos, cantidades) VALUES (99999999, 45000000, ARRAY['VLOL1', 'MCAM1'], ARRAY[1, 1]);
INSERT INTO Ventas (id_empleado, id_cliente, productos, cantidades) VALUES (99999998, 45000001, ARRAY['PMOU1'], ARRAY[2]);
INSERT INTO Ventas (id_empleado, id_cliente, productos, cantidades) VALUES (99999998, 45000001, ARRAY['PMOU1'], ARRAY[2]);

INSERT INTO Devoluciones (id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades) VALUES ('TIENDA1', '2023-12-20', 45000000, 1, ARRAY['VLOL1', 'MCAM1'], ARRAY[1, 1]);
INSERT INTO Devoluciones (id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades) VALUES ('TIENDA2', '2023-12-20', 45000001, 2, ARRAY['PMOU1'], ARRAY[1]);
INSERT INTO Devoluciones (id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades) VALUES ('TIENDA2', '2023-12-20', 45000001, 2, ARRAY['PMOU1'], ARRAY[1]);

SELECT * FROM Productos;
SELECT * FROM Videojuegos;
SELECT * FROM Merchandising;
SELECT * FROM Perifericos;
SELECT * FROM Proveedores;
SELECT * FROM Contrato;
SELECT * FROM Tiendas;
SELECT * FROM Envios;
SELECT * FROM Clientes;
SELECT * FROM Empleados;
SELECT * FROM Trabaja;
SELECT * FROM Ventas;
SELECT * FROM Devoluciones;
SELECT * FROM Disponibilidad;
