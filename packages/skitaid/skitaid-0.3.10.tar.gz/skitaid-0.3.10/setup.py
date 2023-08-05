"""
Hans Roh 2015 -- http://osp.skitai.com
License: BSD
"""

import skitaid
__VER__ = skitaid.VERSION

import sys
import os
import shutil, glob
from warnings import warn
from distutils.core import setup
import distutils.errors
from setuptools.command.easy_install import easy_install

class easy_install_default(easy_install):
	def __init__(self):
		from distutils.dist import Distribution
		dist = Distribution()
		self.distribution = dist
		self.initialize_options()
		self._dry_run = None
		self.verbose = dist.verbose
		self.force = None
		self.help = 0
		self.finalized = 0

e = easy_install_default()
try: e.finalize_options()
except distutils.errors.DistutilsError: pass
python_lib = e.install_dir

if sys.argv[-1] == 'publish':
	if os.name == "nt":
		os.system('python setup.py sdist upload') # bdist_wininst --target-version=2.7
	else:		
		os.system('python setup.py sdist upload')
	sys.exit()

classifiers = [
  'License :: OSI Approved :: BSD License',
  'Development Status :: 4 - Beta',
  'Topic :: Internet :: WWW/HTTP',
	'Topic :: Internet :: WWW/HTTP :: HTTP Servers',				
	'Environment :: Console',
	'Environment :: No Input/Output (Daemon)',
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Intended Audience :: Developers',
	'Intended Audience :: Science/Research',
	'Programming Language :: Python',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3'
]


packages = ['skitaid']
package_dir = {'skitaid': 'skitaid'}

skitaid_files = [
	"bin/*.py",
	"etc/init/skitaid.conf",
	"etc/init.d/skitaid", 
	"etc/skitaid/skitaid.conf",
	"etc/skitaid/servers-available/README.txt", 
	"etc/skitaid/servers-enabled-posix/example.conf",
	"etc/skitaid/servers-enabled-nt/example.conf",
	"etc/skitaid/certifications/*.*",
	"wsgi/example/*.py",
	"wsgi/example/static/*.*",	
	"wsgi/example/resources/*.*",	
	"wsgi/example/templates/*.*"
]

package_data = {
	"skitaid": skitaid_files
}

def remove_silent (d):
	targets = glob.glob (d)
	if not targets: return
	
	for path in targets:
		if os.path.isdir (path):
			remove_silent (os.path.join (path, "*"))
			try: os.rmdir (path)
			except: pass
			continue
			
		try: 
			os.remove (path)
		except: 
			warn ("can't upgrade file: %s" % path)
					
if os.name == "nt":
	remove_silent ("c:\\skitaid\\bin\\skitaid*.py")
	remove_silent ("c:\\skitaid\\wsgi\\example")
	remove_silent ("c:\\skitaid\\etc\\certifications\\example.*")	
	remove_silent ("c:\\skitaid\\etc\\certifications\\README.*")		
	remove_silent ("c:\\skitaid\\pub")
	remove_silent ("c:\\skitaid\\etc\\servers-enabled\\sample.conf")
	
	data_files = [
		("c:\\skitaid\\etc\\certifications", ["skitaid/etc/skitaid/certifications/README.txt", "skitaid/etc/skitaid/certifications/example.pem", "skitaid/etc/skitaid/certifications/example.key"]),
		("c:\\skitaid\\etc\\servers-available", ["skitaid/etc/skitaid/servers-available/README.txt"]),
		("c:\\skitaid\\bin", ["skitaid/bin/install_win32_service.py", "skitaid/bin/skitaid.py", "skitaid/bin/skitaid-instance.py", "skitaid/bin/skitaid-smtpda.py", "skitaid/bin/skitaid-cron.py"]),
		("c:\\skitaid\\wsgi\\example", ["skitaid/wsgi/example/webapp.py"]),
		("c:\\skitaid\\wsgi\\example\\static", ["skitaid/wsgi/example/static/reindeer.jpg"]),
		("c:\\skitaid\\wsgi\\example\\resources", ["skitaid/wsgi/example/resources/sqlite3.db"]),
		("c:\\skitaid\\wsgi\\example\\templates", ["skitaid/wsgi/example/templates/index.html", "skitaid/wsgi/example/templates/documentation.html", "skitaid/wsgi/example/templates/websocket.html"])
	]
	if not os.path.isfile ("c:\\skitaid\\etc\\skitaid.conf"):
		data_files.append (("c:\\skitaid\\etc", ["skitaid/etc/skitaid/skitaid.conf"]))
		data_files.append (("c:\\skitaid\\etc\\servers-enabled", ["skitaid/etc/skitaid/servers-enabled-nt/example.conf"]))

else:
	os.chmod ("skitaid/etc/init.d/skitaid", 0o755)
	for fn in ("skitaid.py", "skitaid-instance.py", "skitaid-smtpda.py", "skitaid-cron.py"):
		source = os.path.join ("skitaid/bin", fn)
		target = os.path.join ("/usr/local/bin", fn)
		os.chmod (source, 0o755)				
		if not os.path.isfile (target):
			continue
		with open (target, "rb") as f:
			exists_python = f.readline ().strip ()
			if not exists_python.startswith (b"#!"):
				continue		
		with open (source, "rb") as f:
			data = f.read ()
			f.close ()														
		with open (source, "wb") as f:
			data = data.replace (b"#!/usr/bin/python", exists_python, 1)
			f.write (data)
	
	remove_silent ("/etc/init.d/skitaid")
	remove_silent ("/usr/local/bin/skitaid*.py")
	remove_silent ("/var/wsgi/example")	
	remove_silent ("/etc/skitaid/certifications/example.*")	
	remove_silent ("/etc/skitaid/certifications/README.*")
	remove_silent ("/var/local/skitaid-pub")
	remove_silent ("/etc/skitaid/servers-enabled/sample.conf")
	
	data_files = [
		("/etc/skitaid/certifications", ["skitaid/etc/skitaid/certifications/README.txt", "skitaid/etc/skitaid/certifications/example.pem", "skitaid/etc/skitaid/certifications/example.key"]),
		("/etc/skitaid/servers-available", ["skitaid/etc/skitaid/servers-available/README.txt"]),
		("/usr/local/bin", ["skitaid/bin/skitaid.py", "skitaid/bin/skitaid-instance.py", "skitaid/bin/skitaid-smtpda.py", "skitaid/bin/skitaid-cron.py"]),
		("/var/wsgi/example", ["skitaid/wsgi/example/webapp.py"]),
		("/var/wsgi/example/static", ["skitaid/wsgi/example/static/reindeer.jpg"]),
		("/var/wsgi/example/resources", ["skitaid/wsgi/example/resources/sqlite3.db"]),
		("/var/wsgi/example/templates", ["skitaid/wsgi/example/templates/index.html", "skitaid/wsgi/example/templates/documentation.html", "skitaid/wsgi/example/templates/websocket.html"]),
		("/etc/init.d", ["skitaid/etc/init.d/skitaid"])
	]
	if not os.path.isfile ("/etc/skitaid/skitaid.conf"):
		data_files.append (("/etc/skitaid", ["skitaid/etc/skitaid/skitaid.conf"]))
		data_files.append (("/etc/skitaid/servers-enabled", ["skitaid/etc/skitaid/servers-enabled-posix/example.conf"]))

if not os.path.isdir ("skitaid"):
	new_data_files = []
	for target, files in data_files:
		newfiles = []
		for each in files:
			newfiles.append (os.path.join (python_lib, each))
		new_data_files.append ((target, newfiles))
	data_files = new_data_files

setup(
	name='skitaid',
	version=__VER__,
	description='Skitai WSGI App Engine',	
	url = 'https://gitlab.com/hansroh/skitaid',
	author='Hans Roh',
	author_email='hansroh@gmail.com',	
	packages=packages,
	package_dir=package_dir,
	data_files = data_files,
	package_data = package_data,
	license='BSD',
	platforms = ["posix", "nt"],
	download_url = "https://pypi.python.org/pypi/skitaid",
	install_requires = ["skitai>=0.18.4"],
	classifiers=classifiers
)

	