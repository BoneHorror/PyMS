
from . import Assets
from .setutils import PYMS_SETTINGS
from .PyMSDialog import PyMSDialog
from .UIKit import *

import json, urllib.request, urllib.parse, urllib.error
from _thread import start_new_thread

class UpdateDialog(PyMSDialog):
	BRANCH = 'master' # Default to `master` branch, but can be update for long-lived branches

	@staticmethod
	def check_update(window, program):
		pass

	def __init__(self, parent, program, versions):
		self.program = program
		self.versions = versions
		PyMSDialog.__init__(self, parent, 'New Version Found', resizable=(False, False))

	def widgetize(self):
		text = "A new version of PyMS is available. It is recommended that you update as soon as possible."
		Label(self, justify=LEFT, anchor=W, text=text).pack(pady=5,padx=5)
		f = Frame(self)
		self.remind = IntVar()
		remindme = PYMS_SETTINGS.get('remindme', True)
		self.remind.set(remindme == True or remindme != Assets.version('PyMS'))
		Checkbutton(f, text='Remind me later', variable=self.remind).pack(side=LEFT, padx=5)
		Hotlink(f, 'Github', 'https://github.com/poiuyqwert/PyMS').pack(side=RIGHT, padx=5)
		f.pack(fill=X, expand=1)
		ok = Button(self, text='Ok', width=10, command=self.ok)
		ok.pack(pady=5)
		return ok

	def ok(self):
		PYMS_SETTINGS.remindme = [Assets.version('PyMS'),1][self.remind.get()]
		PYMS_SETTINGS.save()
		PyMSDialog.ok(self)

class SemVer(object):
	def __init__(self, version):
		self.meta = None
		if '-' in version:
			version,self.meta = version.split('-')
		components = (int(c) for c in version.split('.'))
		self.major, self.minor, self.patch = components

	def __lt__(self, other):
		if not isinstance(other, SemVer):
			return False
		if self.major < other.major:
			return True
		elif self.major > other.major:
			return False
		if self.minor < other.minor:
			return True
		elif self.minor > other.minor:
			return False
		if self.patch < other.patch:
			return True
		elif self.patch > other.patch:
			return False
