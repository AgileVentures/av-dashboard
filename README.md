# av-dashboard    [![Build Status](https://travis-ci.org/AgileVentures/av-dashboard.svg?branch=master)](https://travis-ci.org/AgileVentures/av-dashboard)
An internal dashboard for Agile Ventures analytics

## installation

```
$ pip3 install -r requirements.txt
$ pip3 install -e .
```

## database setup

//put configuration file editing description here

After you have setup the database configurations above, create the databases like so with your postgresql server already running:-

```
$ ./create_database.sh
```

Next, migrate the test and dev databases like so:

```
$ ./migrate_databases.sh
```

## testing
Run

```
$ ./run_tests.sh
```
## development environment

To see the dashboard in development mode, you will need to have done the database setup and then run

```
$ ./run_server.sh
```

And navigate to the url displayed on the output.
