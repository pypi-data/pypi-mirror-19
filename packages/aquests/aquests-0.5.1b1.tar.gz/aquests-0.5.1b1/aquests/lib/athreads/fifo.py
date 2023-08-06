import threading
from collections import deque

class ready_producer_fifo:
	# On http2, it is impossible to bind channel.ready function, 
	# Because http2 channels handle multiple responses concurrently
	# Practically USE http2_producer_fifo
	
	def __init__ (self):
		self.l = deque ()
		self.r = deque ()
		self.has_None = False
	
	def working (self):
		return (self.has_None or self.l or self.r) and 1 or 0
	
	def __len__ (self):
		if self.has_None and not self.l and not self.r:
			# for return None
			self.l.append (None)
			self.has_None = False
			return 1
			
		if self.l:
			if not hasattr (self.l [0], 'ready'):
				return 1
			if not self.l [0].ready ():
				item = self.l.popleft ()
				self.r.append (item)
		
		if self.l:
			return 1
	
		if self.r:
			for i in range (len (self.r)):				
				if self.r [0].ready ():					
					self.l.append (self.r.popleft ())
					return 1	
				self.r.rotate (1)				
		return 0
			
	def __getitem__(self, index):
		return self.l [index]			
				
	def __setitem__(self, index, item):
		if index == 0:
			self.l.appendleft (item)
		else:
			self.l.append (item)
		
	def __delitem__ (self, index):
		del self.l [index]
	
	def append (self, item):		
		self.insert (-1, item)
	
	def appendleft (self, item):
		self.insert (0, item)
	
	def insert_into (self, lst, index, item):		
		if index == 0:
			lst.appendleft (item)
		else:
			lst.append (item)	
		
	def insert (self, index, item):
		if item is None:
			self.has_None = True
			return
			
		if self.has_None:
			return # deny adding	
		
		if hasattr (item, 'ready'):
			return self.insert_into (self.r, index, item)			
		
		self.insert_into (self.l, index, item)		
		
	def clear (self):
		self.l.clear ()
		self.r.clear ()
	
	
class ready_producer_ts_fifo (ready_producer_fifo):
	def __init__ (self):
		ready_producer_fifo.__init__ (self)
		self._lock = threading.Lock ()
	
	def working (self):
		with self._lock:
			return ready_producer_fifo.working (self)
		
	def __len__ (self):
		with self._lock:
			return ready_producer_fifo.__len__ (self)
			
	def __getitem__(self, index):
		with self._lock:
			return ready_producer_fifo.__getitem__ (self, index)
		
	def __setitem__(self, index, item):
		with self._lock:
			ready_producer_fifo.__setitem__ (self, index, item)
		
	def __delitem__ (self, index):
		with self._lock:
			ready_producer_fifo.__delitem__ (self, index)
	
	def clear (self):
		with self._lock:
			ready_producer_fifo.clear (self)
			
	def insert (self, index, item):
		with self._lock:
			ready_producer_fifo.insert (self, index, item)

			
class http2_producer_fifo (ready_producer_ts_fifo):
	# Asyncore ready_producer_fifo replacement
	# For resorting, removeing by http2 priority, cacnel and reset features
	# Also can handle producers has 'ready' method
		
	def remove_from (self, stream_id, lst):
		deleted = 0
		for i in range (len (lst)):
			try:
				producer_stream_id = lst [0].stream_id
			except AttributeError:
				pass
			else:
				if producer_stream_id	== stream_id:
					lst.popleft ()
					deleted += 1
			lst.rotate (1)
		return deleted
							
	def remove (self, stream_id):
		with self._lock:
			if self.l:
				self.remove_from (stream_id, self.l)
			if self.r:
				self.remove_from (stream_id, self.r)
			
	def insert (self, index, item):
		if item is None:
			with self._lock:
				self.has_None = True
			return
		
		with self._lock:	
			if self.has_None:
				return # deny adding	
		
		if hasattr (item, 'ready'):
			with self._lock:
				return self.insert_into (self.r, index, item)
		
		# insert by priority
		try:
			w1 = item.weight
			d1 = item.depends_on
		except AttributeError:
			with self._lock:
				return self.insert_into (self.l, index, item)
		
		index = 0
		inserted = False
		with self._lock:
			for each in self.l:
				try:
					w2 = each.weight
					d2 = each.depends_on
				except AttributeError:
					pass
				else:
					if d2 >= d1 and w2 < w1:
						self.insert_into (self.l, index, item)
						inserted = True
						break
				index += 1
				
			if not inserted:
				self.l.append (item)
				
