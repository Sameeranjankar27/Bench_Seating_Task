#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root1'
app.config['MYSQL_PASSWORD'] = 'sameer27'
app.config['MYSQL_DB'] = 'bench_sharing'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

from app import routes


# In[ ]:




