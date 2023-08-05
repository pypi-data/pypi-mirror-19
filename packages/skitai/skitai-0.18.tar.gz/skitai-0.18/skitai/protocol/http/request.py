try:
	import xmlrpc.client as xmlrpclib
except ImportError:
	import xmlrpclib
	
import base64
try: 
	from urllib.parse import urlparse, quote
except ImportError:
	from urllib import quote
	from urlparse import urlparse
				
from skitai.lib import producers, strutil


class XMLRPCRequest:
	content_type = "text/xml"
			
	def __init__ (self, uri, method, params = (), headers = None, encoding = "utf8", auth = None, logger = None):
		self.uri = uri
		self.method = method
		self.params = params
		self.headers = headers
		self.encoding = encoding
		self.auth = (auth and type (auth) is not tuple and tuple (auth.split (":", 1)) or auth)
		self.logger = logger
		self.address, self.path = self.split (uri)
		self.__xmlrpc_serialized = False
		self.data = self.serialize ()		
	
	def xmlrpc_serialized (self):
		return self.__xmlrpc_serialized
		
	def set_address (self, address):
		self.address = address
		
	def get_address (self):
		return self.address
		
	def get_method (self):
		return "POST"
		
	def split (self, uri):
		if uri.find ("://") == -1:
			return None, uri
			
		scheme, address, script, params, qs, fragment = urlparse (uri)		
		if not script: script = "/"
		path = script
		if params: path += ";" + params
		if qs: path += "?" + qs
		
		try: 
			host, port = address.split (":", 1)
			port = int (port)
		except ValueError:
			host = address
			if scheme in ("http", "ws"):
				port = 80
			else:
				port = 443	
		
		return (host, port)	, path
		
	def serialize (self):
		self.__xmlrpc_serialized = True
		return xmlrpclib.dumps (self.params, self.method, encoding=self.encoding, allow_none=1).encode ("utf8")
	
	def get_auth (self):
		return self.auth
		
	def get_data (self):
		return self.data
	
	def get_useragent (self):
		return "Mozilla/5.0 (compatible; Skitaibot/0.1a)"
				
	def get_content_type (self):
		if self.headers:
			for k, v in list(self.headers.items ()):
				if k.lower () == "content-length":
					del self.headers [k]
				elif k.lower () == "content-type":
					self.content_type = v
					del self.headers [k]
		return self.content_type
	
	def get_headers (self):
		if self.headers:
			return list(self.headers.items ())
		else:
			return []	
			
	
class HTTPRequest (XMLRPCRequest):
	content_type = "application/x-www-form-urlencoded; charset=utf-8"
	def get_method (self):
		return self.method.upper ()
					
	def serialize (self):
		# formdata type can be string, dict, boolean
		if not self.params:
			# no content, no content-type
			self.content_type = None		
			return b""

		if type (self.params) is type ({}):
			if self.get_content_type () != "application/x-www-form-urlencoded":
				raise TypeError ("POST Body should be string or can be encodable")
			fm = []
			for k, v in list(self.params.items ()):
				if self.encoding:
					v = v.decode (self.encoding)					
				fm.append ("%s=%s" % (quote (k), quote (v)))
			return "&".join (fm).encode ("utf8")
		
		if strutil.is_encodable (self.params):
			return self.params.encoding ("utf8")
		
		if self.encoding and strutil.is_decodable (self.params):
			return self.params.decode (self.encoding).encoding ("utf8") 
			
		return self.params
		
		
class HTTPPutRequest (HTTPRequest):
	# PUT content-type hasn't got default type
	content_type = None
			
	def get_method (self):
		return "PUT"
					
	def serialize (self):
		if type (self.params) is not str:
			raise TypeError ("PUT body must be string")
		if self.encoding:
			return self.params.decode (self.encoding).encode ("utf8")
		return self.params.encode ("utf8")
		
		
class HTTPMultipartRequest (HTTPRequest):
	boundary = "-------------------SAE-20150614204358"
	
	def __init__ (self, uri, method, params = {}, headers = None, encoding = None, auth = None, logger = None):
		HTTPRequest.__init__ (self, uri, method, params, headers, encoding, auth, logger)
		if type (self.params) is bytes:
			self.find_boundary ()
	
	def get_method (self):
		return "POST"
						
	def get_content_type (self):
		HTTPRequest.get_content_type (self) # for remove content-type header
		return "multipart/form-data; boundary=" + self.boundary
			
	def find_boundary (self):
		s = self.params.find (b"\r\n")
		if s == -1:
			raise ValueError("boundary not found")
		b = self.params [:s]			
		if b [:2] != b"--":
			raise ValueError("invalid multipart/form-data")
		self.boundary = b [2:s]
		
	def serialize (self):
		if type (self.params) is type ({}):
			return producers.multipart_producer (self.params, self.boundary, self.encoding)
		return self.params

