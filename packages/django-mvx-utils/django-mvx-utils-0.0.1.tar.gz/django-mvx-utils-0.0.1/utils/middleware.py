from datetime import tzinfo

from django.utils import timezone

class VarOffset(tzinfo):

	def __init__(self):
		self.__offset = 0

	def utcoffset(self, dt):
		return self.__offset

	def tzname(self, dt):
		return ''

	def dst(self, dt):
		return timezone.ZERO

	@property
	def offset(self):
		return self.__offset

	@offset.setter
	def offset(self, value):
		self.__offset = value

class TimezoneMiddleware(object):
	"""Automatically sets based on the request.user's timezone. MUST be installed after the AuthenticationMiddleware."""

	def __init__(self):
		self.__timezone = VarOffset()

	def process_request(self, request):
		offset = getattr(request.user,'timezone', None)
		if offset is not None:
			self.__timezone.offset = offset
			timezone.activate(self.__timezone)

	def process_response(self, request, response):
		timezone.deactivate()
