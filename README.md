# Fun Pokedex Api

This project was developed to offer a new perspective at the world of Pokemon.


## Package and Run via Docker Image  ***(Docker must be installed)***

### Running the application using Docker Image

You can run the application using the docker image in my public repository:
```shell script
docker run -i --rm -p 8080:8080 public.ecr.aws/d8b6h6u8/federicogualdi/pokedex:latest
```

### Build and Publish new Docker Image

If you fork this project, you can use my script to simplify the build and publishing tasks.
```shell script
sh build-and-copy.sh $AWS_PROFILE $AWS_ECR_URL $DOCKER_TAG
```


## Running the application in dev mode

You can run application in dev mode that enables live coding using:
```shell script
./mvnw compile quarkus:dev
```


## Packaging and running the application

The application can be packaged using:
```shell script
./mvnw package -Dquarkus.package.type=uber-jar
```
The application, packaged as an _über-jar_, is now runnable using `java -jar target/*-runner.jar`.