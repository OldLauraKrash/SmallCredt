About project
=============

Lenders compete to provide financing to small businesses on best terms.

Database setup
==============
Now, edit mysite/settings.py. It’s a normal Python module with module-level variables representing Django settings. Change the following keys in the DATABASES 'default' item to match your database connection settings.

ENGINE – Either 'django.db.backends.postgresql_psycopg2', 'django.db.backends.mysql', 'django.db.backends.sqlite3' or 'django.db.backends.oracle'. Other backends are also available.

NAME – The name of your database. If you’re using SQLite, the database will be a file on your computer; in that case, NAME should be the full absolute path, including filename, of that file. If the file doesn’t exist, it will automatically be created when you synchronize the database for the first time (see below).

When specifying the path, always use forward slashes, even on Windows (e.g. C:/homes/user/mysite/sqlite3.db).

USER – Your database username (not used for SQLite).

PASSWORD – Your database password (not used for SQLite).

HOST – The host your database is on. Leave this as an empty string (or possibly 127.0.0.1) if your database server is on the same physical machine (not used for SQLite). See HOST for details.


The development server
======================
Let’s verify this worked. Change into the outer mysite directory, if you haven’t already, and run the command python manage.py runserver. You’ll see the following output on the command line:

Validating models...

0 errors found

April 19, 2013 - 15:50:53

Django version 1.5, using settings 'mysite.settings'

Development server is running at http://127.0.0.1:8000/

Quit the server with CONTROL-C.