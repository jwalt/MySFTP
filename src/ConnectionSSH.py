import os
import sys
from .Configuration import Configuration
try:
	import pty, select
except Exception as e:
	print(e)


_b = sys.version_info[0] < 3 and (lambda x:x) or (lambda x:x.encode('utf-8'))

class ConnectionSSH():

	@staticmethod
	def ssh_exec(args, capture_output=False):
		log = []
		# [
		#	0. "sftp",
		#	***. Connection.user + "@" + Connection.host, Before this parameter was sent
		#	1. "cd " + currentPath + " && ls -lrt | sed '/ \.$/d' | sed '/ \.\.$/d'"
		#]
		#args = [arguments[0], "-p " + Configuration.port, Configuration.user + "@" + Configuration.host, arguments[1]]
		program = args[0] # sftp or ssh
		port = '-P ' + Configuration.port
		user_host = Configuration.user + "@" + Configuration.host
		command_remote = "cd '{}'".format(Configuration.currentPath) + args[1]
		log.append("\n".join(args))
		# create pipe for stdout
		stdout_fd, w1_fd = os.pipe()
		stderr_fd, w2_fd = os.pipe()
		r1_fd, pty_fd = os.pipe()
		
		#pid, pty_fd = pty.fork()
		pid = os.fork()
		if not pid:
			log.append("if Not pid")
			os.close(pty_fd)
			os.close(stdout_fd)
			os.close(stderr_fd)
			os.dup2(r1_fd, 0)
			os.dup2(w1_fd, 1)
			os.dup2(w2_fd, 2)
			os.close(r1_fd)
			os.close(w1_fd)
			os.close(w2_fd)
			
			args = [ program ]
			if Configuration.password:
				args.extend(["-o", 'PubkeyAuthentication=no'])

			if program == 'sftp':
				args.extend([port, user_host])
			elif program == 'ssh':
				args.extend([user_host, command_remote])

			os.execvp(args[0], args)
		
		os.close(r1_fd)
		os.close(w1_fd)
		os.close(w2_fd)
		
		output = bytearray()
		rd_fds = [stdout_fd, stderr_fd]

		def _read(fd):
			if fd not in rd_ready:
				return 

			try:
				data = os.read(fd, 128*1024)
			except (OSError, IOError, Exception):
				data = None

			if not data:
				rd_fds.remove(fd)

			return data

		try:
			time_out = 1.76
			log.append(str(rd_fds))
			while rd_fds:

				rd_ready, _, _ = select.select(rd_fds, [], [], time_out)
				
				log.append("1. Status rd_ready:" + str(rd_ready))
				if rd_ready == [] and command_remote.find("ls -lrt") != -1:
					limit = 0
					while limit <= 10 and rd_ready == []:
						rd_ready, _, _ = select.select(rd_fds, [], [], 1)
						limit = limit + 1
					log.append("2. Status rd_ready:" + str(rd_ready))
				
				if rd_ready:
					# Deal with stdout
					data = _read(stdout_fd)
					if data is not None:
						if capture_output:
							output.extend(data)
							log.append("Data is not none and is added to the output")
							time_out = 1.28
						else:
							log.append("Data is not none is not added to the output")
							sys.stdout.write(data.decode('utf-8', 'ignore'))

					# Mensajes del promp
					data = _read(stderr_fd)
					if data is not None:
						if b'assword:' in data:
							os.write(pty_fd, _b(Configuration.password + '\n'))
							log.append("password was typed")
						elif b're you sure you want to continue connecting' in data:
							os.write(pty_fd, b'yes\n')
							log.append("It was said that if you wanted to continue")
						elif rd_ready[0] == stderr_fd and b'onnected to' in data:
							os.write(pty_fd, _b(command_remote + '\n'))
							os.close(pty_fd)
							log.append("Se logro la conexion")
						elif rd_ready[0] == stderr_fd and b'Permission denied, please try again.' in data:
							log.append("Error entering password")
							output.extend(b'Wrong username or password')
							break
						elif rd_ready[0] == stderr_fd and (
								b'Could not resolve hostname' in data
							or b'No route to host' in data
							or b'Network is unreachable' in data
							or b': Permission denied' in data
							or b'No such file or directory' in data
							or b'not found.' in data
							or b'Couldn\'t delete file: Failure' in data):
							log.append("Terminal returns error.")
							output.extend(data)
						else:
							sys.stderr.write(data.decode('utf-8', 'ignore'))
							log.append("Unidentified error, data is described below")
							log.append( str( data.decode('utf-8', 'ignore') ) )
							log.append(str(stderr_fd))
							log.append(str(rd_ready[0]))
							output.extend(data)
				else:
					log.append("A break was made")
					break
		finally:
			log.append("Crash")
			try: os.close(pty_fd)
			except: pass
			try: os.close(stdout_fd)
			except: pass
			try: os.close(stderr_fd)
			except: pass
			
		pid, retval = os.waitpid(pid, 0)
		return retval, output, log
