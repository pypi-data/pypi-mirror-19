from . import wsgi_executor
try:
	import xmlrpc.client as xmlrpclib
except ImportError:
	import xmlrpclib
import sys, os


class Executor (wsgi_executor.Executor):
	def import_proto (self, name):
		fullname = "skitai.proto.%s" % name
		proto = sys.modules.get (fullname)
		if not proto:
			path = os.apth.join (os.path.split (self.was.env ["SCRPIT_PATH"]) [0], "proto", proto + ".py")
			return importlib.machinery.SourceFileLoader(fullname, path).load_module()
		return proto

	def __call__ (self):
		__input = self.env.get ("wsgi.input")
		if __input:
			data = __input.read ()
		else:
			data = None	
			
		proto, methodname = self.env ["PATH_INFO"].split ("/") [-2:]
		if data:
			message = import_proto (proto)
			args = message.parseFromString (data)
		self.build_was ()
		
		current_app, thing, param = self.get_method (self.env ["PATH_INFO"])
		if not thing or param == 301:
			raise Exception('Method "%s" is not supported' % _method)			
		self.was.subapp = current_app
		result = self.generate_content (thing, _args, {})		
		del self.was.subapp
		
		self.commit ()
		self.was.response ["Content-Type"] = "application/jrpc+proto"
		
		del self.was.env		
		return result.SerializeToString ()
