import logging
import os
import shutil

import click
from flask_script import Manager
from livereload import Server

from .server import app

logging.basicConfig(format='[%(levelname)s]:%(message)s', level=logging.INFO)

config_text = 'site_name: My Docs\n'
todo_text = """model:
    - id:
        verbose: id
        type: string
    - title:
        verbose: 标题
        max_length: 20
        min_length: 10
        type: string
    - content:
        verbose: 内容
        type: text
    - category:
        verbose: 类别
        type: string
    - tags:
        verbose: 标签
        type: array

action:
    list:
      args:
      - search
      - limit
      - offset
      - ordering
      return:
      - id
      - title
    retrieve:
      return:
      - id
      - title
      - content
      - category
      - tags
    create:
      send:
      - title
      - content
      - category
      - tags
      return:
      - id
    replace:
      send:
      - id
      - title
      - content
      - category
      - tags
      return:
      - id
      - title
      - content
      - category
      - tags
    update:
      send:
      - id
      - title
      - content
      - category
      - tags
      return:
      - id
      - title
      - content
      - category
      - tags
    destroy:
      return: null
"""


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """
    XDocs - Documentation drives developing.
    """


@cli.command(name="new")
@click.argument('output_dir')
def new(output_dir):
    """Create a new XDocs project"""
    docs_dir = os.path.join(output_dir, 'docs')
    config_path = os.path.join(output_dir, 'xdocs.yml')
    todo_path = os.path.join(docs_dir, 'Todo.yml')
    if os.path.exists(output_dir):
        logging.warning('Directory already exists.')
        return

    logging.info('Creating project directory: %s', output_dir)
    os.mkdir(output_dir)

    logging.info('Writing config file: %s', config_path)
    open(config_path, 'w').write(config_text)

    logging.info('Writing initial docs: %s', todo_path)
    os.mkdir(docs_dir)
    open(todo_path, 'w').write(todo_text)
    logging.info('Project %s created!', output_dir)


@cli.command(name="run")
@click.option('-p', '--port',
              help='IP address and port to serve documentation locally (default:"localhost:8000")',
              metavar='<IP:PORT>')
def run(port):
    """Run the builtin development server"""
    script_path = os.path.dirname(os.path.realpath(__file__))
    base_path = os.getcwd()
    source_path = os.path.join(base_path, 'docs')
    config_path = os.path.join(base_path, 'xdocs.yml')
    client_path = os.path.join(base_path, 'client')
    if not os.path.exists(config_path):
        logging.warning('The Directory is not a XDocs project.')
        return
    # if os.path.exists("client"):
    #     shutil.rmtree("client")

    logging.info('Coping web pages')
    shutil.copytree(script_path + "/client", "client")

    with open(client_path + "/resource", 'w') as f:
        for file in os.listdir(source_path):
            if '.yml' in file:
                f.writelines(file.split('.')[0])
    if not port:
        port = 8888
    manager = Manager(app)
    live_server = Server(app.wsgi)
    live_server.watch(source_path)
    live_server.serve(restart_delay=0, open_url_delay=True, host="0.0.0.0", port=int(port))
    manager.run()


if __name__ == '__main__':
    cli()
