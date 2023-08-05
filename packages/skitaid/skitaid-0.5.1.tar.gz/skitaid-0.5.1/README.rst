======================
Skitai WSGI App Engine
======================

.. contents:: Table of Contents


Changes
========

- 0.5 - now, default executable python become a python3


Introduce
===========

Skitai WSGI App Engine (SWAE) is an daemonizer using Skitai_.

SWAE is a kind of branch of `Medusa Web Server`__ - A High-Performance Internet Server Architecture.

Medusa is different from most other servers because it runs as a single process, multiplexing I/O with its various client and server connections within a single process/thread.

- HTTP/HTTPS Web, XML-RPC Server
- Loadbancing/Cache, API Gateway Server
- HTML5 Websocket Implemeted
- HTTP/2.0 Implemeted
- Multiple Worker Processes (Posix Only)

.. __: http://www.nightmare.com/medusa/medusa.html



Installation / Startup
=========================

**On Posix**

.. code-block:: bash

    sudo pip3 install --no-cache-dir skitaid
    
Option '--no-cache-dir' is should be given, otherwise installation is not working. I don't know why.

If you want to reinstall forcely,

.. code-block:: bash

    sudo pip3 install --no-cache-dir --upgrade --force skitaid


Another way from Git:

.. code-block:: bash

    git clone https://gitlab.com/hansroh/skitaid.git
    cd skitaid
    python setup.py install

For starting Skitai:

.. code-block:: bash
  
    sudo skitaid.py -v &
    sudo skitaid.py stop

    #if everythig is OK,
    
    sudo service skitaid start
    sudo service skitaid stop
    
    #For auto run on boot,
    sudo update-rc.d skitaid defaults
    or
    sudo chkconfig skitaid on


**On Win32**

.. code-block:: bash

    pip install skitaid
    
    cd c:\skitaid\bin
    skitaid.py -v
    skitaid.py stop (in another command prompt)
    
    #if everythig is OK,    
    install-win32-service.py install
    
    #For auto run on boot,
    install-win32-service.py --startup auto install    
    install-win32-service.py start
    install-win32-service.py stop
    

Mounting WSGI Apps and Static Directories
===========================================

Here's three WSGI app samples:

*WSGI App* at /var/wsgi/wsgiapp.py

.. code:: python
  
  def app (env, start_response):
    start_response ("200 OK", [("Content-Type", "text/plain")])
    return ['Hello World']


*Flask App* at /var/wsgi/flaskapp.py

.. code:: python

  from flask import Flask  
  app = Flask(__name__)  
  
  @app.route("/")
  def index ():	 
    return "Hello World"


*Skitai-Saddle App* at /var/wsgi/skitaiapp.py

.. code:: python

  from skitai.saddle import Saddle  
  app = Saddle (__name__)
  
  @app.route('/')
  def index (was):	 
    return "Hello World"

For mounting to SWAE, modify config file in /etc/skitaid/servers-enabled/example.conf

.. code:: python
  
  [routes:line]
  
  ; for files like images, css
  / = /var/wsgi/static
  
  ; app mount syntax is path/module:callable
  / = /var/wsgi/wsgiapp:app
  /aboutus = /var/wsgi/flaskapp:app
  /services = /var/wsgi/skitaiapp:app
  
You can access Flask app from http://127.0.0.1:5000/aboutus and other apps are same.


**Note: Mount point & App routing**

If app is mounted to '/flaskapp',

.. code:: python
   
  from flask import Flask    
  app = Flask (__name__)       
  
  @app.route ("/hello")
  def hello ():
    return "Hello"

Above /hello can called, http://127.0.0.1:5000/flaskapp/hello

Also app should can handle mount point. 
In case Flask, it seems 'url_for' generate url by joining with env["SCRIPT_NAME"] and route point, so it's not problem. Skitai-Saddle can handle obiously. But I don't know other WSGI middle wares will work properly.


Configuration / Management
============================================

Now let's move on to new subject about server configuration amd mainternance.

Configuration
--------------

Configuration files are located in '/etc/skitaid/servers-enabled/\*.conf', and on win32, 'c:\\skitaid\\etc\\servers-enabled/\*.conf'.

Basic configuration is relatively simple, so refer commets of config file. Current config file like this:

.. code:: python

  [server]
  threads = 4
  processes = 2
  ip = 127.0.0.1
  port = 5000
  name = 
  
  [ssl]
  enable_ssl = no
  certfile = server.pem
  keyfile = server.key
  passphrase = 
 
  [tunefactors]
  static_max_age = 300
  response_timeout = 10
  keep_alive = 10
  num_result_cache_max = 200
  
  [proxypass]
  cache_memory = 8
  cache_disk = 0
    
  [routes:line]
  / = /var/wsgi/example/static
  / = /var/wsgi/example/webapp
  /about = @python
  
  [@python]
  ssl = yes
  members = www.python.org:443
  
  [@sqlite3]
  type = sqlite3
  members = /var/wsgi/example/resources/sqlite3.db


Here's configs required your carefulness.

- ip: default is 127.0.0.1 then you can only access to server via 127.0.0.1. If you want to access via public IP, set 0.0.0.0
- processes: number of workers but on Win32, only 1 is valid
- threads: generally not up to 4 per CPU. If set to 0, Skitai run with entirely single thread. so be careful if your WSGI function takes long time or possibly will be delayed by blocking operation.
- num_result_cache_max: number of cache for HTTP/RPC/DBMS results
- response_timeout: transfer delay timeout caused by network problem


Mounting With Virtual Host
-----------------------------

*New in version 0.10.5*

App can be mounted with virtual host.

.. code-block:: bash

  [routes:line]
 
  / = /home/user/www/static
  / = /home/user/www/wsig:app
  
  
  # exactly matching host  
  @ www.mydomain.com mydomain.com 
     
  / = /home/user/mydomain.www/static
  /service = /home/user/mydomain.www/wsgi:app
  
  
  # matched *.mydomain.com include mydomain.com
  @ .mydomain.com
  
  / = home/user/mydomain.any/static 
  / = home/user/mydomain.any/wsgi:app 


  # matched *.mydomain2.com except mydomain2.com
  @ *.mydomain.com
  
  / = home/user/mydomain2.any/static 
  / = home/user/mydomain2.any/wsgi:app 


As a result, the app location '/home/user/mydomain.www/wsgi.py' is mounted to 'www.mydomain.com/service' and 'mydomain.com/service'.


Log Files
-----------

If Skitai run with skitaid.py, there're several processes will be created.

Sample ps command's result is:

.. code-block:: bash

  ubuntu:~/skitai$ ps -ef | grep skitaid
  root     19146 19145  0 Mar03 pts/0    00:00:11 /usr/bin/python /usr/local/bin/skitaid.py
  root     19147 19146  0 Mar03 pts/0    00:00:05 /usr/bin/python /usr/local/bin/skitaid-smtpda.py
  root     19148 19146  0 Mar03 pts/0    00:00:03 /usr/bin/python /usr/local/bin/skitaid-cron.py
  root     19150 19146  0 Mar03 pts/0    00:00:00 /usr/bin/python /usr/local/bin/skitaid-instance.py --conf=example

- /usr/local/bin/skitaid.py : Skitaid Daemon manages all Skitais sub processes
- /usr/local/bin/skitaid-instance.py : Skitai Instance with example.conf
- /usr/local/bin/skitaid-smtpda.py : SMTP Delivery Agent
- /usr/local/bin/skitaid-cron.py : Cron Agent

Skitai Daemon log file is located at:

- posix:  /var/log/skitaid/skitaid.log
- win32: c:\\skitaid\\log\\skitaid.log

To view latest 16Kb log,

  skitaid.py log

SMTP Delivery Agent log is located at:

- posix:  /var/log/skitaid/daemons/smtpda/smtpda.log
- win32: c:\\skitaid\\log\\daemons\\smtpda\\smtpda.log
- skitaid.py -f smtpda log

Cron Agent log is located at:

- posix:  /var/log/skitaid/daemons/cron/cron.log
- win32: c:\\skitaid\\log\\daemons\\cron\\cron.log
- skitaid.py -f cron log


If Skitai App Engine Instances config file is 'example.conf', log file located at:

- posix:  /var/log/skitaid/instances/example/[server|request|app].log
- win32: c:\\skitaid\\log\\instances\\example\\[server|request|app].log
- skitaid.py -f cron -s [server|request|app] log

To view lateset log, 

.. code:: python

  skitaid.py -f example log

Above log is like this:

.. code:: python
  
  2016.03.03 03:37:41 [info] called index
  2016.03.03 03:37:41 [error] exception occured
  2016.03.03 03:37:41 [expt:bp1] <type 'exceptions.TypeError'>\
    index() got an unexpected keyword argument 't'\
    [/skitai/saddle/wsgi_executor.py|chained_exec|51]
  2016.03.03 03:37:41 [info] done index


SMTP Delivery Agent
--------------------

e-Mail sending service is executed seperated system process not threading. Every e-mail is temporary save to file system, e-Mail delivery process check new mail and will send. So there's possibly some delay time.

You can send e-Mail in your app like this:

.. code:: python

    # email delivery service
    e = was.email (subject, snd, rcpt)
    e.set_smtp ("127.0.0.1:465", "username", "password", ssl = True)
    e.add_text ("Hello World<div><img src='cid:ID_A'></div>", "text/html")
    e.add_attachment (r"001.png", cid="ID_A")
    e.send ()

With asynchronous email delivery service, can add default SMTP Server config to skitaid.conf (/etc/skitaid/skitaid.conf or c:\skitaid\etc\skitaid.conf).
If it is configured, you can skip e.set_smtp(). But be careful for keeping your smtp password.

.. code:: python

    [smtpda]
    smtpserver = 127.0.0.1:25
    user = 
    password = 
    ssl = no
    max_retry = 10
    undelivers_keep_max_days = 30

Log file is located at /var/log/skitaid/daemons/smtpda/smtpda.log or c:\skitaid\log\daemons\smtpda\smtpda.log



Batch Task Scheduler
-----------------------

*New in version 0.14.5*

Sometimes app need batch tasks for minimum response time to clients. At this situateion, you can use taks scheduling tool of OS - cron, taks scheduler - or can use Skitai's batch task scheduling service for consistent app management. for this, add jobs configuration to skitaid.conf (/etc/skitaid/skitaid.conf or c:\\skitaid\\etc\\skitaid.conf) like this.

.. code:: python

  [crontab:line]
  
  */2 */2 * * * /home/apps/monitor.py  > /home/apps/monitor.log 2>&1
  9 2/12 * * * /home/apps/remove_pended_files.py > /dev/null 2>&1

Taks configuarion is same with posix crontab.

Cron log file is located at /var/log/skitaid/daemons/cron/cron.log or c:\skitaid\log\daemons\cron\cron.log


Running Skitai as HTTPS Server
---------------------------------

Simply config your certification files to config file (ex. /etc/skitaid/servers-enabled/example.conf). 

.. code:: python

  [ssl]
  ssl = no
  certfile = server.pem
  keyfile = server.key
  passphrase = fatalbug

To genrate self-signed certification file:

.. code:: python

    openssl req -new -newkey rsa:2048 -x509 -keyout server.pem -out server.pem -days 365 -nodes
    
For more detail please read README.txt in /etc/skitaid/certifications/README.txt


**Note For Win32 Python 3 Users**

Change python key value to like `c:\\python34\\python.exe` in c:\\skitaid\\etc\\skitaid.conf.


**Skitai with Nginx / Squid**

From version 0.10.5, Skitai supports virtual hosting itself, but there're so many other reasons using with reverse proxy servers.

Here's some helpful sample works for virtual hosting using Nginx / Squid.

If you want 2 different and totaly unrelated websites:

- www.jeans.com
- www.carsales.com

And make two config in /etc/skitaid/servers-enabled

- jeans.conf *using port 5000*
- carsales.conf *using port 5001*

Then you can reverse proxying using Nginx, Squid or many others.

Example Squid config file (squid.conf) is like this:

.. code:: python
    
    http_port 80 accel defaultsite=www.carsales.com
    
    cache_peer 192.168.1.100 parent 5000 0 no-query originserver name=jeans    
    acl jeans-domain dstdomain www.jeans.com
    http_access allow jeans-domain
    cache_peer_access jeans allow jeans-domain
    cache_peer_access jeans deny all
    
    cache_peer 192.168.1.100 parent 5001 0 no-query originserver name=carsales
    acl carsales-domain dstdomain www.carsales.com
    http_access allow carsales-domain
    cache_peer_access carsales allow carsales-domain
    cache_peer_access carsales deny all

For Nginx might be 2 config files (I'm not sure):

.. code:: python

    ; /etc/nginx/sites-enabled/jeans.com
    server {
	    listen 80;
	    server_name www.jeans.com;
      location / {
        proxy_pass http://192.168.1.100:5000;
      }
    }
    
    ; /etc/nginx/sites-enabled/carsales.com    
    server {
	    listen 80;
	    server_name www.carsales.com;
      location / {
        proxy_pass http://192.168.1.100:5001;
      }
    }


Links
======

- `GitLab Repository`_
- Bug Report: `GitLab issues`_

.. _`GitLab Repository`: https://gitlab.com/hansroh/skitaid
.. _`GitLab issues`: https://gitlab.com/hansroh/skitaid/issues
.. _Skitai: https://pypi.python.org/pypi/skitai


Change Log
==============
  
  0.4
  
  - Server configurration file is changed. You should change it
  - On posix installation, should give option --no-cache-dir

  0.3
  
  - Server configurration file is changed. You should change it
  - On posix installation, should give option --no-cache-dir
  
  0.1
  
  - seperated from Skitai_

  