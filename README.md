# Fun Pokedex Api

> This project was developed to offer a new perspective at the world of Pokemon.

## Table of Contents
- [Fun Pokedex Api](#fun-pokedex-api)
    - [Table of Contents](#table-of-contents)
    - [Package and Run](#package-and-run)
        - [Package and Run via Docker Image](#package-and-run-via-docker-image)
          - [Running the application using Docker Image](#running-the-application-using-docker-image)
          - [Build and Publish new Docker Image](#build-and-publish-new-docker-image)
        - [Running the application in dev mode](#running-the-application-in-dev-mode)
        - [Packaging and running the application](#packaging-and-running-the-application)
    - [Usage](#usage)
      - [Swagger-UI and OpenAPI](#swagger-ui-and-openapi)
    - [Requirements to start the program](#requirements-to-start-the-program)
    - [Needed before production deploy](#needed-before-production-deploy)



## Package and Run

### Package and Run via Docker Image
Required: ***Docker must be installed***

#### Running the application using Docker Image

You can run the application using the docker image in my public repository:
```shell script
docker run -i --rm -p 8080:8080 public.ecr.aws/d8b6h6u8/federicogualdi/pokedex:latest
```
_if there is already the ':latest' image in the local docker registry, remember to delete it to make sure you start the latest version of the project_
```shell script
docker rmi public.ecr.aws/d8b6h6u8/federicogualdi/pokedex:latest
```

#### Build and Publish new Docker Image

If you fork this project, you can use my script to simplify the build and publishing tasks.
```shell script
sh build-and-copy.sh $AWS_PROFILE $AWS_ECR_URL $DOCKER_TAG
```

### Running the application in dev mode

After clone the repository You can run application in dev mode, that also enables live coding, using:
```shell script
./mvnw compile quarkus:dev
```

### Packaging and running the application

The application can be packaged using:
```shell script
./mvnw package -Dquarkus.package.type=uber-jar
```
The application, packaged as a _über-jar_, is now runnable using `java -jar target/*-runner.jar`.



## Usage
While the project is running _(follow the relevant section in this file)_ two endpoints are available.

**GET** pokemon with the property required by the project:

    http://localhost:8080/api/v1/pokemon/<POKEMON_NAME>

**GET** pokemon with the property required by the project and a funny description:

    http://localhost:8080/api/v1/pokemon/translated/<POKEMON_NAME>


### Swagger-UI and OpenAPI
Swagger-UI is available for testing project endpoints, just go to:

    http://localhost:8080/q/swagger-ui

You can also download OpenAPI endpoints specification in json format:

    http://localhost:8080/q/openapi



## Requirements to start the program

If you want to use Docker and you haven't installed it yet, just go to:
https://docs.docker.com/get-docker/

If you want to build and run the project, and you haven't installed java yet, just go to:
https://www.java.com/en/download/help/download_options.html



## Needed before production deploy

Before a production implementation there are a few things to set up.
First, it is necessary to understand how many requests per second we expect,
based on that we can proceed differently.

- Improve Code Performance

If we want to increase the maximum number of concurrent requests, 
we need to refactor PokedexRest to handle the blocking request for event-loops thread.

- Horizontal Scaling

If we want to run multiple instances of 'Pokedex Api' to serve more users -
with the same code base - it will be sufficient to deploy several instances
of 'Pokedex Api' backed by LoadBalancer that will dispatch requests 
among all instances.
NB: this solution preclude local-cache and requires the use of a distributed-cache 
such as Redis. 

- Add Metrics

Add metrics to analyze execution-time and call-occurrences to track most expensive methods

- Add logs you need

Add logs you need to track program execution and detect new bugs.

- Map all known Exceptions

Add mapper for known useful Exception to improve business logic.

- Swagger-UI and OpenAPI

If the project will not be public, it will be necessary to remove Swagger-UI and OpenAPI
from distribution in production.