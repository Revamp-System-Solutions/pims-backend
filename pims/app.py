import json
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit
from collections import namedtuple
from .model.model import *
from sqlalchemy import desc
from datetime import datetime, timedelta
import dateparser
from .model.schema import *
import base64
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/pims'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)


@socketio.on('connect')
def handleConnect():
    now = datetime.now()
    dow = calendar.day_name[now.weekday()]
    print(dow)
