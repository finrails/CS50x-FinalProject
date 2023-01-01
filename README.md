# Tasky
#### Video Demo:  <URL HERE>
#### Description:
Tasky is a lightweight, fast response to-do list which you can run in your machine without headches.

The Tasky has been implemented using Python, HTML, CSS, Flask, SQL, sqlite3, SQLAlchemy and Flask-SQLAlchemy. Task has a good multi-user system, where you can create various accounts, and each account has different access to different data; the system also has a auth system that hash the user password, so if a hacker gain control over your system, the system's password are hashed, so the hacker will never know the users passwords.

Tasky also has a very small permission system, what it means? It means that if a User try to, for example, change the HTML form tag action to delete some other user data, it will be handled and rejected by the Flask app, the same occurs for the edit, do and undo features.

The auth system just prevents that a user access data owned by some other user, so it is the angular stone of Tasky.

Also Tasky has the basic four CRUD operations, (C)reate, (R)ead, (U)pdate, (D)elete. So you can create a new task, after some time you can edit it if you goal change, then you can just delete it if you feel tired, or, in the best scenario, you can just do it; if you regret, just undo it and edit after that.

Tasky also is a responsive app, which means that it will adapt to you device, so, if you have a tablet, you don't need to worry about it, the Tasky will adapt to you device; if you have a smartphone, the same will happens.

Tasky uses sqlite to store the users data, it is stored in /tmp directory, because it has been made to be simple and adaptative.

To communicate with the database i've choose to use the SQLAlchemy with a Wrapper(Flask-SQLAlchemy). Basically the SQLAlchemy is a ORM(Object Relational Mapper), it means that we can map Python objects to SQL real tables, the SQLAlchemy uses the Python sqlite3 DBAPI to communicate with the database, the main goal of SQLAlchemy is to generate queries(e.g. select * from table) using these python objects, the hardwork is the DBAPI who do, SQLAlchemy just generate the queries to it(which is very good).

Oh, we're using Flask, so it uses Jinja2 to generate our HTML. Jinja2 is a template engine, it basically generates our HTML dynamically. Yes, it is it, a program that we ask for a HTML page, and it cast it to us.

Oh i almost forgot, i also programmed some flash messages. flash is a session that persists among user requests, and can be fetched just one time, after that we can't acess it again, it is really good to render flash messages.

Ok, lets describe some files:

- app.py: The file where all things happens, it is the angular stone, it call jinja2 to generate HTML, check for permission, do redirects, call for models, call for sqlalchemy to make query, and cast it to WSGI.

- models.py: where the sqlalchemy models live in, a model is just a Python object mapped to a table in the database, the sqlalchemy handle the hardwork, we just need to declare things to use in the future.

- static: a directory where we store our files which will not me generated dynamically, css, maybe some html static page, and etc.

- templates: here goes all templates that jinja will use to dynamically generate HTML pages, to cast it back to us in app.py.
