from flask_app.controllers import users, tasks, translation_service, posts, stations, passwords, signoffsheets
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)
