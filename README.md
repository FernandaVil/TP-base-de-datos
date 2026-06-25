# Trabajo práctico: sistema de pedidos de comida online

Este repositorio contiene la resolución del trabajo práctico grupal sobre un sistema de pedidos de comida online, abarcando desde el modelado relacional transaccional hasta el procesamiento distribuido de datos masivos.

## Requisitos previos

Para garantizar la reproducibilidad de punta a punta, la infraestructura se encuentra completamente contenida. Se requiere tener instalado:
* Docker y Docker Compose
* Un cliente SQL (como pgAdmin o DBeaver)

## Instrucciones de ejecución

### 1. Despliegue del entorno
Abrir una terminal en la raíz del proyecto y ejecutar el siguiente comando para descargar las imágenes e iniciar los servicios:

    docker compose up -d

### 2. Base de datos relacional (etapas 1 y 2)
El contenedor de PostgreSQL está configurado para auto-inicializarse. Al ejecutar el comando anterior, los scripts DDL y de inserción masiva ubicados en la carpeta etapa_1_postgresql se ejecutan automáticamente. 
* Las consultas de validación estadística y lógica de negocio se encuentran disponibles en la carpeta etapa_2_consultas_avanzadas/.

### 3. Procesamiento distribuido con Apache Spark (etapa 3)
El análisis masivo de datos (MapReduce) se ejecuta dentro de un contenedor oficial para evitar dependencias locales de Java.
1. Ingresar a la interfaz web navegando a: http://localhost:8888
2. Introducir el token de acceso (ver sección de credenciales).
3. Dirigirse a la carpeta work/ y ejecutar secuencialmente el archivo mapreduce_spark.ipynb.

## Accesos y credenciales

Los servicios están expuestos en los siguientes puertos locales con sus respectivas credenciales de acceso:

**PostgreSQL**
* Host name/address: localhost
* Puerto: 5432
* Base de datos: delivery_db
* Usuario: admin
* Contraseña: password123

**Apache Spark (Jupyter Lab)**
* Puerto: 8888
* Token/Contraseña: entregatp

**MongoDB y Redis (etapa 4)**
* MongoDB: puerto 27017 (Usuario: admin / Contraseña: password123)
* Redis: puerto 6379 (Sin autenticación)

## Operaciones de mantenimiento
* Para detener los contenedores sin perder la información generada: docker compose stop
* Para destruir el entorno completo y limpiar los volúmenes: docker compose down -v

---
**Nota técnica para revisión del código fuente**
Si se prefiere evaluar el notebook de Spark nativamente en Visual Studio Code en lugar de utilizar el navegador, se debe abrir el archivo .ipynb, seleccionar "Cambiar kernel" -> "Servidor Jupyter existente" e ingresar la URL directa: http://localhost:8888/?token=entregatp
