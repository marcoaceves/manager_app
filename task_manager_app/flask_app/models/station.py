# from winreg import QueryInfoKey
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from datetime import datetime
import math
from flask import flash

db = 'ahf_db'

class Station:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.task_name = data['task_name']


    @classmethod
    def create_station(cls, data):
        query= "INSERT INTO stations (name, task_name) VALUES (%(name)s,%(task_name)s);"
        result = connectToMySQL(db).query_db(query,data)

        return result
    @classmethod
    def get_all_stations(cls):
        query = "SELECT ANY_VALUE(id) as id,ANY_VALUE(id) as id,ANY_VALUE(name) as name,ANY_VALUE(task_name) as task_name FROM stations GROUP BY(name);"
        results = connectToMySQL(db).query_db(query)
        stations = []
        for i in results:
            stations.append( cls(i) )
        return stations
    @classmethod
    def get_all_stations_tasks(cls):
        query = "SELECT * FROM stations ORDER BY (name);"
        results = connectToMySQL(db).query_db(query)
        stations_tasks = []
        for i in results:
            stations_tasks.append( cls(i) )
        return stations_tasks
    @classmethod
    def get_one_stations_tasks(cls, data):
        query = 'SELECT * FROM stations WHERE name = %(name)s;'
        results = connectToMySQL(db).query_db(query,data)
        stations_tasks = []
        for i in results:
            stations_tasks.append( cls(i) )
        return stations_tasks
    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM stations WHERE stations.id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy_station(cls, data):
        query = 'DELETE FROM stations WHERE stations.name = %(name)s;'
        return connectToMySQL(db).query_db(query,data)