import asyncore 
import re 
import time 
import sys 
import threading 	

DEBUG = False

class OperationalError (Exception):
	pass
	
	
class DBConnect:
	zombie_timeout = 120	
	
	def __init__ (self, address, params = None, lock = None, logger = None):
		self.address = address
		self.params = params
		self.lock = lock		
		self.logger = logger
		
		self.request_count = 0
		self.execute_count = 0
		
		self._cv = threading.Condition ()
		self.active = 0		
		self.conn = None
		self.cur = None
		self.callback = None
		self.out_buffer = ""		
		self.__history = []
		self.set_event_time ()
	
	def get_history (self):
		return self.__history
		
	def duplicate (self):
		return self.__class__ (self.address, self.params, self.lock, self.logger)
		
	def clean_shutdown_control (self, phase, time_in_this_phase):
		if phase == 2:
			self.handle_close (OperationalError, "was entered shutdown process")			
	
	def empty_cursor (self):
		if self.has_result:
			self.fetchall ()			
	
	def maintern (self, object_timeout):
		# query done but not used
		if self.has_result and self.isactive () and time.time () - self.event_time > self.zombie_timeout:			
			self.empty_cursor ()
			self.set_active (False)
			
		if time.time () - self.event_time > object_timeout:
			if not self.isactive ():
				self.disconnect ()
				return True # deletable
		return False	
	
	def reconnect (self):
		self.disconnect ()
		self.connect ()
	
	def disconnect (self):
		self.close ()
				
	def close (self):
		if self.cur:
			self.empty_cursor ()
			try: self.cur.close ()
			except: pass							
		try: self.conn.close ()
		except: pass			
		self.cur = None
		self.conn = None		
	
	def close_case (self):
		if self.callback:
			if self.has_result:
				self.callback (self.cur.description, self.exception_class, self.exception_str, self.fetchall ())
			else:
				self.callback (None, self.exception_class, self.exception_str, None)
			self.callback = None
		self.set_active (False)
			
	def set_active (self, flag, nolock = False):
		if flag:
			flag = time.time ()
		else:
			flag = 0
		if nolock or self.lock is None:
			self.active = flag
			return			
		self.lock.acquire ()
		self.active = flag
		self.request_count += 1
		self.lock.release ()
	
	def get_active (self, nolock = False):
		if nolock or self.lock is None:
			return self.active			
		self.lock.acquire ()	
		active = self.active
		self.lock.release ()	
		return active
	
	def isactive (self):	
		return self.get_active () > 0
		
	def isconnected (self):	
		return self.connected
		
	def get_request_count (self):	
		return self.request_count
	
	def get_execute_count (self):	
		return self.execute_count
	
	def connect (self, force = 0):
		raise NotImplementedError("must be implemented in subclass")
	
	def set_zombie_timeout (self, timeout):
		self.zombie_timeout = timeout

	def handle_timeout (self):
		self.handle_close (OperationalError, "Operation Timeout")
	
	def handle_error (self):
		dummy, exception_class, exception_str, tbinfo = asyncore.compact_traceback()
		self.logger.trace ()
		self.handle_close (exception_class, exception_str)
	
	def handle_close (self, expt = None, msg = ""):		
		self.exception_class, self.exception_str = expt, msg		
		self.close ()
		self.close_case ()
	
	def set_event_time (self):
		self.event_time = time.time ()			
		
	#-----------------------------------------------------
	# DB methods
	#-----------------------------------------------------
	def fetchall (self):		
		result = self.cur.fetchall ()
		self.has_result = False
		return result
		
	def execute (self, sql, callback):
		if DEBUG: self.__history.append ("BEGIN TRAN: %s" % sql)
		raise NotImplementedError("must be implemented in subclass")

