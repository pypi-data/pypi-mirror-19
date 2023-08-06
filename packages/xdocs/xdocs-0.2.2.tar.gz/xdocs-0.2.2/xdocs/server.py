import os
import uuid

from bottle import static_file, Bottle, request, response, abort
from faker import Factory
from yaml import load

app = Bottle(__name__)

fake = Factory.create('zh_CN')

base_path = os.getcwd()
source_path = os.path.join(base_path, 'docs')

app.data = {}
app.resources = {}

for file in os.listdir(source_path):
    if '.yml' in file:
        resource = load(open(os.path.join(source_path, file)).read())
        app.resources[resource['name']] = resource


def generate_mock_data(file_type):
    return eval("fake.{}()".format(file_type))


def setup_data(resources):
    for k, v in resources.items():
        app.data[k] = {}
        for i in range(20):
            temp = {}
            for field in v['model'].keys():
                temp[field] = generate_mock_data("name")
            temp['id'] = uuid.uuid4().__str__()
            app.data[k][temp["id"]] = temp


setup_data(app.resources)


def dict_filter_by_array(source_dict, array):
    result = {}
    for field in array:
        if field in source_dict:
            result[field] = source_dict[field]
    return result


@app.route('/')
def index():
    """documentation web page as the home page"""
    return static_file("index.html", base_path + "/client/")


@app.route('/resource')
def resource():
    """resources is writen in the 'resource' file as a list"""
    return static_file("resource", base_path + "/client/")


@app.route('/docs/<filename>')
def docs(filename):
    """the docs directory is the place where users save there yml documentation file"""
    return static_file(filename, base_path + '/docs')


@app.route('/static/<filename>')
def static(filename):
    """another static file needed by the web pages, such as js css and img"""
    return static_file(filename, base_path + '/client/static')


@app.route('/api/<resources>/', method='GET')
def list(resources):
    """show list of resources"""
    if resources not in app.resources:
        abort(404, "Not Found")

    results = []
    next_page = None
    previous_page = None
    limit = int(request.query.get('limit', 10))
    offset = int(request.query.get('offset', 0))
    count = len(app.data[resources])

    for data in app.data[resources].values():
        return_fields = app.resources[resources]['action']['list']['return']
        results.append(dict_filter_by_array(data, return_fields))

    if offset + limit <= len(app.data[resources]):
        next_page = "http://{}/api/{}/?limit={}&offset={}".format(request.get_header('host'),
                                                                  resources,
                                                                  limit,
                                                                  offset + limit)
    if offset - limit >= 0:
        previous_page = "http://{}/api/{}/?limit={}&offset={}".format(request.get_header('host'),
                                                                      resources,
                                                                      limit,
                                                                      offset - limit)
    return {'count': count,
            "next": next_page,
            "previous": previous_page,
            'results': results[offset:(offset + limit)]}


@app.route('/api/<resources>/', method='POST')
def create(resources):
    """create a new resource"""

    if resources not in app.resources:
        abort(404, "Not Found")

    new_data = dict.fromkeys(app.resources[resources]["model"].keys())
    for key in new_data:
        if key in request.json:
            new_data[key] = request.json.get(key)
    new_data['id'] = uuid.uuid4().__str__()
    app.data[resources][new_data['id']] = new_data
    return new_data


@app.route('/api/<resources>/<resource_id>/', method='GET')
def retrieve(resources, resource_id):
    """show the retrieve of resource"""
    if resources not in app.resources or resource_id not in app.data[resources]:
        abort(404, "Not Found")

    return app.data[resources][resource_id]


@app.route('/api/<resources>/<resource_id>/', method='PUT')
def replace(resources, resource_id):
    """replace the resource"""
    if resources not in app.resources or resource_id not in app.data[resources]:
        abort(404, "Not Found")

    for key in app.data[resources][resource_id].keys():
        app.data[resources][resource_id][key] = request.json.get(key)
    return app.data[resources][resource_id]


@app.route('/api/<resources>/<resource_id>/', method='PATCH')
def update(resources, resource_id):
    """update the resource"""
    if resources not in app.resources or resource_id not in app.data[resources]:
        abort(404, "Not Found")
    for key, value in app.data[resources][resource_id].items():
        app.data[resources][resource_id][key] = request.json.get(key, value)
    return app.data[resources][resource_id]


@app.route('/api/<resources>/<resource_id>/', method='DELETE')
def destroy(resources, resource_id):
    """destroy the resource from app.data"""
    if resources not in app.resources or resource_id not in app.data[resources]:
        abort(404, "Not Found")
    del app.data[resources][resource_id]
    response.status = 204
    return ""


@app.error(404)
def error_handler_404(error):
    return "Not Found"
