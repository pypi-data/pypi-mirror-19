from . import wsgi_executor
try:
	import xmlrpc.client as xmlrpclib
except ImportError:
	import xmlrpclib
import sys, os
import struct
from skitai.lib import producers
from collections import Iterable

    
class grpc_producer (producers.iter_producer):		
	def more (self):		
		try:
			data = next (self.data)
			serialized = data.SerializeToString ()
			return struct.pack ("<B", 0) + struct.pack ("<i", len (serialized)) + serialized			
		except StopIteration:			
			return b""
	
	
class Executor (wsgi_executor.Executor):
	def get_messages (self, fp):
		msgs = []
		byte = fp.read (1)
		while byte:
			iscompressed = struct.unpack ("<B", byte) [0]
			length = struct.unpack ("<i", fp.read (4)) [0]
			msg = fp.read (length)
			msgs.append (msg)
			byte = fp.read (1)
		return tuple (msgs)
		
	def __call__ (self):
		request = self.env ["skitai.was"].request
		msgs = self.get_messages (self.env.get ("wsgi.input"))
		servicename, methodname = self.env ["PATH_INFO"].split ("/") [-2:]
		
		self.build_was ()
		current_app, thing, param, respcode = self.find_method (request, "/" + methodname)
		if respcode: 
			return b""
		
		self.was.subapp = current_app
		result = self.generate_content (thing, msgs, {})		
		del self.was.subapp
		
		self.commit ()
		self.was.response ["Content-Type"] = "application/grpc+proto"

		del self.was.env		
		
		if type (result) is list:
			result = iter (result)		
		return grpc_producer (result)
		
		