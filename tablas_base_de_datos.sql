CREATE DATABASE tienda;

\c tienda

DROP TABLE IF EXISTS PERIFERICOS CASCADE;
DROP TABLE IF EXISTS MERCHANDISING CASCADE;
DROP TABLE IF EXISTS VIDEOJUEGOS CASCADE;
DROP TABLE IF EXISTS VENTAS CASCADE;
DROP TABLE IF EXISTS TRABAJA CASCADE;
DROP TABLE IF EXISTS EMPLEADOS CASCADE;
DROP TABLE IF EXISTS DISPONIBILIDAD CASCADE;
DROP TABLE IF EXISTS PRODUCTOS CASCADE;
DROP TABLE IF EXISTS DEVOLUCIONES CASCADE;
DROP TABLE IF EXISTS CLIENTES CASCADE;
DROP TABLE IF EXISTS ENVIOS CASCADE;
DROP TABLE IF EXISTS TIENDAS CASCADE;
DROP TABLE IF EXISTS CONTRATO CASCADE;
DROP TABLE IF EXISTS PROVEEDORES CASCADE;

CREATE TABLE Productos (
    id_producto VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio NUMERIC(10,2) NOT NULL
);

CREATE TABLE Videojuegos (
    id_videojuego VARCHAR(50) PRIMARY KEY REFERENCES Productos(id_producto) ON DELETE CASCADE,
    plataforma VARCHAR(50) NOT NULL,
    genero VARCHAR(50) NOT NULL
);

CREATE TABLE Merchandising (
    id_merchandising VARCHAR(50) PRIMARY KEY REFERENCES Productos(id_producto) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE Perifericos (
    id_perifericos VARCHAR(50) PRIMARY KEY REFERENCES Productos(id_producto) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL
);

CREATE TABLE Proveedores (
    id_proveedor VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    telefonos VARCHAR(50)[] NOT NULL
);

CREATE TABLE Contrato (
    id_provedor VARCHAR(50) REFERENCES Proveedores(id_proveedor) ON DELETE CASCADE,
    fecha_inicio DATE CHECK (fecha_inicio >= DATE '2000-01-01') NOT NULL,
    fecha_fin DATE,
    duracion INT NOT NULL,
    PRIMARY KEY (id_provedor)
);

CREATE TABLE Tiendas (
    id_tienda VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    telefonos VARCHAR(50)[] NOT NULL
);

CREATE TABLE Envios (
    id_proveedor VARCHAR(50) REFERENCES Proveedores(id_proveedor) ON DELETE CASCADE,
    id_tienda VARCHAR(50) REFERENCES Tiendas(id_tienda) ON DELETE CASCADE,
    productos VARCHAR(50)[] NOT NULL,
    fecha DATE CHECK (fecha >= DATE '2000-01-01') NOT NULL,
    cantidades INT[] NOT NULL,
    PRIMARY KEY (id_proveedor, id_tienda, productos, fecha)
);

CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    telefono VARCHAR(50) NOT NULL
);

CREATE TABLE Disponibilidad (
    id_tienda VARCHAR(50) REFERENCES Tiendas(id_tienda) ON DELETE CASCADE,
    id_producto VARCHAR(50) REFERENCES Productos(id_producto) ON DELETE CASCADE,
    stock INT CHECK (stock >= 0) NOT NULL,
    PRIMARY KEY (id_tienda, id_producto)
);

CREATE TABLE Empleados (
    id_empleado INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    salario NUMERIC(10,2) CHECK (salario >= 1000) NOT NULL
);

CREATE TABLE Trabaja (
    id_tienda VARCHAR(50) REFERENCES Tiendas(id_tienda) ON DELETE CASCADE,
    id_empleado INT REFERENCES Empleados(id_empleado) ON DELETE CASCADE,
    cargo VARCHAR(50) NOT NULL,
    fecha_inicio DATE CHECK (fecha_inicio >= DATE '2000-01-01') NOT NULL,
    fecha_final DATE,
    duracion INT NOT NULL,
    PRIMARY KEY (id_tienda, id_empleado)
);

CREATE TABLE Ventas (
    id_empleado INT REFERENCES Empleados(id_empleado) ON DELETE CASCADE,
    id_cliente INT REFERENCES Clientes(id_cliente) ON DELETE CASCADE,
    fecha_venta DATE CHECK (fecha_venta >= DATE '2000-01-01'),
    id_venta INT,
    productos VARCHAR(50)[] NOT NULL,
    cantidades INT[] NOT NULL,
    total NUMERIC(10,2),
    PRIMARY KEY (id_empleado, id_cliente, fecha_venta, id_venta)
);

CREATE TABLE Devoluciones (
    id_tienda VARCHAR(50) REFERENCES Tiendas(id_tienda) ON DELETE CASCADE,
    fecha_venta DATE CHECK (fecha_venta >= DATE '2000-01-01') NOT NULL,
    id_cliente INT REFERENCES Clientes(id_cliente) ON DELETE CASCADE,
    fecha_devolucion DATE CHECK (fecha_devolucion >= DATE '2000-01-01') NOT NULL,
    id_venta INT NOT NULL,
    id_devolucion INT NOT NULL,
    productos VARCHAR(50)[] NOT NULL,
    cantidades INT[] NOT NULL,
    PRIMARY KEY (id_tienda, fecha_venta, id_cliente, fecha_devolucion, id_devolucion, id_venta)
);
--Trigger para establece fecha devolución y establecer id_devolucion
CREATE OR REPLACE FUNCTION establecer_fecha_e_id_devolucion() RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_devolucion := CURRENT_DATE;
    
    -- Recuperar el último el último id_devolucion de la tabla Devoluciones, si no hay ninguno se pone a 1, si hay se incrementa en 1
    IF EXISTS (SELECT 1 FROM Devoluciones WHERE fecha_venta = NEW.fecha_venta AND id_cliente = NEW.id_cliente) THEN
        NEW.id_devolucion := (SELECT id_devolucion FROM Devoluciones WHERE fecha_venta = NEW.fecha_venta AND id_cliente = NEW.id_cliente ORDER BY id_devolucion DESC LIMIT 1) + 1;
    ELSE
        NEW.id_devolucion := 1;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER establecer_fecha_devolucion_trigger BEFORE INSERT ON Devoluciones FOR EACH ROW EXECUTE FUNCTION establecer_fecha_e_id_devolucion();

-- Trigger para establecer el id_venta
CREATE OR REPLACE FUNCTION establecer_id_venta() RETURNS TRIGGER AS $$
BEGIN
    -- Recuperar el último el último id_venta de la tabla Ventas, si no hay ninguno se pone a 1, si hay se incrementa en 1
    IF EXISTS (SELECT 1 FROM Ventas WHERE id_cliente = NEW.id_cliente AND fecha_venta = NEW.fecha_venta) THEN
        NEW.id_venta := (SELECT id_venta FROM Ventas WHERE id_cliente = NEW.id_cliente AND fecha_venta = NEW.fecha_venta ORDER BY id_venta DESC LIMIT 1) + 1;
    ELSE
        NEW.id_venta := 1;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER establecer_id_venta_trigger BEFORE INSERT ON Ventas FOR EACH ROW EXECUTE FUNCTION establecer_id_venta();

-- Trigger para establecer la fecha de compra
CREATE OR REPLACE FUNCTION establecer_fecha_venta() RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_venta := CURRENT_DATE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER establecer_fecha_venta_trigger BEFORE INSERT ON Ventas FOR EACH ROW EXECUTE FUNCTION establecer_fecha_venta();

-- Cuando se recibe en un envío, se añade el stock recibido a la tienda, envio tiene productos y cantidades, la posición de cada producto en el array corresponde con la posición de la cantidad en el otro array
CREATE OR REPLACE FUNCTION actualizar_stock() RETURNS TRIGGER AS $$
BEGIN
    FOR i IN 1..array_length(NEW.productos, 1) LOOP
        IF EXISTS (SELECT 1 FROM Disponibilidad WHERE id_tienda = NEW.id_tienda AND id_producto = NEW.productos[i]) THEN
            UPDATE Disponibilidad SET stock = stock + NEW.cantidades[i] WHERE id_tienda = NEW.id_tienda AND id_producto = NEW.productos[i];
        ELSE
            INSERT INTO Disponibilidad VALUES (NEW.id_tienda, NEW.productos[i], NEW.cantidades[i]);
        END IF;
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER actualizar_stock_trigger AFTER INSERT ON Envios FOR EACH ROW EXECUTE FUNCTION actualizar_stock();

-- Antes de añadir un contrato hay que calcular la fecha final
CREATE OR REPLACE FUNCTION calcular_fecha_final_contrato() RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_fin := NEW.fecha_inicio + NEW.duracion;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calcular_fecha_final_contrato_trigger BEFORE INSERT ON Contrato FOR EACH ROW EXECUTE FUNCTION calcular_fecha_final_contrato();

-- Antes de añadir un envio hay que comprobar si ha finalizado el contrato con el proveedor
CREATE OR REPLACE FUNCTION verificar_contrato() RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT fecha_fin FROM Contrato WHERE id_provedor = NEW.id_proveedor) < CURRENT_DATE THEN
        RAISE EXCEPTION 'El contrato con el proveedor ha finalizado.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER verificar_contrato_trigger BEFORE INSERT ON Envios FOR EACH ROW EXECUTE FUNCTION verificar_contrato();

-- Antes de procesar una devolucion se comprueba si existe una compra con los mismos datos, si no existe se lanza una excepción
-- Luego hay que comprobar producto a producto si los que se intentan devolver ya han sido devueltos, si alguno ya ha sido devuelto se lanza una excepción. Hay que tener en cuenta que puede haber comprado más de un producto
CREATE OR REPLACE FUNCTION verificar_devolucion() RETURNS TRIGGER AS $$
DECLARE
    productos_comprados RECORD;
    row RECORD;

BEGIN
    IF NOT EXISTS (SELECT 1 FROM Ventas WHERE id_cliente = NEW.id_cliente AND fecha_venta = NEW.fecha_venta AND id_venta = NEW.id_venta) THEN
        RAISE EXCEPTION 'No existe una compra con esos datos.';
    END IF;

    SELECT productos, cantidades INTO productos_comprados FROM Ventas WHERE id_cliente = NEW.id_cliente AND fecha_venta = NEW.fecha_venta AND id_venta = NEW.id_venta and id_venta = NEW.id_venta;

    -- Recorremos todos los productos que se quieren devolver y comprobamos si están en la compra original
    FOR i IN 1..array_length(NEW.productos, 1) LOOP
        IF NOT (NEW.productos[i] = ANY(productos_comprados.productos)) THEN
            RAISE EXCEPTION 'El producto % no se compró.', NEW.productos[i];
        END IF;
    END LOOP;

    FOR row IN SELECT productos, cantidades FROM Devoluciones WHERE fecha_venta = NEW.fecha_venta AND id_cliente = NEW.id_cliente AND id_venta = NEW.id_venta LOOP
        FOR i IN 1..array_length(row.productos, 1) LOOP
            FOR j IN 1..array_length(productos_comprados.productos, 1) LOOP
                IF row.productos[i] = productos_comprados.productos[j] THEN
                    productos_comprados.cantidades[j] := productos_comprados.cantidades[j] - row.cantidades[i];
                END IF;
            END LOOP;
        END LOOP;
    END LOOP;

    -- AHORA tocar restar los new.cantidades a productos_comprados.cantidades
    FOR i IN 1..array_length(NEW.productos, 1) LOOP
        FOR j IN 1..array_length(productos_comprados.productos, 1) LOOP
            IF NEW.productos[i] = productos_comprados.productos[j] THEN
                productos_comprados.cantidades[j] := productos_comprados.cantidades[j] - NEW.cantidades[i];
                IF productos_comprados.cantidades[j] < 0 THEN
                    RAISE EXCEPTION 'No se puede devolver más productos % de los que se compraron.', NEW.productos[i];
                END IF;
            END IF;
        END LOOP;
    END LOOP;


    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER verificar_devolucion_trigger BEFORE INSERT ON Devoluciones FOR EACH ROW EXECUTE FUNCTION verificar_devolucion();

-- Trigger para que tras haber realizado la devolución se añadirá al stock la cantidad devuelta de cada producto
CREATE OR REPLACE FUNCTION devolucion_stock() RETURNS TRIGGER AS $$
BEGIN
    FOR i IN 1..array_length(NEW.productos, 1) LOOP
        IF EXISTS (SELECT 1 FROM Disponibilidad WHERE id_tienda = NEW.id_tienda AND id_producto = NEW.productos[i]) THEN
            UPDATE Disponibilidad SET stock = stock + NEW.cantidades[i] WHERE id_tienda = NEW.id_tienda AND id_producto = NEW.productos[i];
        ELSE
            INSERT INTO Disponibilidad VALUES (NEW.id_tienda, NEW.productos[i], NEW.cantidades[i]);
        END IF;
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER devolucion_stock_trigger AFTER INSERT ON Devoluciones FOR EACH ROW EXECUTE FUNCTION devolucion_stock();

-- Antes de la venta se comprueba si hay existencias en la tienda en la que trabaja el empleado 
CREATE OR REPLACE FUNCTION verificar_stock() RETURNS TRIGGER AS $$
BEGIN
    FOR i IN 1..array_length(NEW.productos, 1) LOOP
        -- Si no existe el producto en la tienda se lanza una excepción
        IF NOT EXISTS (SELECT 1 FROM Disponibilidad WHERE id_tienda = (SELECT id_tienda FROM Trabaja WHERE id_empleado = NEW.id_empleado) AND id_producto = NEW.productos[i]) THEN
            RAISE EXCEPTION 'No existe el producto % en la tienda.', NEW.productos[i];
        END IF;

        IF (SELECT stock FROM Disponibilidad WHERE id_tienda = (SELECT id_tienda FROM Trabaja WHERE id_empleado = NEW.id_empleado) AND id_producto = NEW.productos[i]) < NEW.cantidades[i] THEN
        RAISE EXCEPTION 'No hay suficientes existencias en la tienda del producto %', NEW.productos[i];
        END IF;
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER verificar_stock_trigger BEFORE INSERT ON Ventas FOR EACH ROW EXECUTE FUNCTION verificar_stock();

-- Después de la venta se resta la cantidad comprada al stock de producto en la tienda donde trabaja el empleado
CREATE OR REPLACE FUNCTION venta_stock() RETURNS TRIGGER AS $$
BEGIN
    FOR i IN 1..array_length(NEW.productos, 1) LOOP
        UPDATE Disponibilidad SET stock = stock - NEW.cantidades[i] WHERE id_tienda = (SELECT id_tienda FROM Trabaja WHERE id_empleado = NEW.id_empleado) AND id_producto = NEW.productos[i];
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER venta_stock_trigger AFTER INSERT ON Ventas FOR EACH ROW EXECUTE FUNCTION venta_stock();

-- Antes de la venta se calcula el total
CREATE OR REPLACE FUNCTION calcular_total() RETURNS TRIGGER AS $$
BEGIN
    NEW.total := 0;
    FOR i IN 1..array_length(NEW.productos, 1) LOOP
        NEW.total := NEW.total + (SELECT precio FROM Productos WHERE id_producto = NEW.productos[i]) * NEW.cantidades[i];
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calcular_total_trigger BEFORE INSERT ON Ventas FOR EACH ROW EXECUTE FUNCTION calcular_total();

-- Antes de añadir una entrada en trabaja comprobar si el empleado está trabajando actualmente en alguna 
-- Calculamos la fecha final
CREATE OR REPLACE FUNCTION verificar_empleado() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM Trabaja WHERE id_empleado = NEW.id_empleado AND new.fecha_inicio < fecha_final) THEN
        RAISE EXCEPTION 'El empleado ya está trabajando en otra tienda.';
    END IF;

    NEW.fecha_final := NEW.fecha_inicio + NEW.duracion;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER verificar_empleado_trigger BEFORE INSERT ON Trabaja FOR EACH ROW EXECUTE FUNCTION verificar_empleado();