===============
Skitai Library
===============


News & Changes
===============

- 0.20.4 - add Redis connector

- 0.20 - add API Gateway access handler


.. contents:: Table of Contents


Introduce
===========

Skitai is a kind of branch of `Medusa Web Server`__ - A High-Performance Internet Server Architecture.

Medusa is different from most other servers because it runs as a single process, multiplexing I/O with its various client and server connections within a single process/thread.

Skitai orients light-weight, simplicity  and strengthen networking operations with external resources - HTTP / HTTPS / XML-RPC / PostgreSQL_ - keeping very low costs.

- Working as Web, XML-RPC and Reverse Proxy Loadbancing Server
- HTML5 Websocket & HTTP/2.0 implemeted
- Handling massive RESTful API/RPC/HTTP(S) connections based on asynchronous socket framework at your apps easily
- Asynchronous connection pool with PostgreSQL and Redis

Skitai is not a framework for convinient developing, module reusability and plugin flexibility etc. It just provides some powerful communicating services for your WSGI apps as both server and client.

Also note it is inspired by Zope_ and Flask_ a lot.


From version 0.17 (Oct 2016), `Skitai WSGI App Engine`_ is seperated from this project.

If you want to run Skitai with fully pre-configured functional WSGI app engine as daemon or win32 service, install `Skitai WSGI App Engine`_.


Conceptually, Skitai has been seperated into two components:

1. Skitai App Engine Server, for WSGI apps

2. Skito-Saddle, the small WSGI container integrated with Skitai. But you can also mount any WSGI apps and frameworks like Flask.

.. _hyper-h2: https://pypi.python.org/pypi/h2
.. _Zope: http://www.zope.org/
.. _Flask: http://flask.pocoo.org/
.. _PostgreSQL: http://www.postgresql.org/
.. __: http://www.nightmare.com/medusa/medusa.html



Installation
=========================

**Requirements**

On win32, required *pywin32 binary* - http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/

**Optional Requirements**

* Skitaid can find at least one DNS server from system configuration for Async-DNS query. Possibly it is only problem on dynamic IP allocated desktop, then set DNS manually, please.

- *psycopg2* for querying PostgreSQL asynchronously (`win32 binary`_)
- *Jinja2* for HTML Rendering
- *hyper-h2* for HTTP/2 protocol

.. _`win32 binary`: http://www.stickpeople.com/projects/python/win-psycopg/


**Installation**

.. code-block:: bash

    pip install skitai    

Another way from Git:

.. code-block:: bash

    git clone https://gitlab.com/hansroh/skitai.git
    cd skitai
    python setup.py install


But generally you don't need install alone. When you install Skitai App Engine, proper version of Skitai Library will be installed.


Starting Skitai
================

If you want to run Skitai as daemon or win32 service with configuration file, you can install `Skitai WSGI App Engine`_.

Otherwise if your purpose is just WSGI app developement, you can run Skitai easily at console.


Basic Usage
------------

.. code:: python
  
  #WSGI App

  def app (env, start_response):
    start_response ("200 OK", [("Content-Type", "text/plain")])
    return ['Hello World']
    
  app.use_reloader = True
  app.debug = True

  if __name__ == "__main__": 
  
    import skitai
    
    skitai.run (
      mount = [('/', __file__)]
    )

At now, run this code from console.

.. code-block:: bash

  python wsgiapp.py

You can access this WSGI app by visiting http://127.0.0.1:5000/.

If you want to allow access to your public IPs, or specify port:

.. code:: python

  skitai.run (
    address = "0.0.0.0",
    port = 5000,
    mount = [('/', __file__)]
  )

if you want to change number of threads for WSGI app:

.. code:: python

  skitai.run (
    threads = 4,
    mount = [('/', __file__)]
  )


Mount Multiple WSGI Apps And Static Directories
------------------------------------------------

Here's three WSGI app samples:

.. code:: python
  
  #WSGI App

  def app (env, start_response):
    start_response ("200 OK", [("Content-Type", "text/plain")])
    return ['Hello World']
    
  app.use_reloader = True
  app.debug = True


  # Flask App*
  from flask import Flask  
  app2 = Flask(__name__)  
  
  app2.use_reloader = True
  app2.debug = True
  
  @app2.route("/")
  def index ():	 
    return "Hello World"


  # Skito-Saddle App  
  from skitai.saddle import Saddle  
  app3 = Saddle (__name__)
  
  app3.use_reloader = True
  app3.debug = True
    
  @app3.route('/')
  def index (was):	 
    return "Hello World"


Then place this code at bottom of above WSGI app.

.. code:: python
  
  if __name__ == "__main__": 
  
    import skitai
    
    skitai.run (
      mount = [
        ('/', (__file__, 'app')), # mount WSGI app
        ('/flask', (__file__, 'app2')), # mount Flask app
        ('/skitai', (__file__, 'app3')), # mount Skitai app
        ('/', '/var/www/test/static') # mount static directory
      ]
    )

Enabling Proxy Server
------------------------

.. code:: python

  skitai.run (
    mount = [('/', __file__)],
    proxy = True
  )

Run as HTTPS Server
------------------------

To genrate self-signed certification file:

.. code:: python

    openssl req -new -newkey rsa:2048 -x509 -keyout server.pem -out server.pem -days 365 -nodes


.. code:: python

  skitai.run (
    mount = [('/', __file__)],
    certfile = '/var/www/certs/server.pem' # combined certification with private key
    passphrase = 'your pass phrase'
  )


About Mount Point & App Routing
--------------------------------

If app is mounted to '/flaskapp',

.. code:: python
   
  from flask import Flask    
  app = Flask (__name__)       
  
  @app.route ("/hello")
  def hello ():
    return "Hello"

Above /hello can called, http://127.0.0.1:5000/flaskapp/hello

Also app should can handle mount point. 
In case Flask, it seems 'url_for' generate url by joining with env["SCRIPT_NAME"] and route point, so it's not problem. Skito-Saddle can handle obiously. But I don't know other WSGI containers will work properly.



Concept of Skitai 'was' Services
====================================

'was' means (Skitai) *WSGI Application Support*. 

WSGI container like Flask, need to import 'was':

.. code:: python

  from skitai import was
  
  @app.route ("/")
  def hello ():
    was.get ("http://...")
    ...    

But Saddle WSGI container integrated with Skitai, use just like Python 'self'.

It will be easy to understand think like that:

- Skitai is Python class instance
- 'was' is 'self' which first argument of instance method
- Your app functions are methods of Skitai instance

.. code:: python
  
  @app.route ("/")
  def hello (was, name = "Hans Roh"):
    was.get ("http://...")
    ...

Simply just remember, if you use WSGI container like Flask, Bottle, ... - NOT Saddle - and want to use Skitai asynchronous services, you should import 'was'. Usage is exactly same. But for my convinient, I wrote example codes Saddle version mostly.

OK, let's move on.

Skitai is not just WSGI Web Server but *Micro WSGI Application Server* provides some powerful asynchronous networking (HTTP, SMTP, DNS) and database (PostgreSQL, SQLite3) connecting services.

The reason why Skitai provides these services on server level: 

- I think application server should provide at least efficient network/database handling methods, connection pool and its result caching management, because of only server object has homeostasis to do these things over your app.
- Asynchronous request handling have significant benefits compared to synchronous one

What's the benefit? Let's see synchronous code first.

.. code:: python

  import xmlrpclib
  
  @app.route ("/req")
  def req (was):
    [Job A]
    
    [CREATE REQUEST]
    s = xmlrpclib.Server ("https://pypi.python.org/pypi", timeout = 2)
    result = s.package_releases('roundup')	  
    [BLOCKED WAIT MAX 2 seconds from CREATE REQUEST]
	    
    for a, b in result:
      [Job B with result]
	  
    [Job C]
	  
    content = [Content Generating]
	  
    return content

[Job C] is delayed by [BLOCKED WAIT] by maxium 2 sec.

But asynchronous version is:

.. code:: python

  @app.route ("/req")
  def req (was):
    [CREATE REQUEST]
    s = was.rpc ("https://pypi.python.org/pypi")
    s.package_releases('roundup')
	  
    [Job A]
    [Job C]
    
    result = s.getwait (2)
    [BLOCKED WAIT MAX 2 seconds from CREATE REQUEST]
    for a, b in result:
      [Job B with result]
	  	
    content = [Content Generating]
	  
    return content

There's also [BLOCKED WAIT], but actually RPC request is processed backgound with [Job A & C]. It's same waiting max 2 sec for request, but [Job A & C] is already done in asynchronous version.

If it is possible to put usage of result more backward, asynchoronous benefit will be maximized.

.. code:: python

  @app.route ("/req")
  def req (was):      
    s = was.rpc ("https://pypi.python.org/pypi")
    s.package_releases('roundup')
	  
    [Job A]
    [Job C]
    
    content = [
      Content Generating within Template Engine
      [Generating Job A]
      {% result = s.getwait (2) %}
      {% for a, b in result %}
        [Job B with result]
      {% endfor %}
      [Generating Job B]
    ]
    return content

In 2 seconds (which should possibly wait at the worst situation in synchronous version), [Job A & C] and [Generating Job A] is processed parallelly in asynchronous environment.

There's same problem with database related jobs, so Skitai also provides *asynchronous PostgreSQL connection*. 

But it's not done yet. More benefitial situation is this one.

First, blocking version,

.. code:: python

  import xmlrpclib
  import odbc
  import urllib
  
  @app.route ("/req")
  def req (was):
    s = xmlrpclib.Server ("https://pypi.python.org/pypi", timeout = 2)
    result1 = s.package_releases('roundup')
    
    result2 = urllib.urlopen ("https://pypi.python.org/", timeout = 2)
    
    dbc = odbc.odbc ("127.0.0.1", timeout = 2)
    c = dbc.cursor ()
    c.execute ("select ...")
    result3 = c.fetchall ()	    
    
    content = [Content Generating]
	  
    return content

Actually, all connection doesn't have timeout arg, Anyway above 3 requests will be possibly delayed max '6' seconds.

Now async version is,

.. code:: python

  @app.route ("/req")
  def req (was):
    s1 = was.rpc ("https://pypi.python.org/pypi")
    s1.package_releases('roundup')
    
    s2 = was.get ("https://pypi.python.org/")
    
    s3 = was.db ("127.0.0.1").do ("select ...")
    
    result1 = s1.getwait (2)
    result2 = s2.getwait (2)
    result3 = s3.getwait (2)
    	
    content = [Content Generating]
	  
    return content

Above async version will be possibly delayed max '2' seconds, because waiting-start point is the time request was created and 3 requests was created almost same time and processed parallelly in background.

It can be implemeted by using multi-threading, but Skitai handles all sockets in single threaded non-blocking multi-plexing loop, there's no additional cost for threads creation/context switching etc.

Even better, Skitai manages connection pool for all connections, doesn't need connect operation except at first request at most cases.

Of cause, if use callback mechanism traditionally used for async call like AJAX, it would be more faster, but it's not easy to maintain codes, possibliy will be created 'callback-heaven'. Skitai 'was' service is a compromise between Async and Sync (Blocking and Non-Blocking).

So next two chapters are 'HTTP/XMLRPC Request' and 'Connecting to DBMS'.

Bottom line, the best coding strategy with Skitai is, *"Request Early, Use Lately"*.



REST API / XMLRPC / Websocket Request
=======================================

Usage
------

**Simple HTTP Request**

*Flask Style:*

.. code:: python

  from flask import Flask, request
  from skitai import was
  
  app = Flask (__name__)        
  @app.route ("/get")
  def get ():
    url = request.args.get('url', 'http://www.python.org')
    s = was.get (url)
    result = s.getwait (5) # timeout
    if result.is_normal () and result.code == 200:
      return result.data
    else:
      result.reraise ()


*Skito-Saddle Style*

.. code:: python

  from skitai.saddle import Saddle
  app = Saddle (__name__)
        
  @app.route ("/get")
  def get (was, url = "http://www.python.org"):
    s = was.get (url)
    result = s.getwait (5) # timeout
    if result.is_normal () and result.code == 200:
      return result.data
    else:
      result.reraise ()

Both can access to http://127.0.0.1:5000/get?url=https%3A//pypi.python.org/pypi .

If you are familar to Flask then use it, otherwise choose any WSGI container you like include Skito-Saddle.

Again note that if you want to use WAS services in your WSGI containers (not Skito-Saddle), you should import was.

.. code:: python

  from skitai import was

And result.is_normal () must be checked.

if status is not result.is_normal (), you should handle error by calling result.reraise (), result.get_error (), ignoring or returning alternative content etc. For my convinient, it will be skipped in example codes from now.


Here're post and file upload method examples:

.. code:: python

  s1 = was.post (url, {"user": "Hans Roh", "comment": "Hello"})
  s2 = was.upload (url, {"user": "Hans Roh", "file": open (r"logo.png", "rb")})
  
  result = s1.getwait (2)
  result = s2.getwait (2)

It is important to know that if post/put method's dictionary type data is automatically dumped to json. If you want to post/put www form data, use postform/putform method or add Content-Type header "application/x-www-form-urlencoded". Also in case all the other content types, data should be string or bytes type, and need Content-Type header.

.. code:: python

  s = was.post (
  	url, 
  	{"user": "Hans Roh", "comment": "Hello"}, 
  	headers = {"content-Type", "application/x-www-form-urlencoded"}
  )
  
  # This is exactly same as:
    
  s = was.postform (
  	url, 
  	{"user": "Hans Roh", "comment": "Hello"}  	
  )

Another aliases are postxml, putxml (text/xml), postnvp, putnvp (text/namevalue).

Here's XMLRPC request for example:

.. code:: python

  s = was.rpc (url)
  s.get_prime_number_gt (10000)
  result = s.getwait (2)

Please note XMLRPC method name shouldn't be any of wait, getwait, getswait or cache.  

For requesting with basic/digest authorization:

.. code:: python

  s = was.rpc (url, auth = (username, password))
  s.get_prime_number_gt (10000)
  result = s.getwait (2)


Avaliable methods are:

- was.get (url, data = None, auth = (username, password), headers = [(name, value), ...] or {name: value}, use_cache = True)
- was.post (url, data, auth, headers, use_cache)
- was.rpc (url, data, auth, headers, use_cache) # XMLRPC
- was.ws (url, data, auth, headers, use_cache) # Web Socket
- was.put (url, data, auth, headers, use_cache)
- was.delete (url, data, auth, headers, use_cache)
- was.upload (url, data, auth, headers, use_cache) # For clarity to multipart POST

Above methods return ClusterDistCall (cdc) class.

*Changed in version 0.15.24* 

add reraise arg to cdc.getwait (timeout = 5, reraise = False) 
 
- cdc.getwait (timeout = 5, reraise = False) : return result with status, if reraise is True, raise immediately when error occured    
- cdc.getswait (timeout = 5, reraise = False) : getting multiple results
- cdc.wait (timeout = 5, reraise = True) : no return result just wait until query finished.maybe useful for executing create, update and delete queury

The result returned from cdc.getwait(), getswait ():

- result.code: HTTP status code like 200, 404, ...
- result.msg: HTTP status message
- result.data
- result.status

  - 0: Initial Default Value
  - 1: Operation Timeout
  - 2: Exception Occured
  - 3: Normal

- result.get_status ()
- result.is_normal (): return result.status == 3
- result.reraise ()
- result.get_data ()
- result.get_error ()
- result.cache (timeout)


**Load-Balancing**

If server members are pre defined, skitai choose one automatically per each request supporting *fail-over*.

At first, let's add mysearch members to config file (ex. /etc/skitaid/servers-enabled/sample.conf),

.. code:: python

  [@mysearch]
  ssl = yes
  members = search1.mayserver.com:443, search2.mayserver.com:443
    

Then let's request XMLRPC result to one of mysearch members.
   
.. code:: python

  @app.route ("/search")
  def search (was, keyword = "Mozart"):
    s = was.rpc.lb ("@mysearch/rpc2")
    s.search (keyword)
    results = s.getwait (5)
    return result.data

It just small change from was.rpc () to was.rpc.lb ()

Avaliable methods are:

- was.get.lb ()
- was.post.lb ()
- was.rpc.lb ()
- was.ws.lb ()
- was.upload.lb ()
- was.put.lb ()
- was.delete.lb ()


*Note:* If @mysearch member is only one, was.get.lb ("@mydb") is equal to was.get ("@mydb").

*Note2:* You can mount cluster @mysearch to specific path as proxypass like this:

At config file

.. code:: python
  
  [routes:line]  
  ; for files like images, css
  / = /var/wsgi/static
  
  ; app mount syntax is path/module:callable
  /search = @mysearch  
  
It can be accessed from http://127.0.0.1:5000/search, and handled as load-balanced proxypass.

  

**Map-Reducing**

Basically same with load_balancing except Skitai requests to all members per each request.

.. code:: python

    @app.route ("/search")
    def search (was, keyword = "Mozart"):
      s = was.rpc.map ("@mysearch/rpc2")
      s.search (keyword)
      results = s.getswait (2)
			
      all_results = []
      for result in results:
         all_results.extend (result.data)
      return all_results

There are 2 changes:

1. from was.rpc.lb () to was.rpc.map ()
2. form s.getwait () to s.getswait () for multiple results

Avaliable methods are:

- was.get.map ()
- was.post.map ()
- was.rpc.map ()
- was.ws.map ()
- was.upload.map ()
- was.put.map ()
- was.delete.map ()


**HTML5 Websocket Request**

*New in version 0.11*

There're 3 Skitai 'was' client-side web socket services:

- was.ws ()
- was.ws.lb ()
- was.ws.map ()

It is desinged as simple & no stateless request-response model using web socket message frame for *light overheaded server-to-server communication*. For example, if your web server queries to so many other search servers via RESTful access, web socket might be a good alterative option. Think HTTP-Headerless JSON messaging. Usage is very simailar with HTTP request.

.. code:: python

  @app.route ("/query")
  def query (was):
    s = was.ws (
    	"ws://192.168.1.100:5000/websocket/echo", 
    	was.tojson ({"keyword": "snowboard binding"})
    )
    rs = s.getwait ()
    result = was.fromjson (rs.data)

Usage is same as HTTP/RPC request and obiously, target server should be implemented websocket service routed to '/websocket/echo' in this case.


Caching Result
----------------

Every results returned by getwait(), getswait() can cache.

.. code:: python

  s = was.rpc.lb ("@mysearch/rpc2")
  result = s.getwait (2)
  if result.code == 200:
  	result.cache (60) # 60 seconds
  
  s = was.rpc.map ("@mysearch/rpc2")
  results = s.getswait (2)
  # assume @mysearch has 3 members
  if results.code == [200, 200, 200]:    
    result.cache (60)

Although code == 200 alredy implies status == 3, anyway if status is not 3, cache() will be ignored. If cached, it wil return cached result for 60 seconds.

*New in version 0.15.28*

If you getwait with reraise argument, code can be simple.

.. code:: python

  s = was.rpc.lb ("@mysearch/rpc2")
  content = s.getswait (2, reraise = True).data
  s.cache (60)

Please remember cache () method is both available request and result objects.


For expiring cached result by updating new data:

*New in version 0.14.9*

.. code:: python
  
  refreshed = False
  if was.request.command == "post":
    ...
    refreshed = True
  
  s = was.rpc.lb ("@mysearch/rpc2", use_cache = not refreshed and True or False)
  result = s.getwait (2)
  if result.code == 200:
  	result.cache (60) # 60 seconds  
    

Connecting to DBMS
=====================

Of cause, you can use any database modules for connecting to your DBMS.

Skitai also provides asynchonous PostgreSQL query services for efficient developing and getting advantages of asynchronous server framework by using Psycopg2.

But according to `Psycopg2 advanced topics`_, there are several limitations in using asynchronous connections:

  The connection is always in autocommit mode and it is not possible to change it. So a transaction is not implicitly started at the first query and is not possible to use methods commit() and rollback(): you can manually control transactions using execute() to send database commands such as BEGIN, COMMIT and ROLLBACK. Similarly set_session() can't be used but it is still possible to invoke the SET command with the proper default_transaction.. parameter.

  With asynchronous connections it is also not possible to use set_client_encoding(), executemany(), large objects, named cursors.

  COPY commands are not supported either in asynchronous mode, but this will be probably implemented in a future release.
  
  
If you need blocking jobs, you can use original Psycopg2 module or other PostgreSQL modules.

Anyway, usage is basically same concept with above HTTP Requests.


PostgreSQL
------------

**Simple Query**

.. code:: python

    s = was.db ("127.0.0.1:5432", "mydb", "user", "password")
    s.do ("SELECT city, t_high, t_low FROM weather;")
    result = s.getwait (2)
    
    for row in result.data:
      row.city, row.t_high, row.t_low


*New in version 0.15.15*

result.data was dictionary list but now also can access value via attributes.


**Load-Balancing**

This sample is to show querying sharded database.
Add mydb members to config file.

.. code:: python

    [@mydb]
    type = postresql
    members = s1.yourserver.com:5432/mydb/user/passwd, s2.yourserver.com:5432/mydb/user/passwd

    @app.route ("/query")
    def query (was, keyword):
      s = was.db.lb ("@mydb").do("INSERT INTO CITIES VALUES ('New York');")
      s.wait (2) # no return, just wait for completing query, if failed exception will be raised
      
      s = was.db.lb ("@mydb").do("SELECT * FROM CITIES;")
      result = s.getwait (2)
   
	
**Map-Reducing**

.. code:: python

    @app.route ("/query")
    def query (was, keyword):
      s = was.db.map ("@mydb").do("SELECT * FROM CITIES;")
      results = s.getswait (2)
      all_results = []
      for result in results:
        if result.is_normal ():
          all_results.append (result.data)
      return all_results


Avaliable methods are:

- was.db (server, dbname, user, password, dbtype = "postgresql", use_cache = True)
- was.db.lb (server, dbname, user, password, dbtype = "postgresql", use_cache = True)
- was.db.map (server, dbname, user, password, dbtype = "postgresql", use_cache = True)
- was.db ("@mydb", use_cache = True)
- was.db.lb ("@mydb", use_cache = True)
- was.db.map ("@mydb", use_cache = True)

*Note:* if @mydb member is only one, was.db.lb ("@mydb") is equal to was.db ("@mydb").

*Note 2:* You should call exalctly single do () per a was.db.* () object.


.. _`Psycopg2 advanced topics`: http://initd.org/psycopg/docs/advanced.html


Redis
--------

`New in version 0.20.5`

Redis_ is an open source, in-memory data structure store, used as a database, cache and message broker.

Skitai provides asynchronous connection to Redis server with connection pool. Usage is almost same with PostgreSQL.

.. code:: python

  from skitai import DB_REDIS
  
  @app.route ("/redis")
  def redis (was):
    s = was.db ("127.0.0.1:6379", DB_REDIS).do ("SET", "maykey1", "Hans Roh")	
    rs = s.getwait (5)
    return rs.data [0].value

You can alias to your Redis server at tour configuration file:

.. code:: bash

  [@myredis]
  type = redis
  members = s1.yourserver.com:6379

So you can use more easily.

.. code:: python
  
  @app.route ("/redis")
  def redis (was):
    s1 = was.db.map ("@myredis").do ("SET", "maykey1", "Hans Roh")	
    s2 = was.db ("@myredis").do ("GET", "maykey1")
    s3 = was.db.map ("@myredis").do ("RPUSH", "maykey2", "hello")
    s4 = was.db.map ("@myredis").do ("RPUSH", "maykey2", "world")
    s5 = was.db.lb ("@myredis").do ("LRANGE", "maykey2", 0, -1)
    s6 = was.db.map ("@myredis").do ("SAVE")
    
    buf = []
    for s in (s1, s2, s3, s4, s5, s6):
      rs = s.getwait (5)
      if rs.is_normal ():
        buf.append (str (rs.data [0].value))
      else:
        buf.append (rs.get_error ())
        
    return "<hr>".join (buf)
    

.. _Redis: https://redis.io/


SQLite3 For Fast App Prototyping
------------------------------------

`New in version 0.13`

Skitai provide SQLite3 query API service for fast app prototyping. 

Usage is almost same with PostgreSQL. This service IS NOT asynchronous BUT just emulating.

.. code:: python

    from skitai import DB_SQLITE3
    
    s = was.db ("sqlite3.db", DB_SQLITE3)
    s.do ("""
      drop table if exists people;
      create table people (name_last, age);
      insert into people values ('Cho', 42);
    """)
    # result is not needed use wait(), and if failed, excpetion will be raised
    s.wait (5)

    s = was.db ("sqlite3.db", DB_SQLITE3).do ("select * from people;")    
    result = s.getwait (2)

Also load-balacing and map-reuducing is exactly same with PostgreSQL.

.. code:: python

    [@mysqlite3]
    type = sqlite3
    members = /tmp/sqlite1.db, /tmp/sqlite2.db


*Note:* You should call exalctly 1 execute () per a was.db.* () object, and 'select' statement should be called alone.


Caching Result
------------------

Same as HTTP/RPC, every results returned by getwait(), getswait() can cache.

.. code:: python

  s = was.db.lb ("@mydb").do ("select ...")
  result = s.getwait (2)
  result.cache (60)
  
  s = was.db.map ("@mydb").do ("select ...")
  results = s.getswait (2)
  result.cache (60)
  
If result or one of results has status != 3, cache() will be ignored.

*New in version 0.15.28*

If you getwait with reraise argument, code can be simple.

.. code:: python

  s = was.db ("@mydb")
  for row in s.getswait (2, reraise = True).data:
    ...
  s.cache (60)

Please remember cache () method is both available DB query request and result objects.

For expiring cached result by updating new data:

*New in version 0.14.9*

.. code:: python
  
  has_new_data = False
  if was.request.command == "post":
    ...
    has_new_data = True
  
  s = was.db.lb ("@mydb", use_cache = not has_new_data and True or False)
  s.do ("select ...")
  result = s.getwait (2)
  result.cache (60)
  	

Other Utility Service of 'was'
=================================

This chapter's 'was' services are also avaliable for all WSGI middelwares.

- was.status () # HTML formatted status information like phpinfo() in PHP.
- was.tojson (object)
- was.fromjson (string)
- was.toxml (object) # XMLRPC
- was.fromxml (string) # XMLRPC
- was.restart () # Restart Skitai App Engine Server, but this only works when processes is 1 else just applied to current worker process.
- was.shutdown () # Shutdown Skitai App Engine Server, but this only works when processes is 1 else just applied to current worker process.



HTTP/2.0
============

*New in version 0.16*

Skiai supports HTPT2 both 'h2' protocl over encrypted TLS and 'h2c' for clear text (But now Sep 2016, there is no browser supporting h2c protocol).

Basically you have nothing to do for HTTP2. Client's browser will handle it except `HTTP2 server push`_.

For using it, you just call was.response.hint_promise (uri) before return response data. It will work only client browser support HTTP2, otherwise will be ignored.

.. code:: python

  @app.route ("/promise")
  def promise (was):
  
    was.response.hint_promise ('/images/A.png')
    was.response.hint_promise ('/images/B.png')
    
    return was.response ("200 OK", 'Promise Sent<br><br><img src="/images/A.png"><img src="/images/B.png">')	


.. _`HTTP2 server push`: https://tools.ietf.org/html/rfc7540#section-8.2


HTML5 Websocket
====================

*New in version 0.11*

The HTML5 WebSockets specification defines an API that enables web pages to use the WebSockets protocol for two-way communication with a remote host.

Skitai can be HTML5 websocket server and any WSGI containers can use it.

But I'm not sure my implemetation is right way, so it is experimental and could be changable.

I think there're 3 handling ways to use websockets.

1. thread pool manages n websocket connection

2. one thread per websocket connection

3. one thread manages n websockets connection

So skitai supports above all 3 ways.

First of all, see conceptual client side java script for websocket.

.. code:: html
  
  <body>
  <ul id="display"></ul>
  <input id="mymsg" type="text">
  <button onclick='talk ();'>Submit<button>
  
  <script language="javascript" type="text/javascript">  
  var wsUri = "ws://localhost:5000/websocket/chat";
  testWebSocket();
  
  function testWebSocket()
  {
    websocket = new WebSocket(wsUri);
    websocket.onopen = function(evt) { onOpen(evt) };
    websocket.onclose = function(evt) { onClose(evt) };
    websocket.onmessage = function(evt) { onMessage(evt) };
    websocket.onerror = function(evt) { onError(evt) };
  }
  
  function onOpen(evt) {doSend("Hello");}
  function onClose(evt) {log_info ("DISCONNECTED");}  
  function onMessage(evt) {log_info('evt.data');}
  function onError(evt) {log_info('ERROR: ' + evt.data));}  
  function doClose () {websocket.close();}  
  function doSend(message) {
  	log_info('SENT: ' + message));
  	websocket.send(message);
  }
  function talk () {
    doSend ($("#mymsg").val());
    $("#mymsg").val("");
  }
  function log_info (message) {
   $('<li>' + message + '</li>').appendTo ("#display");
  }    
  </script>  
  </body>


If your WSGI app enable handle websocket, it should give  initial parameters to Skitai.

You should check exist of env ["websocket_init"], set initializing parameters.

initializing parameters should be tuple of (websocket design spec, keep alive timeout, variable name)

*websocket design specs* can  be choosen one of 3 .

WEBSOCKET_REQDATA

  - Thread pool manages n websocket connection
  - It's simple request and response way like AJAX
  - Use skitai initail thread pool, no additional thread created
  - Low cost on threads resources, but reposne cost is relatvley high than the others
  
WEBSOCKET_DEDICATE

  - One thread per websocket connection
  - Use when interactives takes long time like websocket version telnet or subprocess stdout streaming
  - New thread created per websocket connection
 
WEBSOCKET_DEDICATE_THREADSAFE

  - Thread safe version of WEBSOCKET_DEDICATE
  - Multiple threads can call websocket.send (msg)
 
WEBSOCKET_MULTICAST
  
  - One thread manages n websockets connection
  - Chat room model, all websockets will be managed by single thread
  - New thread created per chat room

*keep alive timeout* is seconds.

*variable name* is various usage per each design spec.


Simple Data Request & Response
-------------------------------

Here's a echo app for showing simple request-respone.

Client can connect by ws://localhost:5000/websocket/chat.

*Skito-Saddle Style*

.. code:: python

  from skitai.saddle import Saddle
  import skitai
  
  app = Saddle (__name__)
  app.debug = True
  app.use_reloader = True

  @app.route ("/websocket/echo")
  def echo (was, message = ""):
    if "websocket_init" in was.env:
      was.env ["websocket_init"] = (skitai.WEBSOCKET_REQDATA, 60, "message")
      return ""
    return "ECHO:" + message

*Flask Style*

.. code:: python

  from flask import Flask, request 
  import skitai
  
  app = Flask (__name__)
  app.debug = True
  app.use_reloader = True

  @app.route ("/websocket/echo")
  def echo ():
    if "websocket_init" in request.environ:
      request.environ ["websocket_init"] = (skitai.WEBSOCKET_REQDATA, 60, "message")
      return ""
    return "ECHO:" + request.args.get ("message")

In this case, variable name is "message", It means take websocket's message as "message" arg.

Dedicated Websocket
-----------------------

This app will handle only one websocket client. and if new websocekt connected, will be created new thread.

Client can connect by ws://localhost:5000/websocket/talk?name=Member.

.. code:: python

  @app.route ("/websocket/talk")
  def talk (was, name):
    if "websocket_init" in was.env:
      was.env ["websocket_init"] = (skitai.WEBSOCKET_DEDICATE, 60, None)
      return ""
    
    ws = was.env ["websocket"]
    while 1:
      messages = ws.getswait (10)
      if messages is None:
        break  
      for m in messages:
        if m.lower () == "bye":
          ws.send ("Bye, have a nice day." + m)
          ws.close ()
          break
        elif m.lower () == "hello":
          ws.send ("Hello, " + name)        
        else:  
          ws.send ("You Said:" + m)

In this case, variable name should be None. If exists, will be ignored.

Threadsafe-Dedicated Websocket
-------------------------------

This app will handle only one websocket client. and if new websocekt connected, will be created new thread.

Also you can new threads in your function which use websocket.send ().

.. code:: python
  
  def calculate (ws, id, count):
    p = Popen (
      [sys.executable, r'calucate.py', '-c', count],
      universal_newlines=True,
      stdout=PIPE, shell = False
    )    
    for line in iter(p.stdout.readline, ''):	 
      self.ws.send (line)	
    p.stdout.close ()
  
  @app.route ("/websocket/calculate")
  def calculate (was):
    if "websocket_init" in was.env:
      was.env ["websocket_init"] = (skitai.WEBSOCKET_DEDICATE_THREADSAFE, 60, None)
      return ""
    
    workers = 0
    ws = was.env ["websocket"]
    while 1:
      messages = ws.getswait (10)
      if messages is None:
        break 
      for m in messages:
        if m.lower () == "bye":
          ws.send ("Bye, have a nice day." + m)
          ws.close ()
          break
        elif m.lower () == "run":
          threading.Thread (target = calculate, args = (ws, workers, m[3:].strip ()).start ()
          workers +=1
        else:  
          ws.send ("You said %s but I can't understatnd" % m)

In this case, variable name should be None. If exists, will be ignored.


Multicasting Websocket
------------------------

Here's simple mutiuser chatting app.

Many clients can connect by ws://localhost:5000/websocket/chat?roomid=1. and can chat between all clients.

.. code:: python

  @app.route ("/websocket/chat")
  def chat (was, roomid):
    if "websocket_init" in was.env:
      was.env ["websocket_init"] = (skitai.WEBSOCKET_MULTICAST, 60, "roomid")
      return ""
    
    ws = was.env ["websocket"]  
    while 1:
      messages = ws.getswait (10)
      if messages is None:
        break  
      for client_id, m in messages:
        ws.sendall ("Client %d Said: %s" % (client_id, m))

In this case, variable name is "roomid", then Skitai will create websocket group seperatly by roomid value.


You can access all examples by skitai sample app after installing skitai.

.. code:: python

  sudo skitaid-instance.py -v -f sample

Then goto http://localhost:5000/websocket in your browser.

In next chapter's features of 'was' are only available for *Skito-Saddle WSGI container*. So if you have no plan to use Saddle, just skip.



Request Handling with Skito-Saddle
====================================

*Saddle* is WSGI container integrated with Skitai App Engine.

Flask and other WSGI container have their own way to handle request. So If you choose them, see their documentation.

And note below objects and methods *ARE NOT WORKING* in any other WSGI containers except Saddle.


Access Saddle App
------------------

You can access all Saddle object from was.app.

- was.app.debug
- was.app.use_reloader
- was.app.config # use for custom configuration like was.app.config.my_setting = 1

- was.app.securekey
- was.app.session_timeout = None	

- was.app.authorization = "digest"
- was.app.authenticate = False
- was.app.realm = None
- was.app.users = {}
- was.app.jinja_env

- was.app.build_url () is equal to was.ab ()

Currently was.app.config has these properties and you can reconfig by setting new value:

- was.app.config.max_post_body_size = 5 * 1024 * 1024
- was.app.config.max_cache_size = 5 * 1024 * 1024
- was.app.config.max_multipart_body_size = 20 * 1024 * 1024
- was.app.config.max_upload_file_size = 20000000


Debugging and Reloading App
-----------------------------

If debug is True, all errors even server errors is shown on both web browser and console window, otherhwise shown only on console.

If use_reloader is True, Skito-Saddle will detect file changes and reload app automatically, otherwise app will never be reloaded.

.. code:: python

  from skitai.saddle import Saddle
  
  app = Saddle (__name__)
  app.debug = True # output exception information
  app.use_reloader = True # auto realod on file changed
  

Routing
--------

Basic routing is like this:

.. code:: python
	
  @app.route ("/hello")
  def hello_world (was):	
    return was.render ("hello.htm")

For adding some restrictions:

.. code:: python
	
  @app.route ("/hello", methods = ["GET"], content_types = ["text/xml"])
  def hello_world (was):	
    return was.render ("hello.htm")

If method is not GET, Saddle will response http error code 405 (Method Not Allowed), and content-type is not text/xml, 415 (Unsupported Content Type).
    
  
Access Request
----------------

Reqeust object provides these methods and attributes:

- was.request.command # lower case get, post, put, ...
- was.request.version # HTTP Version, 1.0, 1.1
- was.request.uri
- was.request.args # dictionary contains url/form parameters
- was.request.split_uri () # (script, param, querystring, fragment)
- was.request.get_header ("content-type") # case insensitive
- was.request.get_headers () # retrun header all list
- was.request.get_body ()
- was.request.get_scheme () # http or https
- was.request.get_remote_addr ()
- was.request.get_user_agent ()
- was.request.get_content_type ()
- was.request.get_main_type ()
- was.request.get_sub_type ()


Response
-------------

Basically, just return contents.

.. code:: python
	
  @app.route ("/hello")
  def hello_world (was):	
    return was.render ("hello.htm")

If you need set additional headers or HTTP status,
    
.. code:: python
  
  @app.route ("/hello")
  def hello (was):	
    return was.response ("200 OK", was.render ("hello.htm"), [("Cache-Control", "max-age=60")])

  def hello (was):	
    return was.response (body = was.render ("hello.htm"), headers = [("Cache-Control", "max-age=60")])

  def hello (was):	       
    was.response.set_header ("Cache-Control", "max-age=60")
    return was.render ("hello.htm")

Above 3 examples will make exacltly same result.

Sending specific HTTP status code,

.. code:: python
  
  def hello (was):	
    return was.response ("404 Not Found", was.render ("err404.htm"))
  
  def hello (was):
    # if body is not given, automaticcally generated with default error template.
    return was.response ("404 Not Found")

If app raise exception, traceback information will be displayed only app.debug = True. But you intentionally send it inspite of app.debug = False:

.. code:: python
  
  # File
  @app.route ("/raise_exception")
  def raise_exception (was):	
    try:
    	raise ValueError ("Test Error")
    except:    	
    	return was.response ("500 Internal Server Error", exc_info = sys.exc_info ())
    
You can return various objects.

.. code:: python
  
  # File
  @app.route ("/streaming")
  def streaming (was):	
    return was.response ("200 OK", open ("mypicnic.mp4", "rb"), headers = [("Content-Type", "video/mp4")])
  
  # Generator
  def build_csv (was):	
    def generate():
      for row in iter_all_rows():
        yield ','.join(row) + '\n'
    return was.response ("200 OK", generate (), headers = [("Content-Type", "text/csv")])   
    

All available return types are:

- String, Bytes, Unicode
- File-like object has 'read (buffer_size)' method, optional 'close ()'
- Iterator/Generator object has 'next() or _next()' method, optional 'close ()' and shoud raise StopIteration if no more data exists.
- Something object has 'more()' method, optional 'close ()'
- Classes of skitai.lib.producers
- List/Tuple contains above objects
- XMLRPC dumpable object for if you want to response to XMLRPC

The object has 'close ()' method, will be called when all data consumed, or socket is disconnected with client by any reasons.

- was.response (status = "200 OK", body = None, headers = None, exc_info = None)
- was.response.set_status (status) # "200 OK", "404 Not Found"
- was.response.get_status ()
- was.response.set_headers (headers) # [(key, value), ...]
- was.response.get_headers ()
- was.response.set_header (k, v)
- was.response.get_header (k)
- was.response.del_header (k)
- was.response.hint_promise (uri) # *New in version 0.16.4*, only works with HTTP/2.x and will be ignored HTTP/1.x


Getting URL Parameters
-------------------------

.. code:: python
  
  @app.route ("/hello")
  def hello_world (was, num = 8):
    return num
  # http://127.0.0.1:5000/hello?num=100	
	
  @app.route ("/hello/<int:num>")
  def hello_world (was, num = 8):
    return str (num)
    # http://127.0.0.1:5000/hello/100


Also you can access as dictionary object 'was.request.args'.

.. code:: python

  num = was.request.args.get ("num", 0)


for fancy url building, available param types are:

- int
- float
- path: /download/<int:major_ver>/<path>, should be positioned at last like /download/1/version/1.1/win32
- If not provided, assume as string. and all space char replaced to "_'


Getting Form Parameters
----------------------------

Getting form is not different from the way for url parameters, but generally form parameters is too many to use with each function parameters, can take from single args \*\*form or take mixed with named args and \*\*form both.

.. code:: python

  @app.route ("/hello")
  def hello (was, **form):  	
  	return "Post %s %s" % (form.get ("userid", ""), form.get ("comment", ""))
  	
  @app.route ("/hello")
  def hello_world (was, userid, **form):
  	return "Post %s %s" % (userid, form.get ("comment", ""))


Building URL
---------------

If your app is mounted at "/math",

.. code:: python

  @app.route ("/add")
  def add (was, num1, num2):  
    return int (num1) + int (num2)
    
  was.app.build_url ("add", 10, 40) # returned '/math/add?num1=10&num2=40'
  
  # BUT it's too long to use practically,
  # was.ab is acronym for was.app.build_url
  was.ab ("add", 10, 40) # returned '/math/add?num1=10&num2=40'
  was.ab ("add", 10, num2=60) # returned '/math/add?num1=10&num2=60'
  
  @app.route ("/hello/<name>")
  def hello (was, name = "Hans Roh"):
    return "Hello, %s" % name
	
  was.ab ("hello", "Your Name") # returned '/math/hello/Your_Name'
 

Access Environment Variables
------------------------------

was.env is just Python dictionary object.

.. code:: python

  if "HTTP_USER_AGENT" in was.env:
    ...
  was.env.get ("CONTENT_TYPE")


Jinja2 Templates Engine
--------------------------

Although You can use any template engine, Skitai provides was.render() which uses Jinja2_ template engine. For providing arguments to Jinja2, use dictionary or keyword arguments.

.. code:: python
  
  return was.render ("index.html", choice = 2, product = "Apples")
  
  #is same with:
  
  return was.render ("index.html", {"choice": 2, "product": "Apples"})
  
  #BUT CAN'T:
  
  return was.render ("index.html", {"choice": 2}, product = "Apples")


Directory structure sould be:

- /project_home/app.py
- /project_home/templates/index.html


At template, you can use all 'was' objects anywhere defautly. Especially, Url/Form parameters also can be accessed via 'was.request.args'.

.. code:: html
  
  {{ was.cookie.username }} choices item {{ was.request.args.get ("choice", "N/A") }}.
  
  <a href="{{ was.ab ('checkout', choice) }}">Proceed</a>

Also 'was.g' is can be useful in case threr're lots of render parameters.

.. code:: python

  was.g.product = "Apple"
  was.g.howmany = 10
  
  return was.render ("index.html")

And at jinja2 template, 
  
.. code:: html
  
  {% set g = was.g }} {# make shortcut #}
  Checkout for {{ g.howmany }} {{ g.product }}{{g.howmany > 1 and "s" or ""}}
  

If you want modify Jinja2 envrionment, can through was.app.jinja_env object.

.. code:: python
  
  def generate_form_token ():
    ...
    
  was.app.jinja_env.globals['form_token'] = generate_form_token


*New in version 0.15.16*

Added new app.jinja_overlay () for easy calling app.jinja_env.overlay ().

.. code:: python

  app = Saddle (__name__)
  app.debug = True
  app.use_reloader = True
  app.jinja_overlay (
  	line_statement = "%", 
  	variable_string = "#", 
  	block_start_string = "{%", 
  	block_end_string = "}"
  )

Original Jinja2 form is:

.. code:: html
  
  {% extends "layout.htm" %}  
  {% block title %}Dash Board{% endblock %}
  
  {% for group in stat|groupby ('nation') %}
    <h1>{% block sectionname %}Population of {{group.grouper}}{% endblock %}</h1>
    {% for row in group.list  %}
      <h2>{{row.state}}</h1>
      <a href="{{ was.ab ('bp_state', row.nation, loop.index)}}">{{row.population}}</a>
      <a href="#" onclick="javascript: create_map ('{{row.state}}');">Map</a>
    {% endfor %}
  {% endfor %}

app.jinja_overlay ("%", "#", "{%", "}") changes jinja environment,

- variable_start_string = from {{ to #
- variable_end_string = from }} to #
- line_statement_prefix = from None to %
- line_comment_prefix = from None to %%
- block_start_string = unchange, keep {%
- block_end_string = from %} to }
- trim_blocks = from False to True
- lstrip_blocks = from False to True

Important note for escaping charcter '#', use '##', but this is only valid when variable_start_string and variable_end_string are same. Also escaping '%' which appears at first of line excluding space/tab:

.. code:: html

  % raw:
    %HOME%/bin
    <a href="#" onclick="javascript: create_map ();">Map</a>
  % endraw

As a result, template can be written:

.. code:: html

  % extends "layout.htm"
  % block title:
    Dash Board
  % endblock  
  
  % for group in stat|groupby ('nation'):
    <h1>{% block sectionname }Population of #group.grouper#{% endblock }</h1>
    % for row in group.list:
      <h2>#row.state#</h1>
      <a href="#was.ab ('state_view', row.nation, loop.index)#">#row.population#</a>
      <a href="##" onclick="javascript: create_map ('#row.state#');">Map</a>
    % endfor
  % endfor

If you like this style, just call 'app.jinja_overlay ()'. In my case, above template is more easy to read/write if applying proper syntax highlighting to text editor.

For more detail, `Jinja2 Line Statements and Escape`_.

*Warning*: Current Jinja2 2.8 dose not support double escaping (##) and 'raw' line_statement but it will be applied to runtime patch by Saddle. So if you use app.jinja_overlay, you have compatible problems with official Jinja2.


.. _`Jinja2 Line Statements and Escape`: http://jinja.pocoo.org/docs/dev/templates/#line-statements
.. _Jinja2: http://jinja.pocoo.org/


Access Cookie
----------------

was.cookie has almost dictionary methods.

.. code:: python

  if "user_id" not in was.cookie:
  	was.cookie.set ("user_id", "hansroh")  	
  	# or  	
  	was.cookie ["user_id"] = "hansroh"


*Changed in version 0.15.30*

'was.cookie.set()' method prototype has been changed.

.. code:: python

  was.cookie.set (
    key, val, 
    expires = None, 
    path = None, domain = None, 
    secure = False, http_only = False
  ) 

'expires' args is seconds to expire. 

 - if None, this cookie valid until browser closed
 - if 0 or 'now', expired immediately
 - if 'never', expire date will be set to a hundred years from now

If 'secure' and 'http_only' options are set to True, 'Secure' and 'HttpOnly' parameters will be added to Set-Cookie header.

If 'path' is None, every app's cookie path will be automaticaaly set to their mount point.

For example, your admin app is mounted on "/admin" in configuration file like this:

.. code:: python

  app = ... ()
  
  if __name__ == "__main__": 
  
    import skitai
    
    skitai.run (
      address = "127.0.0.1",
      port = 5000,
      mount = {'/admin': app}
    )

If you don't specify cookie path when set, cookie path will be automatically set to '/admin'. So you want to access from another apps, cookie should be set with upper path = '/'.

.. code:: python
  
  was.cookie.set ('private_cookie', val)
        
  was.cookie.set ('public_cookie', val, path = '/')
  

  	
- was.cookie.set (key, val, expires = None, path = None, domain = None, secure = False, http_only = False)
- was.cookie.remove (key, path, domain)
- was.cookie.clear (path, domain)
- was.cookie.keys ()
- was.cookie.values ()
- was.cookie.items ()
- was.cookie.has_key ()
- was.cookie.iterkyes ()
- was.cookie.itervalues ()
- was.cookie.iteritems ()


Access Session
----------------

was.session has almost dictionary methods.

To enable session for app, random string formatted securekey should be set for encrypt/decrypt session values.

*WARN*: `securekey` should be same on all skitai apps at least within a virtual hosing group, Otherwise it will be serious disaster.

.. code:: python

  app.securekey = "ds8fdsflksdjf9879dsf;?<>Asda"
  app.session_timeout = 1200 # sec
  
  @app.route ("/session")
  def hello_world (was, **form):  
    if "login" not in was.session:
      was.session.set ("user_id", form.get ("hansroh"))
      # or
      was.session ["user_id"] = form.get ("hansroh")

- was.session.set (key, val)
- was.session.get (key, default = None)
- was.session.source_verified (): If current IP address matches with last IP accesss session
- was.session.getv (key, default = None): If not source_verified (), return default
- was.session.remove (key)
- was.session.clear ()
- was.session.kyes ()
- was.session.values ()
- was.session.items ()
- was.session.has_key ()
- was.session.iterkyes ()
- was.session.itervalues ()
- was.session.iteritems ()


Messaging Box
----------------

Like Flask's flash feature, Skitai also provide messaging tool.

.. code:: python  

  @app.route ("/msg")
  def msg (was):
    was.mbox.send ("This is Flash Message", "flash")
    was.mbox.send ("This is Alert Message Kept by 60 seconds on every request", "alram", valid = 60)
    return was.redirect (was.ab ("showmsg", "Hans Roh"), status = "302 Object Moved")
  
  @app.route ("/showmsg")
  def showmsg (was, name):
    return was.render ("msg.htm", name=name)
    
A part of msg.htm is like this:

.. code:: html

  Messages To {{ name }},
  <ul>
  	{% for message_id, category, created, valid, msg, extra in was.mbox.get () %}
  		<li> {{ mtype }}: {{ msg }}</li>
  	{% endfor %}
  </ul>

Default value of valid argument is 0, which means if page called was.mbox.get() is finished successfully, it is automatically deleted from mbox.

But like flash message, if messages are delayed by next request, these messages are save into secured cookie value, so delayed/long term valid messages size is limited by cookie specificatio. Then shorter and fewer messsages would be better as possible.

'was.mbox' can be used for general page creation like handling notice, alram or error messages consistently. In this case, these messages (valid=0) is consumed by current request, there's no particular size limitation.

Also note valid argument is 0, it will be shown at next request just one time, but inspite of next request is after hundred years, it will be shown if browser has cookie values.

.. code:: python  
  
  @app.before_request
  def before_request (was):
    if has_new_item ():
      was.mbox.send ("New Item Arrived", "notice")
  
  @app.route ("/main")  
  def main (was):
    return was.render ("news.htm")

news.htm like this:

.. code:: html

  News for {{ was.g.username }},
  <ul>
  	{% for mid, category, created, valid, msg, extra in was.mbox.get ("notice", "news") %}
  		<li class="{{category}}"> {{ msg }}</li>
  	{% endfor %}
  </ul>

- was.mbox.send (msg, category, valid_seconds, key=val, ...)
- was.mbox.get () return [(message_id, category, created_time, valid_seconds, msg, extra_dict)]
- was.mbox.get (category) filtered by category
- was.mbox.get (key, val) filtered by extra_dict
- was.mbox.source_verified (): If current IP address matches with last IP accesss mbox
- was.mbox.getv (...) return get () if source_verified ()
- was.mbox.search (key, val): find in extra_dict. if val is not given or given None, compare with category name. return [message_id, ...]
- was.mbox.remove (message_id)


Named Session & Messaging Box
------------------------------

*New in version 0.15.30*

You can create multiple named session and mbox objects by mount() methods.

.. code:: python

  was.session.mount (
    name = None, securekey = None, 
    path = None, domain = None, secure = False, http_only = False, 
    session_timeout = None
   )
  
  was.mbox.mount (
    name = None, securekey = None, 
    path = None, domain = None, secure = False, http_only = False
  )


For example, your app need isolated session or mbox seperated default session for any reasons, can create session named 'ADM' and if this session or mbox is valid at only /admin URL.

.. code:: python

  @app.route("/")
  def index (was):	 
    was.session.mount ("ADM", SECUREKEY_STRING, path = '/admin')
    was.session.set ("admin_login", True)

    was.mbox.mount ("ADM", SECUREKEY_STRING, path = '/admin')
    was.mbox.send ("10 data has been deleted", 'warning')

SECUREKEY_STRING needn't same with app.securekey. And path, domain, secure, http_only args is for session cookie, you can mount any named sessions or mboxes with upper cookie path and upper cookie domain. In other words, to share session or mbox with another apps, path should be closer to root (/).

.. code:: python

  @app.route("/")
  def index (was):	 
    was.session.mount ("ADM", SECUREKEY_STRING, path = '/')
    was.session.set ("admin_login", True)

Above 'ADM' sesion can be accessed by all mounted apps because path is '/'.
    
Also note was.session.mount (None, SECUREKEY_STRING) is exactly same as mounting default session, but in this case SECUREKEY_STRING should be same as app.securekey.

mount() is create named session or mbox if not exists, exists() is just check wheather exists named session already.

.. code:: python

  if not was.session.exists (None):
    return "Your session maybe expired or signed out, please sign in again"
      
  if not was.session.exists ("ADM"):
    return "Your admin session maybe expired or signed out, please sign in again"




File Upload
---------------

.. code:: python
  
  FORM = """
    <form enctype="multipart/form-data" method="post">
    <input type="hidden" name="submit-hidden" value="Genious">   
    <p></p>What is your name? <input type="text" name="submit-name" value="Hans Roh"></p>
    <p></p>What files are you sending? <br />
    <input type="file" name="file">
    </p>
    <input type="submit" value="Send"> 
    <input type="reset">
  </form>
  """
  
  @app.route ("/upload")
  def upload (was, *form):
    if was.request.command == "get":
      return FORM
    else:
      file = form.get ("file")
      if file:
        file.save ("d:\\var\\upload", dup = "o") # overwrite
			  
'file' object's attributes are:

- file.file: temporary saved file full path
- file.name: original file name posted
- file.size
- file.mimetype
- file.remove ()
- file.save (into, name = None, mkdir = False, dup = "u")

  * if name is None, used file.name
  * dup: 
    
    + u - make unique (default)
    + o - overwrite


Registering Event Calls To App and was.g
-----------------------------------------

.. code:: python

  @app.before_request
  def before_request (was):
    if not login ():
      return "Not Authorized"
  
  @app.finish_request
  def finish_request (was):
    was.g.user_id    
    was.g.user_status
    ...
  
  @app.failed_request
  def failed_request (was, exc_info):
    was.g.user_id    
    was.g.user_status
    ...
  
  @app.teardown_request
  def teardown_request (was):
    was.g.resouce.close ()
    ...
  
  @app.route ("/view-account")
  def view_account (was, userid):
    was.g.user_id = "jerry"
    was.g.user_status = "active"
    was.g.resouce = open ()
    return ...

For this situation, 'was' provide was.g that is empty class instance. was.g is valid only in current request. After end of current request.

If view_account is called, Saddle execute these sequence:

.. code:: python
  
  try:
    try: 
      content = before_request (was)
      if content:
        return content
      content = view_account (was, *args, **karg)
      
    except:
      content = failed_request (was, sys.exc_info ())
      if content is None:
      	raise
      
    else:
      finish_request (was)

  finally:
    teardown_request (was)
  
  return content
    
Be attention, failed_request's 2nd arguments is sys.exc_info (). Also finish_request and teardown_request (NOT failed_request) should return None (or return nothing). 

If you handle exception with failed_request (), return custom error content, or exception will be reraised and Saddle will handle exception.

*New in version 0.14.13*

.. code:: python

 @app.failed_request
  def failed_request (was, exc_info):
    # releasing resources
    return was.response (
    	"501 Server Error", 
    	was.render ("err501.htm", msg = "We're sorry but something's going wrong")
    )
    
Also there're another kind of method group,

.. code:: python

  @app.startup
  def startup (wasc):
    logger = wasc.logger.get ("app")
    # OR
    logger = wasc.logger.make_logger ("login", "daily")
    config = wasc.config
    wasc.register ("loginengine", SNSLoginEngine (logger))
    wasc.register ("searcher", FulltextSearcher (wasc.numthreads))    
  
  @app.onreload  
  def onreload (wasc):
    wasc.loginengine.reset ()
  
  @app.shutdown    
  def shutdown (wasc):
    wasc.searcher.close ()
        
    wasc.unregister ("loginengine")
    wasc.unregister ("searcher")
  
'wasc' is Python Class object of 'was', so mainly used for sharing Skitai server-wide object via was.object.

And you can access numthreads, logger, config from wasc.

As a result, myobject can be accessed by all your current app functions even all other apps mounted on Skitai.

.. code:: python
  
  # app mounted to 'abc.com/members'
  @app.route ("/")
  def index (was):
    was.loginengine.get_user_info ()
    was.searcher.query ("ipad")
  
  # app mounted to 'abc.com/register'
  @app.route ("/")
  def index (was):
    was.loginengine.check_user_to ("facebook")
    was.searcher.query ("ipad")
  
  # app mounted to 'def.com/'
  @app.route ("/")
  def index (was):
    was.searcher.query ("news")

*Note:* The way to mount with host, see *'Mounting With Virtual Host'* chapter below.

It maybe used like plugin system. If a app which should be mounted loads pulgin-like objects, theses can be used by Skitai server wide apps via was.object1, was.object2,...

These methods will be called,

1. startup: when app imported on skitai server started
2. onreload: when app.use_reloader is True and app is reloaded
3. shutdown: when skitai server is shutdowned
  

WWW-Authenticate
-------------------

*Changed in version 0.15.21*

  - removed app.user and app.password
  - add app.users object has get(username) methods like dictionary  

Saddle provide simple authenticate for administration or perform access control from other system's call.

.. code:: python

  app = Saddle (__name__)
  
  app.authorization = "digest"
  app.authenticate = True
  app.realm = "Partner App Area of mysite.com"
  app.users = {"app": ("iamyourpartnerapp", 0, {'role': 'root'})}
	
  @app.route ("/hello/<name>")
  def hello (was, name = "Hans Roh"):
    return "Hello, %s" % name

If app.authenticate is True, all routes of app require authorization (default is False).

Otherwise you can make some routes requirigng authorization like this:

.. code:: python
 
  @app.route ("/hello/<name>", authenticate = True)
  def hello (was, name = "Hans Roh"):
    return "Hello, %s" % name


The return of app.users.get (username) can be:

  - (str password, boolean encrypted, obj userinfo)
  - (str password, boolean encrypted)
  - str password

If you use encrypted password, you should use digest authorization and password should encrypt by this way:

.. code:: python
  
  from hashlib import md5
  
  encrypted_password = md5 (
  	("%s:%s:%s" % (username, realm, password)).encode ("utf8")
  ).hexdigest ()

		
If authorization is successful, app can access username and userinfo vi was.request.user.

  - was.request.user.name
  - was.request.user.realm
  - was.request.user.info
  

If your server run with SSL, you can use app.authorization = "basic", otherwise recommend using "digest" for your password safety.


Mount Saddlery On Saddle (Packaging for Larger App)
-----------------------------------------------------

*Changed in version 0.15*

Before 0.15

.. code:: python
  
  # admin.py
  from skitai.saddle import Package
  app = Package ("/admin") # mount point
  
  @app.route ("/<name>")
  def hello (was):
    # can build other module's method url
    return was.ab ("index", 1, 2) 
    
  # app.py
  from skitai.saddle import Saddle
  from . import admin
  
  app = Saddle (__name__)
  app.add_package (admin, "app")
  
  @app.route ("/")
  def index (was, num1, num2):  
    return was.ab ("hello", "Hans Roh") # url building
  
For now, if your app is very large or want to manage codes by categories, you can seperate your app.

admin.py
  
.. code:: python

  from skitai.saddle import Saddlery
  part = Saddlery ()
  
  @part.route ("/<name>")
  def hello (was):
    # can build other module's method url
    return was.ab ("index", 1, 2) 

app.py

.. code:: python

  from skitai.saddle import Saddle
  from . import admin
  
  app = Saddle (__name__)
  app.debug = True
  app.use_reloader = True  
  app.mount ("/admin", admin, "part")
  
  @app.route ("/")
  def index (was, num1, num2):  
    return was.ab ("hello", "Hans Roh") # url building
        
Now, hello function's can be accessed by '/[app mount point]/admin/Hans_Roh'.
  
App's configs like debug & use_reloader, etc, will be applied to packages except event calls.

*Note:* was.app is always main Saddle app NOT current Saddlery sub app.

Saddlery can have own sub Saddlery and event calls.

.. code:: python
  
  from skitai.saddle import Saddlery
  from . import admin_sub
  
  part = Saddlery () # mount point
  # Saddlery also can have sub Saddlery
  part.mount ("/admin/sub", admin_sub, "app")
  
  @part.startup
  def startup (wasc):
    wasc.register ("loginengine", SNSLoginEngine ())
    wasc.register ("searcher", FulltextSearcher ())    
  
  @part.shutdown    
  def shutdown (wasc):
    wasc.searcher.close ()
        
    wasc.unregister ("loginengine")
    wasc.unregister ("searcher")
    
  @part.before_request
  def before_request (was):
    if not login ():
      return "Not Authorized"
  
  @part.teardown_request
  def teardown_request (was):
    was.g.resouce.close ()
    ...
  
  @part.route ("/<name>")
  def hello (was):
    # can build other module's method url
    return was.ab ("index", 1, 2) 

In this case, app and sub-app's event calls are nested executed in this order.

.. code:: python

  app.before_request()
    sub-app.before_request()
      hello()
    sub-app.finish_request() or package.failed_request()
    sub-app.teardown_request ()
  app.finish_request() or app.failed_request()
  app.teardown_request ()


**Saddlery and Jinja2 Templates**

was.render (template_path) always find templates directory where app.py exists, even if admin.py is located in sub directory with package form. This is somewhat conflicated but I think it's more easier way to maintain template files and template include policy. Remeber one app can have one templates directoty. But you can seperate into templates files by sub directory. For example:

.. code:: python

  /app.py
  /admin.py
  /members/__init__.py
  /static
  /templates/includes/header.html  
  /templates/includes/footer.html
  /templates/app/index.html  
  /templates/admin/index.html
  /templates/members/index.html

But if you want to use independent templates under own templates directory:

.. code:: python

  from skitai.saddle import Saddlery
  
  part = Saddlery (__name__)
  
  @part.route ("/<name>")
  def hello (was):
    return was.render2 ("show.htm", name = name)


Implementing XMLRPC Service
-----------------------------

Client Side:

.. code:: python

  import xmlrpc.client as rpc
  
  s = rpc.Server ("http://127.0.0.1:5000/rpc") # RPC App mount point
  result = s.add (10000, 5000)  
  
  
Server Side:

.. code:: python

  @app.route ("/add")
  def index (was, num1, num2):  
    return num1 + num2

Is there nothing to diffrence? Yes. Saddle app methods are also used for XMLRPC service if return values are XMLRPC dumpable.


Logging and Traceback
------------------------

If Skitai run with -v option, app and exceptions are displayed at your console, else logged at files.

.. code:: python
  
  @app.route ("/")
  def sum ():  
    was.log ("called index", "info")    
    try:
      ...
    except:  
    	was.log ("exception occured", "error")
    	was.traceback ("bp1")
    was.log ("done index", "info")

Note inspite of you do not handle exception, all app exceptions will be logged automatically by Saddle. And it includes app importing and reloading exceptions.

- was.log (msg, category = "info")
- was.traceback (identifier = "") # identifier is used as fast searching log line for debug


Project Purpose
===================

Skitai App Engine's original purpose is to serve python fulltext search engine Wissen_ which is my another pypi work. And I found that it is possibly useful for building and serving websites.

Anyway, I am modifying my codes to optimizing for enabling service on Linux machine with relatvely poor H/W (ex. AWS_ t2.nano instance) and making easy to auto-scaling provided cloud computing service like AWS_.

If you need lots of outside http(s) resources connecting jobs and use PostgreSQL, it might be worth testing and participating this project.

Also note it might be more efficient that circumstance using `Gevent WSGI Server`_ + Flask. They have well documentation and already tested by lots of users.


.. _Wissen: https://pypi.python.org/pypi/wissen
.. _AWS: https://aws.amazon.com
.. _`Gevent WSGI Server`: http://www.gevent.org/


Links
======

- `GitLab Repository`_
- Bug Report: `GitLab issues`_

.. _`GitLab Repository`: https://gitlab.com/hansroh/skitai
.. _`GitLab issues`: https://gitlab.com/hansroh/skitai/issues
.. _`Skitai WSGI App Engine`: https://pypi.python.org/pypi/skitaid


Change Log
==============
  
  0.20 (Dec 2016)
  
  - View *News & Changes* chapter
  
  0.19 (Dec 2016)
  
  - Reengineering was.request methods, fix disk caching  
  
  0.18 (Dec 2016)
  
  - 0.18.11 - default content-type of was.post(), was.put() has been changed from 'application/x-www-form-urlencoded' to 'application/json'. if you use this method currently, you SHOULD change method name to was.postform()

  - 0.18.7 - response contents caching has been applied to all was.request services (except websocket requests).

  
  0.17 (Oct 2016)
  
  - `Skitai WSGI App Engine`_ is seperated
  
  0.16 (Sep 2016)
  
  - 0.16.20 fix SSL proxy and divide into package for proxy & websocket_handler
  - 0.16.19 fix HTTP2 cookie
  - 0.16.18 fix handle large request body
  - 0.16.13 fix thread locking for h2.Connection
  - 0.16.11 fix pushing promise and response on Firefox
  - 0.16.8 fix pushing promise and response
  - 0.16.6 add several configs to was.app.config for limiting post body size from client
  - 0.16.5 add method: was.response.hint_promise (uri) for sending HTP/2 PUSH PROMISE frame
  - 0.16.3 fix flow control window
  - 0.16.2 fix HTTP/2 Uprading for "http" URIs (RFC 7540 Section 3.2)
  - 0.16 HTTP/2.0 implemented with hyper-h2_
  
  0.15 (Mar 2016)
  
  - fixed fancy URL <path> routing
  - add Websocket design spec: WEBSOCKET_DEDICATE_THREADSAFE
  - fixed Websocket keep-alive timeout
  - fixed fancy URL routing
  - 'was.cookie.set()' method prototype has been changed.
  - added Named Session & Messaging Box
  - fix select error when closed socket, thanks to spam-proxy-bots
  - add mimetypes for .css .js
  - fix debug output
  - fix asynconnect.maintern
  - fix loosing end of compressed content
  - fix app reloading, @shutdown
  - fix XMLRPC response and POST length
  - add was.mbox.search (), change spec was.mbox.get ()
  - fix routing bugs & was.ab()
  - add saddle.Saddlery class for app packaging
  - @app.startup, @app.onreload, @app.shutdown arguments has been changed
  
  0.14 (Feb 2016)
  
  - fix proxy occupies CPU on POST method failing
  - was.log(), was.traceback() added
  - fix valid time in message box 
  - changed @failed_request event call arguments and can return custom error page
  - changed skitaid.py command line options, see 'skitaid.py --help'
  - batch task scheduler added
  - e-mail sending fixed
  - was.session.getv () added
  - was.response spec. changed
  - SQLite3 DB connection added
  
  0.13 (Feb 2016)
  
  - was.mbox, was.g, was.redirect, was.render added  
  - SQLite3 DB connection added
  
  0.12 (Jan 2016) - Re-engineering 'was' networking, PostgreSQL & proxy modules
  
  0.11 (Jan 2016) - Websocket implemeted
  
  0.10 (Dec 2015) - WSGI support
  
