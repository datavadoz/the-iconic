# The ICONIC challenge

## Overview
This is the challange project from **The ICONIC**. The main functionality of this project is to perform 2 data workflows:

- Ingest test_data.zip into database (Postgres).
- Perform business queries and send a report email every day.

![](images/architecture.png)

## Prerequisite
Docker with compose plugin (current version: 20.10.17).

## Instruction
To build the system:
```
docker compose build
```

To bring the system up:
```
docker compose up -d
```

**Note**: If the system starts at the first time, the database has nothing. So, we need to create tables and insert some initial records. To do that, refer to the below instructions:

1. Open PgAdmin with URL `http://localhost:8000/` and login with username `danhvo.uit@gmail.com` and password `root`.
2. Register a new server in PgAdmin with following configurations:
![](images/regisger_server_1.jpg)
![](images/regisger_server_2.jpg)
3. Access to **the-iconic** database and perform all `*.sql` files in `src/iconic/model/migrate` path.
4. Insert the Google Mail credential:
```
INSERT INTO resource (resource_name, resource_password)
VALUES ('your_email@gmail.com', 'your_email_app_password')
```
5. Access Prefect Deployment UI: `http://localhost:4200/deployments` and perform quick run the `ingest-zip-to-pg/ingest_test_data` deloyment to download and ingest [test_data.zip](https://github.com/theiconic/technical-challenges/raw/master/data/sample-data/test_data.zip) to Postgres database:
![](images/deployment_1.jpg)
6. After the `ingest-zip-to-pg/ingest_test_data` workflow finish, we perform quick run the `report/daily_report` deployment also to query and send report email. The email should look like as below:
![](images/email_1.jpg)
7. All things are in shape now!
