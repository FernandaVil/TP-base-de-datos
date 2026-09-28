# End-to-end data architecture: food delivery system

**How to manage transactional data, caching, and big data analytics in a single containerized environment?**

This collaboratively built project simulates the complete data infrastructure of a food delivery application. Through a Docker-orchestrated environment, we integrated relational databases for secure transactions, distributed processing for massive analytics, and NoSQL databases for real-time state management.

> 🇪🇸 [Versión en español](./README.es.md)
> 
> **Development team:** Developed alongside Richard Pavez and James Tuesta as part of the database systems curriculum for the data science degree (UBA).

## Architecture and technologies
To resolve the different bottlenecks of a high-traffic application, we divided the infrastructure into three layers:
* **Transactional layer (PostgreSQL):** Relational modeling and DDL scripts to guarantee the integrity of users, businesses, and payments.
* **Massive analytics layer (Apache Spark):** MapReduce implementation to process business metrics at scale without saturating the operational database.
* **Cache and state layer (Redis & MongoDB):** Migration of structured data to NoSQL documents and in-memory usage for millisecond responses on order status.

## Prerequisites
To guarantee end-to-end reproducibility, the infrastructure is completely containerized. You must have installed:
- Docker and Docker Compose
- An SQL client (such as pgAdmin or DBeaver)

## Execution instructions

### 1. Environment deployment
Open a terminal in the root of the project and run the following command to download the images and start the services:

    docker compose up -d

### 2. Relational database (stages 1 and 2)
The PostgreSQL container is configured to auto-initialize. When running the previous command, the DDL and bulk insertion scripts located in the `etapa_1_postgresql` folder are executed automatically. 
- The statistical validation and business logic queries are available in the `etapa_2_consultas_avanzadas/` folder.

### 3. Distributed processing with Apache Spark (stage 3)
The massive data analysis (MapReduce) runs inside an official container to avoid local Java dependencies.
1. Enter the web interface by navigating to: `http://localhost:8888`
2. Enter the access token (see credentials section).
3. Go to the `work/` folder and sequentially run the `mapreduce_spark.ipynb` file.

> **Technical note for source code review:** If you prefer to evaluate the Spark notebook natively in Visual Studio Code instead of using the browser, open the `.ipynb` file, select "Change kernel" -> "Existing Jupyter server" and enter the direct URL: `http://localhost:8888/?token=entregatp`

### 4. NoSQL databases (stage 4: MongoDB and Redis)
The execution files for this stage are located in the `etapa_4_nosql/` folder.
1. **Redis:** Run the dedicated Python script to initialize the in-memory structures and simulate reading or updating states.
2. **MongoDB:** Run the corresponding Python script to read the exported data from PostgreSQL, transform it, and populate the collections in the document database.

## Access and credentials
The services are exposed on the following local ports with their respective access credentials:

**PostgreSQL**
- Host name/address: `localhost`
- Port: `5432`
- Database: `delivery_db`
- User: `admin`
- Password: `password123`

**Apache Spark (Jupyter Lab)**
- Port: `8888`
- Token/Password: `entregatp`

**MongoDB and Redis (stage 4)**
- MongoDB: port `27017` (User: `admin` / Password: `password123`)
- Redis: port `6379` (No authentication)

## Maintenance operations
- To stop the containers without losing the generated information: `docker compose stop`
- To destroy the entire environment and clean the volumes: `docker compose down -v`
