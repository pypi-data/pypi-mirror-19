import os

from bottle import static_file, Bottle

app = Bottle(__name__)

app.cwd = os.getcwd()

from faker import Faker

fake = Faker()


@app.route('/')
def index():
    return static_file("index.html", app.cwd + "/client/")


@app.route('/docs/<filename>')
def docs(filename):
    return static_file(filename, root=app.cwd + '/docs')


@app.route('/static/<filename>')
def static(filename):
    return static_file(filename, root=app.cwd + '/client/static')


