import sublime
import sublime_plugin
import time
from datetime import datetime
from threading import Thread, currentThread, current_thread
from .Configuration import Configuration
from .extras import Debug

hilo = None;

class ShowProgressBarCommand(sublime_plugin.TextCommand):
	cntLine = 0
	t = None
	view_only = None
	timer = None
	loading = False

	def run(self, edit, msg = '', loading = False, stop = False, replace_flag = False):
		if self.view_only == None:
			self.view_only = self.view.window().find_output_panel("progress_bar")
		view = self.view_only
		if view == None:
			self.view.run_command("progress_bar", {'msg': msg})
		else:
			if view.settings().get('syntax') != 'MySFTP.sublime-syntax':
				self.set_syntax(view)
			if loading == True and stop == False:
				ShowProgressBarCommand.loading = True
				self.timer = sublime.set_timeout(self.showLoading, 128)
			elif loading == False and stop == True:
				ShowProgressBarCommand.loading = False
			elif loading == False and stop == False:
				self.insert(view, edit, msg, replace_flag)

	def showLoading(self):
		if ShowProgressBarCommand.loading:
			sublime.active_window().run_command("show_progress_bar", {'msg': "*", "replace_flag": True})
			self.timer = sublime.set_timeout(self.showLoading, 128)

	def insert(self, view, edit, msg, replace_flag = False):
		view.set_read_only(False)
		point = view.text_point(ShowProgressBarCommand.cntLine, 0)
		view.insert(edit, point, msg)
		#view.set_read_only(True) -> Linea Mala por eso se atoraba el programa
		view.show(point)
		num_lines = msg.count("\n")
		if num_lines == 0:
			ShowProgressBarCommand.cntLine += 1
		else:
			ShowProgressBarCommand.cntLine += num_lines


	def set_syntax(self, view):
		view.settings().set("color_scheme", "MySFTP.sublime-color-scheme")
		view.set_syntax_file("MySFTP.sublime-syntax")

class ProgressBarCommand(sublime_plugin.WindowCommand):

	createPanelOutput = False
	
	def run(self, msg = '', loading = False, stop = False):
		print("method run ProgressBarCommand")
		if ProgressBarCommand.createPanelOutput == False:
			self.window.create_output_panel("progress_bar")
			ProgressBarCommand.createPanelOutput = True
		self.window.run_command("show_panel", {"panel": "output.progress_bar"})
		
		#sublime.set_timeout_async(self.show_progress(msg, loading, stop), 1)
		#def show_progress(self, msg, loading, stop):
		view = self.window.find_output_panel("progress_bar")
		view.run_command("show_progress_bar", {"msg" : msg, "loading": loading, "stop": stop})

	def _destroy(self):
		self.window.destroy_output_panel("progress_bar")

	@staticmethod
	def showMessage(self, msg = ''):
		ProgressBarCommand.getWindow(self).run_command('progress_bar', {"msg": msg})

	@staticmethod
	def initConnection(self):
		ProgressBarCommand.getWindow(self).run_command('progress_bar', {"msg": 'Connecting to the server\nPlugged in: ' + Configuration.host + ' as: ' + Configuration.user + "\n"})

	@staticmethod
	def showList(self):
		ProgressBarCommand.__runLoading(self, "Listing directory '{}'".format(Configuration.currentPath))

	@staticmethod
	def showDownload(self, file_server, file_local):
		ProgressBarCommand.__runLoading(self, "Downloading '{}' en '{}'.".format(file_server, file_local))

	@staticmethod
	def showUpload(self, file_local, file_server):
		ProgressBarCommand.__runLoading(self, "Uploading '{}' en '{}'.".format(file_local, file_server))

	@staticmethod
	def showMakeFile(self, file_name):
		ProgressBarCommand.__runLoading(self, "Creating file '{}'.".format(file_name))

	@staticmethod
	def showMakeDir(self, dir_name):
		ProgressBarCommand.__runLoading(self, "Creating folder '{}'.".format(dir_name))

	@staticmethod
	def showChmod(self, path):
		ProgressBarCommand.__runLoading(self, "Changing permissions to '{}'.".format(path))

	@staticmethod
	def showDelete(self, path):
		ProgressBarCommand.__runLoading(self, "Deleting '{}'.".format(path))

	@staticmethod
	def showRename(self, current_name, new_name):
		ProgressBarCommand.__runLoading(self, "Moving '{}' a '{}'.".format(current_name, new_name))

	@staticmethod
	def showSuccess(self):
		ProgressBarCommand.__stopLoading(self, True)

	@staticmethod
	def showError(self):
		ProgressBarCommand.__stopLoading(self, False)

	@staticmethod
	def showCancel(self):
		ProgressBarCommand.__stopLoading(self, False, cancel=True)

	@staticmethod
	def showErrorPermissions(self):
		ProgressBarCommand.__stopLoading(self, False, "You do not have the necessary permissions.")

	@staticmethod
	def showErrorCredentials(self):
		ProgressBarCommand.__stopLoading(self, False, "The username or password is incorrect.")

	@staticmethod
	def showErrorTimeOutExpired(self):
		ProgressBarCommand.__stopLoading(self, False, "Timeout.")

	@staticmethod
	def showConnectionRefuse(self):
		ProgressBarCommand.__stopLoading(self, False, "A connection cannot be established since the destination computer expressly denied the connection.")

	@staticmethod
	def showErrorNoSuchFileOrDirectory(self):
		ProgressBarCommand.__stopLoading(self, False, "The file or directory does not exist.")

	@staticmethod
	def __runLoading(self, msg, show_time=True):
		msg = "{} -> {}".format(datetime.now().strftime("%H:%M:%S"), msg) if show_time else msg
		ProgressBarCommand.getWindow(self).run_command('progress_bar', {"msg": "{} ".format(msg)})
		ProgressBarCommand.getWindow(self).run_command('progress_bar', {"loading": True})

	@staticmethod
	def __stopLoading(self, success, msg='', cancel=False):
		msg = "success.\n" if success else ("error.\n{}\n".format(msg) if msg != '' else "error.\n")
		msg = "Cancel.\n" if cancel else msg
		ProgressBarCommand.getWindow(self).run_command("progress_bar", {"stop": True})
		ProgressBarCommand.getWindow(self).run_command("progress_bar", {"msg": " {}".format(msg)})

	@staticmethod
	def getWindow(objecto):
		parents = objecto.__class__.__bases__
		name_class = parents[0].__name__
		if name_class == 'WindowCommand':
			return objecto.window
		elif name_class == 'TextCommand':
			return objecto.view.window()
