#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

# Database configuration
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'bench_sharing'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify(user)
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/admin/benchtypes', methods=['GET', 'POST'])
def manage_benchtypes():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BenchTypes")
        benchtypes = cur.fetchall()
        cur.close()
        return jsonify(benchtypes)
    if request.method == 'POST':
        data = request.get_json()
        type_name = data['type_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO BenchTypes (type_name) VALUES (%s)", [type_name])
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'BenchType added successfully'})

@app.route('/resources', methods=['GET', 'POST'])
def manage_resources():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Resources")
        resources = cur.fetchall()
        cur.close()
        return jsonify(resources)
    if request.method == 'POST':
        data = request.get_json()
        resource_name = data['resource_name']
        type_id = data['type_id']
        description = data['description']
        available_from = data['available_from']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Resources (resource_name, type_id, description, available_from) VALUES (%s, %s, %s, %s)", 
                    (resource_name, type_id, description, available_from))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Resource added successfully'})

@app.route('/resources/<int:resource_id>/book', methods=['POST'])
def book_resource(resource_id):
    data = request.get_json()
    company_id = data['company_id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Resources SET company_id=%s, booked_at=NOW() WHERE resource_id=%s", (company_id, resource_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Resource booked successfully'})

@app.route('/resources/<int:resource_id>/release', methods=['POST'])
def release_resource(resource_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Resources SET company_id=NULL, booked_at=NULL WHERE resource_id=%s", (resource_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Resource released successfully'})

if __name__ == '__main__':
    app.run(debug=True)

