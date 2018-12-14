# How to use docker to spin up WebSiteOne

## Prerequisites

In order to run this container you'll need docker installation
* [Windows](https://docs.docker.com/docker-for-windows/)
* [OS X](https://docs.docker.com/docker-for-mac/)
* [Linux](https://docs.docker.com/linux/started/)

## Setup the project
Follow the instruction at [Project README.md](../README.md) to set up the configs for the project

## Start docker

Start the application

```bash
$ ./docker/start.sh
```

## Stop docker

Stop the application

```bash
$ ./docker/stop.sh
```

## Seed Database

To add seed data to the database, run the commands below

```bash
$ ./docker/seed.sh
$ ./docker/start.sh
```
The application should start with the database containing the seed data

## Tests inside docker container

TODO

ps: those docker commands were tested under the following environment:

- MacOS 10.13.6
    - Docker version 18.06.0-ce, build 0ffa825
    - docker-compose version 1.22.0, build f46880f


If it doesn't work for you, try to check your docker version and consider upgrading it if you have an older version.
