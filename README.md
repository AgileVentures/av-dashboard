# av-dashboard    [![Build Status](https://travis-ci.org/AgileVentures/av-dashboard.svg?branch=master)](https://travis-ci.org/AgileVentures/av-dashboard)
An internal dashboard for Agile Ventures analytics

## installation

```
$ pip3 install -r requirements.txt
$ pip3 install -e .
```

## database setup

You will need to configure the database connection in several files before you can proceed.
First, copy alembic.ini.example as so:

```
cp alembic.ini.example alembic.ini
```

Then you should edit the part of the file that says:-

```
[test_db]
sqlalchemy.url = postgresql://postgres:pw@localhost:5432/av_dashboard_test
[dev_db]
sqlalchemy.url = postgresql://postgres:pw@localhost:5432/av_dashboard_dev
[ci_db]
sqlalchemy.url = postgresql://postgres@localhost/av_dashboard_test
```

In the newly copied file, you will want to insert the corresponding password for your database where it has 'pw', and the user where it has 'postgres'.
In the event that your local database is on a different host or port, feel free to change 'localhost:5432'.

Next, you will need to copy the config.py.example file that is in the instance folder:

```
cp instance/config.py.example instance/config.py
```

In the newly copied file, you will want to edit the file:

```
POSTGRES_USER = 'user'
POSTGRES_PASSWORD = 'password'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
```

Insert the corresponding user, password and possibly host and port for your local database.

Next, copy the test.py.example and dev.py.example in the config folder as so:

```
cp config/test.py.example config/test.py
cp config/dev.py.example
```

In most cases, you can just leave these files as they are, but in case you want a special name for your test or dev database, edit it appropriately.  But if you do
edit this default, also edit in the alembic.ini above.

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

To see the dashboard in development mode, you will need to have done the database setup and then run the command to seed the database:

```
$ ./seed_database.sh
```

And then run the tests:

```
$ ./run_server.sh
```

And navigate to the url displayed on the output.
