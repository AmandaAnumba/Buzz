from flask import Flask

buzz = Flask(__name__)
from buzz import views