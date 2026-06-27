import pandas as pd
import random
import re
from faker import Faker

fake = Faker('es_AR')

# Mismo diccionario y listas originales
categorias_posibles = ['pizzería', 'hamburguesería', 'sushi', 'comida sana', 'parrilla', 'heladería']
prefijos_genericos = ["Lo de", "La esquina de", "El rey de", "El bodegón de"]
prefijos_especificos = {
    'pizzería': ["Pizzería", "La mejor pizza de", "Pizzas"],
    'hamburguesería': ["Burger", "Hamburguesas"],
    'sushi': ["Sushi", "Izakaya"],
    'comida sana': ["Delivery veggie", "La huerta de"],
    'parrilla': ["Parrilla", "El asador de", "Carnes"],
    'heladería': ["Heladería", "Los helados de"]
}

menu_base = {
    'pizzería': [("Pizza Margarita", "Muzzarella, tomate fresco y albahaca", 8000), ("Fugazzetta Rellena", "Doble masa con extra queso y cebolla", 11000), ("Empanada de Carne", "Frita, cortada a cuchillo", 1500)],
    'hamburguesería': [("Doble Bacon Cheeseburger", "Dos medallones, cheddar, panceta y salsa", 9500), ("Hamburguesa Veggie", "Medallón de lentejas con lechuga y tomate", 8500), ("Papas Fritas con Cheddar", "Porción grande para compartir", 4500)],
    'sushi': [("Roll Salmon Avocado", "8 piezas con salmón rosado y palta", 12000), ("Nigiri de Salmón", "5 piezas de corte grueso", 9000), ("Gyozas de Cerdo", "Empanaditas al vapor y selladas", 6000)],
    'comida sana': [("Ensalada Caesar", "Pollo grillado, crutones, parmesano y aderezo", 7500), ("Wrap de Pollo", "Tortilla integral con vegetales frescos", 6500), ("Bowl de Quinoa", "Con palta, tomate cherry y huevo poché", 8000)],
    'parrilla': [("Ojo de Bife", "Corte premium de 400gr punto a elección", 18000), ("Choripán Clásico", "Puro cerdo con chimichurri casero", 4000), ("Provoleta", "Fundida con orégano y ají molido", 6500)],
    'heladería': [("Cuarto de Helado", "Hasta 3 sabores a elección", 4500), ("Kilo de Helado", "Hasta 4 sabores a elección", 14000), ("Cucurucho Bañado", "Doble bocha con baño de chocolate", 3500)]
}

def limpiar_texto(texto):
    return re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]", "", texto).strip()

# 2. Listas para guardar los datos
restaurantes_extras = []
platos_extras = []

# IMPORTANTE: Arrancamos el ID de platos en 1000 para evitar colisiones con tu BD original
id_plato_global = 1000 

print("Generando 50 restaurantes extra...")

# IMPORTANTE: Iteramos del 51 al 100
for i in range(51, 101):
    cat = random.choice(categorias_posibles)
    if random.random() > 0.5:
        prefijo = random.choice(prefijos_genericos)
    else:
        prefijo = random.choice(prefijos_especificos[cat])
    
    nombre_limpio = limpiar_texto(f"{prefijo} {fake.last_name()}")
    
    # guardamos el restaurante con el esquema exacto de PostgreSQL
    restaurantes_extras.append({
        'id_restaurante': i,
        'nombre': nombre_limpio,
        'id_direccion': random.randint(1, 4000), # asignación aleatoria a una dirección existente
        'categoria': cat
    })
    
    # Generamos los platos para este restaurante
    opciones_platos = menu_base.get(cat, menu_base['hamburguesería'])
    for nombre_plato, desc, precio in opciones_platos:
        precio_final = precio + random.choice([-500, 0, 500, 1000])
        if precio_final <= 0: 
            precio_final = precio
            
        # guardamos el plato con el esquema exacto
        platos_extras.append({
            'id_plato': id_plato_global,
            'id_restaurante': i,
            'nombre': limpiar_texto(nombre_plato),
            'descripcion': limpiar_texto(desc),
            'precio_actual': precio_final,
            'esta_disponible': True
        })
        id_plato_global += 1

# 3. Exportamos a CSV
df_restaurantes = pd.DataFrame(restaurantes_extras)
df_platos = pd.DataFrame(platos_extras)

df_restaurantes.to_csv('restaurantes_extras.csv', index=False)
df_platos.to_csv('platos_extras.csv', index=False)

print("¡Listo! Archivos 'restaurantes_extras.csv' y 'platos_extras.csv' generados con éxito.")