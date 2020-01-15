# SmartImageRepository
### prerequisites
1. Docker and docker compose needs to be installed, since everything will be running in docker containers. 
2. Port 8888, 8889, 5432 and 8501 need to be available on the host machine.

### steps to start the app:
 1. Download the state dict of the object detector model of this app from [here](https://drive.google.com/open?id=1UPuvEI1SeugSpjLo5ZZwVqjSuju87pD6), then put it in `TagGeneratorService/model` directory, 
 2. Download the MSCOCO dataset's annotation from [here](https://drive.google.com/open?id=1P__hYzIrKXFiLV1YjZC40CRo28dALc_r), and put it in `data` directory. 
 3. Start the app by running `docker-compose up`, it might take a moment to build.
 4. If this is the first time the app be being built, to populate the database, run the following:
    ```
        docker build -f Dockerfile.populate -t populatedb .
        docker run --network host populatedb
    ```
    fail to do so will result the database being empty. It will take a few minutes to add all entries from MSCOCO dataset's validation set into the database.
 5. Access the app here: http://localhost:8501
 
### how does the app works:
This app is consist of three microservices, search service, tag service and web app.
Postgres database is used for storage. Everything is containerized and can be bought up
 by running `docker-compose up`. 
 
 The web app accepts 
 
 The Tag Service
 
 The Search Service