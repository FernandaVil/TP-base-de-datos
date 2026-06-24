import random
import unicodedata
from faker import Faker
from datetime import timedelta
import os

# usamos la localización argentina
fake = Faker('es_AR')

# volúmenes de datos (ajustados para calidad)
NUM_USUARIOS = 1000
NUM_RESTAURANTES = 50
NUM_REPARTIDORES = 200
NUM_PROMOCIONES = 20
NUM_PEDIDOS = 5000

def limpiar_texto(texto):
    return str(texto).replace("'", "''").replace("\n", " ")

def normalizar_email(texto):
    """quita tildes y espacios para armar emails reales"""
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.lower().replace(" ", ".")

print("generando datos de alta consistencia en memoria...")

# 1. usuarios y sus fechas de registro (guardadas para validación cronológica)
usuarios = []
fechas_registro_usuarios = {}
for i in range(1, NUM_USUARIOS + 1):
    nombre = fake.first_name()
    apellido = fake.last_name()
    nombre_completo = f"{nombre} {apellido}"
    email = f"{normalizar_email(nombre_completo)}{i}@gmail.com"
    # limitamos las fechas de registro para que sean previas a la creación de pedidos
    fecha_reg = fake.date_between(start_date='-2y', end_date='-7m')
    fechas_registro_usuarios[i] = fecha_reg
    usuarios.append(f"({i}, '{limpiar_texto(nombre_completo)}', '{email}', '{fake.phone_number()}', '{fecha_reg}')")

# 2. catálogo estricto de calles (normalización de direcciones)
calles_caba = ["Av. Corrientes", "Av. Rivadavia", "Av. Santa Fe", "Av. Cabildo", "Av. Callao", "Gurruchaga", "Thames", "Honduras"]
calles_inserts = []
for idx, nombre_calle in enumerate(calles_caba, 1):
    calles_inserts.append(f"({idx}, '{nombre_calle}')")
id_direccion_global = 1
direcciones_inserts = []
restaurantes = []

# creamos el diccionario de memoria: la clave será (id_calle, altura) y el valor será el id_direccion
memoria_direcciones = {}

def obtener_o_crear_direccion(id_calle, altura):
    global id_direccion_global
    tupla_ubicacion = (id_calle, altura)
    
    # si la dirección ya existe en memoria, reutilizamos su ID
    if tupla_ubicacion in memoria_direcciones:
        return memoria_direcciones[tupla_ubicacion]
    
    # si es nueva, la guardamos, la agregamos a los inserts y avanzamos el contador
    memoria_direcciones[tupla_ubicacion] = id_direccion_global
    direcciones_inserts.append(f"({id_direccion_global}, {id_calle}, {altura})")
    id_asignado = id_direccion_global
    id_direccion_global += 1
    return id_asignado

# 3. restaurantes (nombres fijos y asignación de dirección normalizada)
nombres_restaurantes = [
    ("La Mezzetta", "pizzería"), ("Guerrín", "pizzería"), ("El Cuartito", "pizzería"), ("Kentucky", "pizzería"),
    ("Burger Joint", "hamburguesería"), ("The Food Truck Store", "hamburguesería"), ("Pérez H", "hamburguesería"),
    ("Sushi Club", "sushi"), ("Fabric Sushi", "sushi"), ("Dashi", "sushi"),
    ("Sacro", "comida sana"), ("Artemisia", "comida sana"), ("El Club de la Milanesa", "parrilla"),
    ("Don Julio", "parrilla"), ("La Cabrera", "parrilla"), ("Rapa Nui", "heladería"), ("Lucciano's", "heladería")
]

prefijos_genericos = ["Lo de", "La esquina de", "El rey de", "El bodegón de"]
prefijos_especificos = {
    'pizzería': ["Pizzería", "La mejor pizza de", "Pizzas"],
    'hamburguesería': ["Burger", "Hamburguesas"],
    'sushi': ["Sushi", "Izakaya"],
    'comida sana': ["Delivery veggie", "La huerta de"],
    'parrilla': ["Parrilla", "El asador de", "Carnes"],
    'heladería': ["Heladería", "Los helados de"]
}

categorias_posibles = ['pizzería', 'hamburguesería', 'sushi', 'comida sana', 'parrilla', 'heladería']

while len(nombres_restaurantes) < NUM_RESTAURANTES:
    cat = random.choice(categorias_posibles)
    if random.random() > 0.5:
        prefijo = random.choice(prefijos_genericos)
    else:
        prefijo = random.choice(prefijos_especificos[cat])
    nombres_restaurantes.append((f"{prefijo} {fake.last_name()}", cat))

direcciones_inserts = []
restaurantes = []

for i in range(1, NUM_RESTAURANTES + 1):
    nombre, categoria = nombres_restaurantes[i-1]
    id_calle = random.randint(1, len(calles_caba))
    altura = random.randint(100, 4500)
    
    # usamos la memoria para obtener el ID (nuevo o reciclado)
    id_direccion_actual = obtener_o_crear_direccion(id_calle, altura)
    
    restaurantes.append(f"({i}, '{limpiar_texto(nombre)}', {id_direccion_actual}, '{categoria}')")

# 4. repartidores
repartidores = []
for i in range(1, NUM_REPARTIDORES + 1):
    nombre_completo = f"{fake.first_name()} {fake.last_name()}"
    repartidores.append(f"({i}, '{limpiar_texto(nombre_completo)}', '{fake.phone_number()}', '{random.choice(['moto', 'bicicleta'])}', true)")

# 5. promociones y sus rangos de vigencia (guardados para validación temporal estática)
promociones = []
intervalos_promociones = {}
desc_porcentajes = {}
porcentajes_validos = [10, 15, 20, 25, 30, 40, 50]
for i in range(1, NUM_PROMOCIONES + 1):
    inicio = fake.date_time_between(start_date='-8m', end_date='now')
    fin = inicio + timedelta(days=random.randint(30, 90))
    descuento = random.choice(porcentajes_validos)
    desc_porcentajes[i] = descuento
    intervalos_promociones[i] = (inicio, fin)
    promociones.append(f"({i}, 'PROMO{descuento}OFF_{i}', {descuento}, '{inicio}', '{fin}', {random.randint(50, 1000)})")

# 6. platos (diccionario temático)
menu_base = {
    'pizzería': [("Pizza Margarita", "Muzzarella, tomate fresco y albahaca", 8000), ("Fugazzetta Rellena", "Doble masa con extra queso y cebolla", 11000), ("Empanada de Carne", "Frita, cortada a cuchillo", 1500)],
    'hamburguesería': [("Doble Bacon Cheeseburger", "Dos medallones, cheddar, panceta y salsa", 9500), ("Hamburguesa Veggie", "Medallón de lentejas con lechuga y tomate", 8500), ("Papas Fritas con Cheddar", "Porción grande para compartir", 4500)],
    'sushi': [("Roll Salmon Avocado", "8 piezas con salmón rosado y palta", 12000), ("Nigiri de Salmón", "5 piezas de corte grueso", 9000), ("Gyozas de Cerdo", "Empanaditas al vapor y selladas", 6000)],
    'comida sana': [("Ensalada Caesar", "Pollo grillado, crutones, parmesano y aderezo", 7500), ("Wrap de Pollo", "Tortilla integral con vegetales frescos", 6500), ("Bowl de Quinoa", "Con palta, tomate cherry y huevo poché", 8000)],
    'parrilla': [("Ojo de Bife", "Corte premium de 400gr punto a elección", 18000), ("Choripán Clásico", "Puro cerdo con chimichurri casero", 4000), ("Provoleta", "Fundida con orégano y ají molido", 6500)],
    'heladería': [("Cuarto de Helado", "Hasta 3 sabores a elección", 4500), ("Kilo de Helado", "Hasta 4 sabores a elección", 14000), ("Cucurucho Bañado", "Doble bocha con baño de chocolate", 3500)]
}

platos = []
platos_por_restaurante = {r: [] for r in range(1, NUM_RESTAURANTES + 1)}
precio_por_plato = {}
id_plato_global = 1

for i in range(1, NUM_RESTAURANTES + 1):
    categoria = nombres_restaurantes[i-1][1]
    opciones = menu_base.get(categoria, menu_base['hamburguesería'])
    for nombre_plato, desc, precio in opciones:
        precio_final = precio + random.choice([-500, 0, 500, 1000])
        if precio_final <= 0: precio_final = precio
        platos_por_restaurante[i].append(id_plato_global)
        precio_por_plato[id_plato_global] = precio_final
        platos.append(f"({id_plato_global}, {i}, '{limpiar_texto(nombre_plato)}', '{limpiar_texto(desc)}', {precio_final}, true)")
        id_plato_global += 1

# 7. procesamiento de pedidos con validación de consistencia estática estricta
pedidos = []
detalles = []
historiales = []
id_historial_global = 1

for id_pedido in range(1, NUM_PEDIDOS + 1):
    id_usuario = random.randint(1, NUM_USUARIOS)
    id_restaurante = random.choice([r for r, p in platos_por_restaurante.items() if len(p) > 0])
    
    # restricción: la fecha de creación debe ser posterior a la fecha de registro del usuario
    fecha_minima_usuario = fechas_registro_usuarios[id_usuario]
    
    # 1. TRAMPA CORREGIDA: Decidimos PRIMERO si va a usar promo (ej. 25% de probabilidad)
    usar_promo = random.random() < 0.25
    id_promocion = 'NULL'
    fecha_creacion = None

    if usar_promo and intervalos_promociones:
        # Elegimos una promoción cualquiera al azar de nuestro catálogo
        id_promo_elegida, (ini, fin) = random.choice(list(intervalos_promociones.items()))
        
        # --- CORRECCIÓN A PRUEBA DE BALAS ---
        # Si la variable tiene hora, la limpiamos. Si ya es fecha pura, la dejamos igual.
        f_min = fecha_minima_usuario.date() if hasattr(fecha_minima_usuario, 'date') else fecha_minima_usuario
        f_ini = ini.date() if hasattr(ini, 'date') else ini
        f_fin = fin.date() if hasattr(fin, 'date') else fin
        
        # Ahora sí, ambas hablan el mismo idioma
        fecha_inicio_valida = max(f_min, f_ini)
        
        if fecha_inicio_valida <= f_fin:
            # FORZAMOS la fecha para que caiga dentro de la promo
            fecha_creacion = fake.date_time_between(start_date=fecha_inicio_valida, end_date=f_fin)
            id_promocion = id_promo_elegida
            
    # 2. Si no usó promo (o por mala suerte eligió una promo antiquísima para un usuario nuevo)
    if fecha_creacion is None:
        fecha_creacion = fake.date_time_between(start_date=fecha_minima_usuario, end_date='now')
        id_promocion = 'NULL'
    # restricción logística: si el pedido finaliza entregado, debe poseer repartidor asignado
    # asignamos estado inicial para determinar el alcance logístico del flujo
    es_pedido_reciente = random.random() < 0.10
    if es_pedido_reciente:
        id_repartidor = 'NULL'
    else:
        id_repartidor = random.randint(1, NUM_REPARTIDORES)

    # generación de la dirección de entrega usando la memoria
    id_calle_entrega = random.randint(1, len(calles_caba))
    altura_entrega = random.randint(100, 4500)
    
    id_direccion_actual_entrega = obtener_o_crear_direccion(id_calle_entrega, altura_entrega)
    
    # restricción del catálogo: platos elegidos pertenecen estrictamente al restaurante del pedido
    cantidad_items = random.randint(1, 3)
    platos_elegidos = random.sample(platos_por_restaurante[id_restaurante], min(cantidad_items, len(platos_por_restaurante[id_restaurante])))
    
    subtotal = 0
    for id_plato in platos_elegidos:
        cantidad = random.randint(1, 4)
        precio_hist = precio_por_plato[id_plato]
        subtotal += (cantidad * precio_hist)
        detalles.append(f"({id_pedido}, {id_plato}, {cantidad}, {precio_hist})")
        
    # restricción financiera: cálculo exacto aplicando descuentos vigentes
    total_abonado = subtotal
    if id_promocion != 'NULL':
        total_abonado = subtotal * (1 - (desc_porcentajes[id_promocion] / 100.0))
    
    pedidos.append(f"({id_pedido}, {id_usuario}, {id_restaurante}, {id_repartidor}, {id_promocion}, '{fecha_creacion}', {round(total_abonado, 2)}, {id_direccion_actual_entrega})")
    
    # restricción de la máquina de estados: transiciones cronológicas y lógicas sin duplicados
    historiales.append(f"({id_historial_global}, {id_pedido}, 'creado', '{fecha_creacion}')")
    id_historial_global += 1
    
    if id_repartidor == 'NULL':
        # flujos indeterminados o cancelaciones prematuras desde la preparación
        if random.random() > 0.4:
            fecha_prep = fecha_creacion + timedelta(minutes=random.randint(2, 6))
            historiales.append(f"({id_historial_global}, {id_pedido}, 'en_preparacion', '{fecha_prep}')")
            id_historial_global += 1
            if random.random() > 0.8: # simulación menor de cancelaciones
                fecha_canc = fecha_prep + timedelta(minutes=random.randint(5, 10))
                historiales.append(f"({id_historial_global}, {id_pedido}, 'cancelado', '{fecha_canc}')")
                id_historial_global += 1
    else:
        # transiciones lógicas completas para pedidos despachados con repartidor
        fecha_prep = fecha_creacion + timedelta(minutes=random.randint(3, 10))
        historiales.append(f"({id_historial_global}, {id_pedido}, 'en_preparacion', '{fecha_prep}')")
        id_historial_global += 1
        
        fecha_camino = fecha_prep + timedelta(minutes=random.randint(8, 15))
        historiales.append(f"({id_historial_global}, {id_pedido}, 'en_camino', '{fecha_camino}')")
        id_historial_global += 1
        
        if random.random() > 0.05:
            fecha_entregado = fecha_camino + timedelta(minutes=random.randint(10, 25))
            historiales.append(f"({id_historial_global}, {id_pedido}, 'entregado', '{fecha_entregado}')")
            id_historial_global += 1
        else:
            fecha_canc = fecha_camino + timedelta(minutes=random.randint(5, 15))
            historiales.append(f"({id_historial_global}, {id_pedido}, 'cancelado', '{fecha_canc}')")
            id_historial_global += 1

# guardado estructurado en el script sql destino
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(directorio_actual, 'etapa_1_postgresql', '2_insercion_datos.sql')

with open(ruta_archivo, 'w', encoding='utf-8') as f:
    f.write("BEGIN;\n\n")
    
    def escribir_inserts(tabla, columnas, lista_valores):
        if not lista_valores: return
        f.write(f"INSERT INTO {tabla} ({columnas}) VALUES \n")
        f.write(",\n".join(lista_valores))
        f.write(";\n\n")

    escribir_inserts('usuario', 'id_usuario, nombre, email, telefono, fecha_registro', usuarios)
    escribir_inserts('calle', 'id_calle, nombre', calles_inserts)
    escribir_inserts('direccion', 'id_direccion, id_calle, altura', direcciones_inserts)
    escribir_inserts('restaurante', 'id_restaurante, nombre, id_direccion, categoria', restaurantes)
    escribir_inserts('repartidor', 'id_repartidor, nombre, telefono, vehiculo, esta_activo', repartidores)
    escribir_inserts('promocion', 'id_promocion, codigo, porcentaje_descuento, fecha_inicio, fecha_fin, stock_usos', promociones)
    escribir_inserts('plato', 'id_plato, id_restaurante, nombre, descripcion, precio_actual, esta_disponible', platos)
    escribir_inserts('pedido', 'id_pedido, id_usuario, id_restaurante, id_repartidor, id_promocion, fecha_hora_creacion, total_abonado, id_direccion_entrega', pedidos)
    escribir_inserts('detalle_pedido', 'id_pedido, id_plato, cantidad, precio_unitario_historico', detalles)
    f.write("ALTER TABLE historial_estado_pedido DISABLE TRIGGER ALL;\n")
    escribir_inserts('historial_estado_pedido', 'id_historial, id_pedido, estado, fecha_hora', historiales)
    f.write("ALTER TABLE historial_estado_pedido ENABLE TRIGGER ALL;\n")
    
    f.write("COMMIT;\n")

print("¡archivo 2_insercion_datos.sql generado con integridad absoluta!")