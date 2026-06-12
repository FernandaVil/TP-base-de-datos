# Trabajo práctico de introducción a bases de datos

Este repositorio contiene la resolución del trabajo práctico grupal sobre un sistema de pedidos de comida online.

## Requisitos previos

Para poder ejecutar este proyecto, es necesario tener instalado Docker y Docker Compose en el equipo.

## Instrucciones para levantar el entorno

1. Clonar este repositorio en la computadora local.
2. Abrir una terminal en la raíz del proyecto.
3. Ejecutar el siguiente comando para descargar las imágenes e iniciar las bases de datos:

   docker compose up -d

4. Los servicios estarán disponibles en los siguientes puertos locales:
   - PostgreSQL: 5432
   - MongoDB: 27017
   - Redis: 6379

Para detener los contenedores sin borrar los datos, utilizar el comando `docker compose stop`. Para destruir el entorno completo, utilizar `docker compose down -v`.