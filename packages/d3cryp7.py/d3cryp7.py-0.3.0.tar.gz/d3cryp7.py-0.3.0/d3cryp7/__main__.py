from configparser import ConfigParser
from d3cryp7.blueprints import api, config
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from os import path
import argparse
import d3cryp7

app = Flask(__name__)
app.register_blueprint(api.blueprint, url_prefix = '/api')
app.register_blueprint(config.blueprint, url_prefix = '/config')
Bootstrap(app)

@app.route('/')
def index():
	'''
	The index of the HTTP server
	'''

	return render_template('index.html')

def main():
	'''
	The main method and entry point of the application
	'''

	parser = argparse.ArgumentParser(
		description = 'd3cryp7 v%s' % d3cryp7.__version__
	)
	parser.add_argument(
		'-c', '--config',
		type = str,
		dest = 'config_file',
		action = 'store',
		default = path.expanduser('~') + '/.d3cryp7.ini',
		help = 'the configuration file to use (default: ~/.d3cryp7.ini)'
	)
	parser.add_argument(
		'--host',
		type = str,
		dest = 'host',
		action = 'store',
		default = '0.0.0.0',
		help = 'the host IP to listen to (default: 0.0.0.0)'
	)
	parser.add_argument(
		'--port',
		type = int,
		dest = 'port',
		action = 'store',
		default = 80,
		help = 'the port to listen to (default: 80)'
	)
	parser.add_argument(
		'--version',
		action = 'version',
		version = 'd3cryp7 v%s' % d3cryp7.__version__
	)
	args = parser.parse_args()
	config = ConfigParser()

	if len(config.read(args.config_file)) == 0:
		config['DEFAULT'] = {
			'host': args.host,
			'port': args.port
		}
		config['Clarifai'] = {
			'app_id': '',
			'app_secret': ''
		}

		with open(args.config_file, 'w') as config_file:
			config.write(config_file)

	d3cryp7.__host__ = config['DEFAULT']['host']
	d3cryp7.__port__ = config['DEFAULT']['port']
	d3cryp7.__conf__ = args.config_file
	d3cryp7.config = config

	try:
		print('d3cryp7 v%s\n' % d3cryp7.__version__)
		app.run(d3cryp7.__host__, d3cryp7.__port__, threaded = True)
		print()
	except PermissionError as e:
		if args.port < 1024:
			print('Only the root user can bind to port %i\n' % d3cryp7.__port__)
		else:
			print('An unknown error occured:\n')
			print(e, end = '\n\n')

	exit(d3cryp7.__status__.value)

if __name__ == '__main__':
	main()
