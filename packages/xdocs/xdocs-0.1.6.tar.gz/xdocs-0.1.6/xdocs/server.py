import os

from bottle import static_file, Bottle, request
from faker import Factory

app = Bottle(__name__)

app.cwd = os.getcwd()

fake = Factory.create('zh_CN')


@app.route('/')
def index():
    return static_file("index.html", app.cwd + "/client/")


@app.route('/resource')
def index():
    return static_file("resource", app.cwd + "/client/")


@app.route('/docs/<filename>')
def docs(filename):
    return static_file(filename, root=app.cwd + '/docs')


@app.route('/static/<filename>')
def static(filename):
    return static_file(filename, root=app.cwd + '/client/static')


@app.route('/static/<filename>')
def list(filename):
    return static_file(filename, root=app.cwd + '/client/static')


@app.route('/api/<resources>/', method='GET')
def list(resources):
    return {resources: request.method}


@app.route('/api/<resources>/', method='POST')
def create(resources):
    return {resources: request.method}


@app.route('/api/<resources>/<resource_id>/', method='GET')
def retrieve(resources, resource_id):
    return {resources: resource_id + request.method}


@app.route('/api/<resources>/<resource_id>/', method='PUT')
def replace(resources, resource_id):
    return {resources: resource_id + request.method}


@app.route('/api/<resources>/<resource_id>/', method='PATCH')
def update(resources, resource_id):
    return {resources: resource_id + request.method}


@app.route('/api/<resources>/<resource_id>/', method='DELETE')
def delete(resources, resource_id):
    return {resources: resource_id + request.method}
