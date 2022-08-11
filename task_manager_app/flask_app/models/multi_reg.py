# from winreg import QueryInfoKey
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from datetime import datetime
import math
from flask import flash


db = 'ahf_db'

class Multi_Register:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.rph_initial = data['rph_initial']

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} day(s) ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hour(s) ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minute(s) ago"
        else:
            return f"{math.floor(delta.total_seconds())} second(s) ago"

    @classmethod
    def create_signoff_sheet(cls, data):
        query= "INSERT INTO multi_register (date, reg_user_id ) VALUES (%(date)s, %(reg_user_id)s);"
        result = connectToMySQL(db).query_db(query,data)

        return result
    @classmethod
    def get_signoff_sheet(cls, data):
        query = """SELECT id, name, rph_initial, reg_user_id,  date FROM multi_register WHERE reg_user_id = %(reg_user_id)s  ORDER BY (date);"""

        results = connectToMySQL(db).query_db(query, data)
        register_dates = []
        for i in results:
            register_dates.append( cls(i) )
        return register_dates
    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM multi_register WHERE reg_user_id = %(reg_user_id)s;'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def signoff_update(cls, data):
        query = "UPDATE multi_register SET name=%(name)s, rph_initial=%(rph_initial)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)