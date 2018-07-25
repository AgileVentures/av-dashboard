# av-dashboard
An internal dashboard for Agile Ventures analytics

## installation

```
$ pip3 install -r requirements.txt
$ pip3 install -e .
```

## testing

```
$ aloe
```

##development environment

To easily see the dashboard in development mode, you have to set flask to be in development mode by doing

```
$ export FLASK_ENV=development
```

on the command line before running flask run.  Or in windows run this before:

```
$ set FLASK_ENV=development
```

Note however that if you run this command and then run aloe tests they will fail as your app will still be
in development mode and bypassing the authentication procedures which are under test.  To go back to a production mode, run:

```
$ export FLASK_ENV=production
```

or the windows equivalent and then the tests should pass again.
