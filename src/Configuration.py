import json
from .extras import readFile, Debug, getPath

class Configuration():
	flag_config = False

	package_path = ''
	mysftp_path = ''
	tmp_path = ''
	servers_path = ''
	psftp_path = ''

	type = 'ftp'
	user = 'root'
	host = '127.0.0.1'
	port = 21
	password = ''
	nick = ''
	currentPath = ''

	snippet = [{
		'nick': '${1:root}',
		'type': '${2:[sftp|ftp]}',
		'host': '${3:[ip_host|server_host_name|domain]}',
		'user': '${4:user}',
		'password': '${5:password}',
		'port': '${6:port}',
		'remote_path': '${7:/var/www/html/}'
	}]

	def __init__(self, config):
		self.type = config[0]['type']
		self.host = config[0]['host']
		self.user = config[0]['user']
		self.port = config[0]['port']
		self.nick = config[0]['nick']
		self.password = config[0]['password']
		self.currentPath = config[0]['remote_path']

	@staticmethod
	def setConfig(json_config_file):
		json_file = json.loads( readFile(json_config_file) )
		Configuration.type = json_file[0]['type']
		if Configuration.type != 'sftp' and Configuration.type != 'ftp':
			sublime.message_dialog('Invalid connection type.')
			Configuration.flag_config = False
			return

		if Configuration.currentPath == '':
			Debug.print("It is empty.")
			Configuration.currentPath = getPath(json_file[0]['remote_path'])
		if Configuration.host != "" and Configuration.host != json_file[0]["host"] and Configuration.user != "" and Configuration.user != json_file[0]["user"]:
			Configuration.currentPath = getPath(json_file[0]['remote_path'])

		Configuration.host = json_file[0]['host']
		Configuration.user = json_file[0]['user']
		Configuration.nick = json_file[0]['nick']

		if Configuration.nick == "":
			sublime.message_dialog('You need to put a Nick.')
			Configuration.flag_config = False
			return

		Configuration.password = json_file[0]['password']
		Configuration.port = json_file[0]['port']

		if Configuration.user == None or Configuration.user == '':
			self.window.run_command("progress_bar", {"message" : "Host server not defined in configuration file"})
		if Configuration.host == None or Configuration.host == '':
			self.window.run_command("progress_bar", {"message" : "Host server not defined in configuration file"})
		if Configuration.password == None or Configuration.password == '':
			self.window.run_command("progress_bar", {"message" : "The password has not been defined in the configuration file"})
		if Configuration.user == None or Configuration.user == '' or Configuration.host == None or Configuration.host == '' or Configuration.password == None or Configuration.password == '': 
			Configuration.flag_config = False
			return
		Configuration.flag_config = True

	@staticmethod
	def getJsonConfig():
		return json.dumps([{
				'nick': Configuration.nick,
				'type': Configuration.type,
				'host': Configuration.host,
				'user': Configuration.user,
				'password': Configuration.password,
				'port': Configuration.port,
				'remote_path': Configuration.currentPath
			}],
			indent='\t'
		)
