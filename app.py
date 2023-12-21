import os
import psycopg2
from flask import Flask, request, url_for, redirect, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
        	database="tienda",
        # user=os.environ['DB_USERNAME'],
		user="postgres",
		# password=os.environ['DB_PASSWORD']
        password="kiara312")
    return conn

def insert_into_productos(id_producto, nombre, precio):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO productos (id_producto, nombre, precio) VALUES (%s, %s, %s);', (id_producto, nombre, precio))
        conn.commit()
        cur.close()
        conn.close()
        
def insert_into_videojuegos(id_producto, plataforma, genero):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO videojuegos (id_videojuego, plataforma, genero) VALUES (%s, %s, %s);', (id_producto, plataforma, genero))
    conn.commit()
    cur.close()
    conn.close()
    
def insert_into_merchandising(id_producto, tipo):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO merchandising (id_merchandising, tipo) VALUES (%s, %s);', (id_producto, tipo))
    conn.commit()
    cur.close()
    conn.close()
    
def insert_into_perifericos(id_producto, tipo, marca):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO perifericos (id_periferico, tipo, marca) VALUES (%s, %s, %s);', (id_producto, tipo, marca))
    conn.commit()
    cur.close()
    conn.close()
    
def insert_into_devoluciones(id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO devoluciones (id_tienda, fecha_venta, id_cliente, fecha_devolucion, id_venta, id_devolucion, productos, cantidades) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (id_tienda, fecha_venta, id_cliente, fecha_venta, id_venta, id_venta, productos, cantidades))
    conn.commit()
    cur.close()
    conn.close()

# Rutas para Productos
@app.route('/productos', methods=['GET','POST'])
def insert_producto():
    if request.method == 'POST':
        data = request.get_json()  # Obtén los datos del cuerpo de la solicitud POST

        id_producto = data.get('id_producto')
        nombre = data.get('nombre')
        precio = data.get('precio')
        tipo = id_producto[0]  # Este campo determinará en qué tabla se insertará

        # Primero, inserta en la tabla Productos
        if not (tipo == 'V' or tipo == 'M' or tipo == 'P'):
             return jsonify({"status": "fail", "message": "No se pudo insertar el producto, tipo inválido. Recuerda que el tipo debe ser V, M o P (Videojuego, Merchandising o Periférico)"})
         
        insert_into_productos(id_producto, nombre, precio)

        # Luego, en función del tipo, inserta en la tabla correspondiente
        if tipo == 'V':
            plataforma = data.get('plataforma')
            genero = data.get('genero')
            insert_into_videojuegos(id_producto, plataforma, genero)
            return jsonify({"status": "success", "message": "Producto insertado correctamente"})
        elif tipo == 'M':
            tipo = data.get('tipo')
            insert_into_merchandising(id_producto, tipo)
            return jsonify({"status": "success", "message": "Producto insertado correctamente"})
        elif tipo == 'P':
            tipo = data.get('tipo')
            marca = data.get('marca')
            insert_into_perifericos(id_producto, tipo, marca)
            return jsonify({"status": "success", "message": "Producto insertado correctamente"})

    if request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM productos;')
        productos = cur.fetchall()
        productos_json = []
        for producto in productos:
            tipo = producto[0][0]
            if tipo == 'V':
                cur.execute('SELECT * FROM videojuegos WHERE id_videojuego = %s;', (producto[0],))
            elif tipo == 'M':
                cur.execute('SELECT * FROM merchandising WHERE id_merchandising = %s;', (producto[0],))
            elif tipo == 'P':
                cur.execute('SELECT * FROM perifericos WHERE id_periferico = %s;', (producto[0],))
            producto_aux = cur.fetchone()
            producto_json = {
                "id_producto": producto[0],
                "nombre": producto[1],
                "precio": producto[2]
            }
            if tipo == 'V':
                producto_json["plataforma"] = producto_aux[1]
                producto_json["genero"] = producto_aux[2]
            elif tipo == 'M':
                producto_json["tipo"] = producto_aux[1]
            elif tipo == 'P':
                producto_json["tipo"] = producto_aux[1]
                producto_json["marca"] = producto_aux[2]
            productos_json.append(producto_json)
        cur.close()
        conn.close()
        return jsonify(productos_json)

@app.route('/productos/<id_producto>', methods=['GET','PUT','DELETE'])
def get_productos_id(id_producto):
    if request.method == 'DELETE':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM productos WHERE id_producto = %s;', (id_producto,))
        conn.commit()
        
        if cur.rowcount > 0:
            tipo = id_producto[0]
            if tipo == 'V':
                cur.execute('DELETE FROM videojuegos WHERE id_videojuego = %s;', (id_producto,))
            elif tipo == 'M':
                cur.execute('DELETE FROM merchandising WHERE id_merchandising = %s;', (id_producto,))
            elif tipo == 'P':
                cur.execute('DELETE FROM perifericos WHERE id_periferico = %s;', (id_producto,))
            cur.close()
            conn.close()
            return jsonify({"status": "success", "message": "Producto eliminado correctamente"})
        else:
            cur.close()
            conn.close()
            return jsonify({"status": "fail", "message": "No se pudo eliminar el producto"})

    elif request.method == 'PUT':
        data = request.get_json()
        nombre = data.get('nombre')
        precio = data.get('precio')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM productos WHERE id_producto = %s;', (id_producto,))
        producto = cur.fetchone()
        if producto is None:
            return jsonify({"status": "fail", "message": "No se pudo actualizar el producto, no existe"})
        else:
            if nombre is None:
                nombre = producto[1]
            if precio is None:
                precio = producto[2]
        cur.execute('UPDATE productos SET nombre = %s, precio = %s WHERE id_producto = %s;', (nombre, precio, id_producto))
        tipo = id_producto[0]
        if tipo == 'V':
            plataforma = data.get('plataforma')
            genero = data.get('genero')
            cur.execute('SELECT * FROM videojuegos WHERE id_videojuego = %s;', (id_producto,))
            producto = cur.fetchone()
            if plataforma is None:
                plataforma = producto[1]
            if genero is None:
                genero = producto[2]
            cur.execute('UPDATE videojuegos SET plataforma = %s, genero = %s WHERE id_videojuego = %s;', (plataforma, genero, id_producto))
        elif tipo == 'M':
            tipo = data.get('tipo')
            cur.execute('SELECT * FROM merchandising WHERE id_merchandising = %s;', (id_producto,))
            producto = cur.fetchone()
            if tipo is None:
                tipo = producto[1]
            cur.execute('UPDATE merchandising SET tipo = %s WHERE id_merchandising = %s;', (tipo, id_producto))
        elif tipo == 'P':
            tipo = data.get('tipo')
            marca = data.get('marca')
            cur.execute('SELECT * FROM perifericos WHERE id_periferico = %s;', (id_producto,))
            producto = cur.fetchone()
            if tipo is None:
                tipo = producto[1]
            if marca is None:
                marca = producto[2]
            cur.execute('UPDATE perifericos SET tipo = %s, marca = %s WHERE id_periferico = %s;', (tipo, marca, id_producto))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "message": "Producto actualizado correctamente"})
    
    elif request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM productos WHERE id_producto = %s;', (id_producto,))
        producto = cur.fetchone()
        if producto is None:
            return jsonify({"status": "fail", "message": "No se pudo encontrar el producto"})

        json_producto = {
            "id_producto": producto[0],
            "nombre": producto[1],
            "precio": producto[2]
        }
        tipo = id_producto[0]
        
        if tipo == 'V':
            cur.execute('SELECT * FROM videojuegos WHERE id_videojuego = %s;', (id_producto,))
            producto = cur.fetchone()
            json_producto["plataforma"] = producto[1]
            json_producto["genero"] = producto[2]
        elif tipo == 'M':
            cur.execute('SELECT * FROM merchandising WHERE id_merchandising = %s;', (id_producto,))
            producto = cur.fetchone()
            json_producto["tipo"] = producto[1]
        elif tipo == 'P':
            cur.execute('SELECT * FROM perifericos WHERE id_periferico = %s;', (id_producto,))
            producto = cur.fetchone()
            json_producto["tipo"] = producto[1]
            json_producto["marca"] = producto[2]
        
        cur.close()
        conn.close()    
        return jsonify(json_producto)    

    
# Rutas para Videojuegos
@app.route('/videojuegos', methods=['GET'])
def get_videojuegos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT productos.id_producto, nombre, precio, plataforma, genero FROM videojuegos JOIN productos ON videojuegos.id_videojuego = productos.id_producto;')
    videojuegos = cur.fetchall()
    cur.close()
    conn.close()
    json_videojuegos = []
    for videojuego in videojuegos:
        json_videojuego = {
            "id_producto": videojuego[0],
            "nombre": videojuego[1],
            "precio": videojuego[2],
            "plataforma": videojuego[3],
            "genero": videojuego[4]
        }
        json_videojuegos.append(json_videojuego)
    return jsonify(json_videojuegos)

# Rutas para Merchandising
@app.route('/merchandising', methods=['GET'])
def get_merchandising():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT productos.id_producto, nombre, precio, tipo FROM merchandising JOIN productos ON merchandising.id_merchandising = productos.id_producto;')
    merchandising = cur.fetchall()
    cur.close()
    conn.close()
    
    json_merchandising = []
    for merch in merchandising:
        json_merch = {
            "id_producto": merch[0],
            "nombre": merch[1],
            "precio": merch[2],
            "tipo": merch[3]
        }
        json_merchandising.append(json_merch)
    return jsonify(json_merchandising)
    
# Rutas para Perifericos
@app.route('/perifericos', methods=['GET'])
def get_perifericos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT productos.id_producto, nombre, precio, tipo, marca FROM perifericos JOIN productos ON perifericos.id_periferico = productos.id_producto;')
    perifericos = cur.fetchall()
    cur.close()
    conn.close()
    
    json_perifericos = []
    for periferico in perifericos:
        json_periferico = {
            "id_producto": periferico[0],
            "nombre": periferico[1],
            "precio": periferico[2],
            "tipo": periferico[3],
            "marca": periferico[4]
        }
        json_perifericos.append(json_periferico)
    return jsonify(json_perifericos)

# Rutas para Proveedores
@app.route('/proveedores', methods=['GET'])
def get_proveedores():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM proveedores;')
    proveedores = cur.fetchall()
    cur.close()
    conn.close()
    
    json_proveedores = []
    for proveedor in proveedores:
        json_proveedor = {
            "id_proveedor": proveedor[0],
            "nombre": proveedor[1],
            "direccion": proveedor[2],
            "telefono": proveedor[3]
        }
        json_proveedores.append(json_proveedor)
    return jsonify(json_proveedores)

@app.route('/proveedores/<id_proveedor>', methods=['GET', 'DELETE'])
def get_proveedores_id(id_proveedor):
    if request.method == 'DELETE':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM proveedores WHERE id_proveedor = %s;', (id_proveedor,))
        conn.commit()
        cur.close()
        conn.close()
        if cur.rowcount > 0:
            return jsonify({"status": "success", "message": "Proveedor eliminado correctamente"})
        else:
            return jsonify({"status": "fail", "message": "No se pudo eliminar el proveedor"})
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM proveedores WHERE id_proveedor = %s;', (id_proveedor,))
        proveedor = cur.fetchone()
        cur.close()
        conn.close()
        
        if proveedor is None:
            return jsonify({"status": "fail", "message": "No se pudo encontrar el proveedor"})
        
        json_proveedor = {
            "id_proveedor": proveedor[0],
            "nombre": proveedor[1],
            "direccion": proveedor[2],
            "telefono": proveedor[3]
        }
        
        return jsonify(json_proveedor)

# Rutas para Tiendas
@app.route('/tiendas', methods=['GET'])
def get_tiendas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tiendas;')
    tiendas = cur.fetchall()
    cur.close()
    conn.close()
    
    json_tiendas = []
    for tienda in tiendas:
        json_tienda = {
            "id_tienda": tienda[0],
            "nombre": tienda[1],
            "direccion": tienda[2],
            "telefono": tienda[3]
        }
        json_tiendas.append(json_tienda)
    return jsonify(json_tiendas)

@app.route('/tiendas/<id_tienda>', methods=['GET', 'DELETE'])
def get_tiendas_id(id_tienda):
    if request.method == 'DELETE':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tiendas WHERE id_tienda = %s;', (id_tienda,))
        conn.commit()
        cur.close()
        conn.close()
        if cur.rowcount > 0:
            return jsonify({"status": "success", "message": "Tienda eliminada correctamente"})
        else:
            return jsonify({"status": "fail", "message": "No se pudo eliminar la tienda"})
    elif request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM tiendas WHERE id_tienda = %s;', (id_tienda,))
        tienda = cur.fetchone()
        cur.close()
        conn.close()
        
        if tienda is None:
            return jsonify({"status": "fail", "message": "No se pudo encontrar la tienda"})
        else:
            json_tienda = {
                "id_tienda": tienda[0],
                "nombre": tienda[1],
                "direccion": tienda[2],
                "telefono": tienda[3]
            }
            return jsonify(json_tienda)

# Rutas para Envios
@app.route('/envios', methods=['GET'])
def get_envios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM envios;')
    envios = cur.fetchall()
    cur.close()
    conn.close()
    
    json_envios = []
    for envios in envios:
        json_envio = {
            "id_proveedor": envios[0],
            "id_tienda": envios[1],
            "productos": envios[2],
            "fecha": envios[3],
            "cantidades": envios[4]
        }
        json_envios.append(json_envio)
    return jsonify(json_envios)


@app.route('/envios/proveedor/<id_proveedor>', methods=['GET'])
def get_envios_proveedor(id_proveedor):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM envios WHERE id_proveedor = %s;', (id_proveedor,))
    envios = cur.fetchall()
    cur.close()
    conn.close()
    
    json_envios = []
    for envio in envios:
        json_envio = {
            "id_proveedor": envio[0],
            "id_tienda": envio[1],
            "productos": envio[2],
            "fecha": envio[3],
            "cantidades": envio[4]
        }
        json_envios.append(json_envio)
    return jsonify(json_envios)

@app.route('/envios/tienda/<id_tienda>', methods=['GET'])
def get_envios_tienda(id_tienda):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM envios WHERE id_tienda = %s;', (id_tienda,))
    envios = cur.fetchall()
    cur.close()
    conn.close()
    
    json_envios = []
    for envio in envios:
        json_envio = {
            "id_proveedor": envio[0],
            "id_tienda": envio[1],
            "productos": envio[2],
            "fecha": envio[3],
            "cantidades": envio[4]
        }
        json_envios.append(json_envio)
    return jsonify(json_envios)

# Rutas para Clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
   
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes;')
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        
        json_clientes = []
        for cliente in clientes:
            json_cliente = {
                "id_cliente": cliente[0],
                "nombre": cliente[1],
                "direccion": cliente[2],
                "telefono": cliente[3]
            }
            json_clientes.append(json_cliente)
        return jsonify(json_clientes)
    
@app.route('/clientes/<id_cliente>', methods=['GET', 'PUT', 'DELETE'])
def get_clientes_id(id_cliente):
    if request.method == 'DELETE':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM clientes WHERE id_cliente = %s;', (id_cliente,))
        conn.commit()
        cur.close()
        conn.close()
        
        if cur.rowcount > 0:
            return jsonify({"status": "success", "message": "Cliente eliminado correctamente"})
        else:
            return jsonify({"status": "fail", "message": "No se pudo eliminar el cliente"})
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes WHERE id_cliente = %s;', (id_cliente,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        
        if cliente is None:
            return jsonify({"status": "fail", "message": "No se pudo encontrar el cliente"})
        else:
            json_cliente = {
                "id_cliente": cliente[0],
                "nombre": cliente[1],
                "direccion": cliente[2],
                "telefono": cliente[3]
            }
            return jsonify(json_cliente)

# Rutas para Disponibilidad
@app.route('/disponibilidad', methods=['GET'])
def get_disponibilidad():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM disponibilidad;')
    disponibilidad = cur.fetchall()
    cur.close()
    conn.close()
    
    json_disponibilidad = []
    for disp in disponibilidad:
        json_disp = {
            "id_tienda": disp[0],
            "id_producto": disp[1],
            "cantidad": disp[2]
        }
        json_disponibilidad.append(json_disp)
        
    return jsonify(json_disponibilidad)

@app.route('/disponibilidad/tienda/<id_tienda>/', methods=['GET'])
def get_disponibilidad_tienda(id_tienda):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT disponibilidad.id_producto, stock FROM disponibilidad WHERE id_tienda = %s;', (id_tienda,))
    disponibilidad = cur.fetchall()
    cur.close()
    conn.close()
    
    json_disponibilidad = []
    for disp in disponibilidad:
        json_disp = {
            "id_producto": disp[0],
            "cantidad": disp[1]
        }
        json_disponibilidad.append(json_disp)
        
    return jsonify(json_disponibilidad)

@app.route('/disponibilidad/tienda/<id_tienda>/producto/<id_producto>/', methods=['GET'])
def get_disponibilidad_tienda_producto(id_tienda, id_producto):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT stock FROM disponibilidad WHERE id_tienda = %s AND id_producto = %s;', (id_tienda, id_producto))
        
        cantidad = cur.fetchone()
        cur.close()
        conn.close()
        
        if cantidad is None:
            return jsonify({"status": "fail", "message": "No se pudo encontrar la disponibilidad"})
        else:
            json_cantidad = {
                "cantidad": cantidad[0]
            }
            return jsonify(json_cantidad)

# Rutas para Empleados
@app.route('/empleados', methods=['GET'])
def get_empleados():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM empleados;')
    empleados = cur.fetchall()
    cur.close()
    conn.close()
    
    json_empleados = []
    for empleado in empleados:
        json_empleado = {
            "id_empleado": empleado[0],
            "nombre": empleado[1],
            "apellidos": empleado[2],
            "salario": empleado[3]
        }
        json_empleados.append(json_empleado)
        
    return jsonify(json_empleados)


@app.route('/empleados/<id_empleado>', methods=['GET', 'DELETE'])
def get_empleados_id(id_empleado):
    if request.method == 'DELETE':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM empleados WHERE id_empleado = %s;', (id_empleado,))
        conn.commit()
        cur.close()
        conn.close()
        
        if cur.rowcount > 0:
            return jsonify({"status": "success", "message": "Empleado eliminado correctamente"})
        else:
            return jsonify({"status": "fail", "message": "No se pudo eliminar el empleado"})
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM empleados WHERE id_empleado = %s;', (id_empleado,))
        empleado = cur.fetchone()
        cur.close()
        conn.close()
        
        if empleado is None:
            return jsonify({"status": "fail", "message": "No se pudo encontrar el empleado"})
        else:
            json_empleado = {
                "id_empleado": empleado[0],
                "nombre": empleado[1],
                "apellidos": empleado[2],
                "salario": empleado[3]
            }
            return jsonify(json_empleado)

# Rutas para Trabaja
@app.route('/trabaja', methods=['GET'])
def get_trabaja():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM trabaja;')
    trabaja = cur.fetchall()
    cur.close()
    conn.close()
    
    json_trabaja = []
    for trab in trabaja:
        json_trab = {
            "id_tienda": trab[0],
            "id_empleado": trab[1],
            "cargo": trab[2],
            "fecha_inicio": trab[3],
            "fecha_final": trab[4],
            "duración": trab[5]
        }
        json_trabaja.append(json_trab)
    return jsonify(json_trabaja)

@app.route('/trabaja/tienda/<id_tienda>', methods=['GET'])
def get_trabaja_tienda(id_tienda):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM trabaja WHERE id_tienda = %s;', (id_tienda,))
    trabaja = cur.fetchall()
    cur.close()
    conn.close()
    
    json_trabaja = []
    for trab in trabaja:
        json_trab = {
            "id_tienda": trab[0],
            "id_empleado": trab[1],
            "cargo": trab[2],
            "fecha_inicio": trab[3],
            "fecha_final": trab[4],
            "duración": trab[5]
        }
        json_trabaja.append(json_trab)
    return jsonify(json_trabaja)

@app.route('/trabaja/empleado/<id_empleado>', methods=['GET', 'DELETE'])
def get_trabaja_empleado(id_empleado):
    if request.method == 'DELETE':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM trabaja WHERE id_empleado = %s;', (id_empleado,))
        conn.commit()
        cur.close()
        conn.close()
        
        if cur.rowcount > 0:
            return jsonify({"status": "success", "message": "Trabajo eliminado correctamente"})
        else:
            return jsonify({"status": "fail", "message": "No se pudo eliminar el trabajo"})
        
    elif request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM trabaja WHERE id_empleado = %s;', (id_empleado,))
        trabaja = cur.fetchone()
        cur.close()
        conn.close()

        if trabaja is None:
            return jsonify({"status": "fail", "message": "No se pudo encontrar el trabajo"})
        json_trab = {
            "id_tienda": trabaja[0],
            "id_empleado": trabaja[1],
            "cargo": trabaja[2],
            "fecha_inicio": trabaja[3],
            "fecha_final": trabaja[4],
            "duración": trabaja[5]
        }
        return jsonify(json_trab)

# Rutas para Ventas
@app.route('/ventas/', methods=['GET','POST'])
def get_ventas():
    if request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM ventas;')
        ventas = cur.fetchall()
        cur.close()
        conn.close()

        json_ventas = []
        for venta in ventas:
            json_venta = {
                "id_empleado": venta[0],
                "id_cliente": venta[1],
                "fecha_venta": venta[2],
                "id_venta": venta[3],
                "productos": venta[4],
                "cantidades": venta[5],
                "total": venta[6]
            }
            json_ventas.append(json_venta)

        return jsonify(json_ventas)
            
    if request.method == 'POST':
        data = request.get_json()
        id_empleado = data.get('id_empleado')
        id_cliente = data.get('id_cliente')
        productos = data.get('productos')
        cantidades = data.get('cantidades')
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO ventas (id_empleado, id_cliente, productos, cantidades) VALUES (%s, %s, %s, %s);', (id_empleado, id_cliente, productos, cantidades))
        
        conn.commit()
        if cur.rowcount == 0:
            cur.close()
            conn.close()
            return jsonify({"status": "fail", "message": "No se pudo insertar la venta"})
        
        cur.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Venta insertada correctamente"})

    
@app.route('/ventas/tienda/<id_tienda>', methods=['GET'])
def get_ventas_tienda(id_tienda):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_empleado FROM trabaja WHERE id_tienda = %s;', (id_tienda,))
    empleados = cur.fetchall()
    
    ids_empleados = [empleado[0] for empleado in empleados]
    ids_empleados = tuple(ids_empleados)
    
    cur.execute('SELECT * FROM ventas WHERE id_empleado IN %s;', (ids_empleados,))
    
    ventas = cur.fetchall()
    cur.close()
    conn.close()
    
    json_ventas = []
    for venta in ventas:
        json_venta = {
            "id_empleado": venta[0],
            "id_cliente": venta[1],
            "fecha_venta": venta[2],
            "id_venta": venta[3],
            "productos": venta[4],
            "cantidades": venta[5],
            "total": venta[6]
        }
        json_ventas.append(json_venta)
        
    return jsonify(json_ventas)

@app.route('/ventas/cliente/<id_cliente>', methods=['GET'])
def get_ventas_cliente(id_cliente):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM ventas WHERE id_cliente = %s;', (id_cliente,))
    ventas = cur.fetchall()
    cur.close()
    conn.close()
    
    json_ventas = []
    for venta in ventas:
        json_venta = {
            "id_empleado": venta[0],
            "id_cliente": venta[1],
            "fecha_venta": venta[2],
            "id_tienda": venta[3],
            "productos": venta[4],
            "cantidades": venta[5],
            "total": venta[6]
        }
        json_ventas.append(json_venta)
        
    return jsonify(json_ventas)

@app.route('/ventas/empleado/<id_empleado>', methods=['GET'])
def get_ventas_empleado(id_empleado):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM ventas WHERE id_empleado = %s;', (id_empleado,))
    ventas = cur.fetchall()
    cur.close()
    conn.close()
    json_ventas = []
    
    for venta in ventas:
        json_venta = {
            "id_empleado": venta[0],
            "id_cliente": venta[1],
            "fecha_venta": venta[2],
            "id_tienda": venta[3],
            "productos": venta[4],
            "cantidades": venta[5],
            "total": venta[6]
        }
        json_ventas.append(json_venta)
        
    return jsonify(json_ventas)

# Rutas para Devoluciones
@app.route('/devoluciones', methods=['GET','POST'])
def get_devoluciones():
    if request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM devoluciones;')
        devoluciones = cur.fetchall()
        cur.close()
        conn.close()

        json_devoluciones = []
        for devolucion in devoluciones:
            json_devolucion = {
                "id_tienda": devolucion[0],
                "fecha_venta": devolucion[1],
                "id_cliente": devolucion[2],
                "fecha_devolucion": devolucion[3],
                "id_venta": devolucion[4],
                "id_devolucion": devolucion[5],
                "productos": devolucion[6],
                "cantidades": devolucion[7]
            }
            json_devoluciones.append(json_devolucion)

        return jsonify(json_devoluciones)

    elif request.method == 'POST':
        data = request.get_json()
        id_tienda = data.get('id_tienda')
        fecha_venta = data.get('fecha_venta')
        id_cliente = data.get('id_cliente')
        id_venta = data.get('id_venta')
        productos = data.get('productos')
        cantidades = data.get('cantidades')
        
        if not (id_tienda and fecha_venta and id_cliente and id_venta and productos and cantidades):
            return jsonify({"status": "fail", "message": "No se pudo insertar la devolución, faltan campos"})
        
        insert_into_devoluciones(id_tienda, fecha_venta, id_cliente, id_venta, productos, cantidades)
        
        return jsonify({"status": "success", "message": "Devolución insertada correctamente"})
        

@app.route('/devoluciones/<id_tienda>', methods=['GET'])
def get_devoluciones_id(id_tienda):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM devoluciones WHERE id_tienda = %s;', (id_tienda,))
    devoluciones = cur.fetchall()
    cur.close()
    conn.close()
    
    json_devoluciones = []
    for devolucion in devoluciones:
        json_devolucion = {
            "id_tienda": devolucion[0],
            "fecha_venta": devolucion[1],
            "id_cliente": devolucion[2],
            "fecha_devolucion": devolucion[3],
            "id_venta": devolucion[4],
            "id_devolucion": devolucion[5],
            "productos": devolucion[6],
            "cantidades": devolucion[7]
        }
        json_devoluciones.append(json_devolucion)
        
    return jsonify(json_devoluciones)

