import click
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.cli.command()
@click.argument('name')
def test_print(name):
  print("Hello " + name)

#from app import admin, routes
