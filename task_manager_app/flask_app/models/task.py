# from winreg import QueryInfoKey
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from datetime import datetime
import math
from flask import flash

db = 'ahf_db'

class Task:
    def __init__(self, data):
        self.id = data['id']
        self.task_name = data['task_name']
        self.due_date = data['due_date']
        self.priority = data['priority']
        self.complete = data['complete']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

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
    def create_task(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES (%(task_name)s,%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    # Will Call Station Tasks
    @classmethod
    def assign_will_call_1(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Will Call Report',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_will_call_2(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Delivery Report',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_will_call_3(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Not Scanned Report',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_will_call_4(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Pending in Store Receiving',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_will_call_5(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Check Voice Mail',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result
    @classmethod
    def assign_will_call_6(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Visual check Will Call',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_will_call_7(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('File Prescriptions',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    # Shipping Station Tasks
    @classmethod
    def assign_shipping_1(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Clean and Calibrate Kirbys',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_shipping_2(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Receive Cardinal Order',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_shipping_3(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('PSA Report',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_shipping_4(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('FedEx Exception Report',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_shipping_5(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Financial Hardship Report',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_shipping_6(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Submit Daily Order',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    # Shipping drop off Tasks
    @classmethod
    def assign_drop_off_1(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Calendar Events',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_drop_off_2(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Check Sfax RXs',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_drop_off_3(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Refill Queue',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_drop_off_4(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Rejection Queue',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    # Shipping station 1 Tasks
    @classmethod
    def assign_station_one_1(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('AR Report',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_station_one_2(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Receive Mail',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_station_one_3(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Check CRC emails (afternoon)',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_station_one_4(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Brinks (Tuesday)',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    # Shipping station 2 Tasks
    @classmethod
    def assign_station_two_1(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('Bill Nursing homes',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def assign_station_two_2(cls, data):
        query= "INSERT INTO tasks (task_name, user_id, priority, complete, due_date) VALUES ('35 Day Report',%(user_id)s,%(priority)s,%(complete)s,%(due_date)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def get_all_tasks(cls,data):
        query = "SELECT * FROM tasks"
        results = connectToMySQL(db).query_db(query,data)
        all_tasks = []
        for task in results:
            all_tasks.append( cls(task) )
        return all_tasks

# get all tasks that belong to one user
    @classmethod
    def get_all_user_tasks(cls,data):
        query = "SELECT * FROM tasks WHERE user_id =  %(user2)s"
        results = connectToMySQL(db).query_db(query,data)
        taskss = []
        for task in results:
            taskss.append( cls(task) )
        return taskss

    @classmethod
    def complete_update(cls, data):
        query = "UPDATE tasks SET complete=%(complete)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM tasks WHERE tasks.id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_task( task ):
        is_valid = True
        if len(task['task_name']) < 3:
            flash("Task name must be at least 3 characters","task")
            is_valid= False
        if len(task['due_date']) < 3:
            flash("Must Select Due Date!","task")
            is_valid= False

        return is_valid

    @staticmethod
    def validate_station( task ):
        is_valid = True
        if len(task['due_date']) < 3:
            flash("Must Select Due Date!","station")
            is_valid= False

        return is_valid