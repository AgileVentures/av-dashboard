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

## Tests inside docker container

TODO

ps: those docker commands were tested under the following environment:

- MacOS 10.13.6
    - Docker version 18.06.0-ce, build 0ffa825
    - docker-compose version 1.22.0, build f46880f

- Linux Manjaro 17.1.12
    - Docker version 18.06.1-ce, build e68fc7a215
    - docker-compose version 1.22.0


If it doesn't work for you, try to check your docker version and consider upgrading it if you have an older version.
