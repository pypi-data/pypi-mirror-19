# FLask-Stormpath-Plus

## What is the differencies between plus and original version

- add a sha256 hashing to the password before sending to stormpath server.

## Below content is same with flask stormpath
Build simple, secure web applications with Stormpath and Flask!


## Documentation

You can find this project's documentation on ReadTheDocs:
http://flask-stormpath.readthedocs.org/en/latest/


## Sample Application

If you'd like to hop directly into some code, we've built a sample application,
which demonstrates how Flask-Stormpath-Plus can be used to build a very simple
user-facing website with user registration, login, dashboard, etc.

You can find the project on GitHub here:
https://github.com/stormpath/stormpath-flask-sample

This application provides a simple local web server that allows you to create
users, log them in, log them out, etc.

You can use this as a reference for implementing `Flask-Stormpath-Plus` into your
Flask projects.


## Backend

This library is largely based on the excellent
[Flask-Login](http://flask-login.readthedocs.org/en/latest/) library.  Most
functionality is piggybacked off this library, including secure user sessions /
etc.

Right now we're rapidly developing this library to make it easy for Flask
developers to add user authentication to their projects without the complication
that comes along with it.

If you have features or suggestions, please let me know!

