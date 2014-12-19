from django import template
import math

register = template.Library()


@register.filter(name='secToDuration')
def secToDuration(value):
	"""Convert seconds int into hh:mm:ss string"""
	def standardize(num):
		if (num < 10):
			num = "0" + str(num)
		return num

	secs = int(value)
	if secs > 0:
		hourSecs = 3600
		minSecs = 60
		# Create string to hold outout
		durationString = ''
		# Calculate number of hours from seconds
		hours = int(math.floor(secs / int(hourSecs)))
		# Subtract hours from seconds
		secs = secs - (hours * int(hourSecs))
		# Calculate number of minutes from seconds (minus number of days and hours)
		minutes = int(math.floor(secs / int(minSecs)))
		# Subtract days from seconds
		secs = secs - (minutes * int(minSecs))
		# Calculate number of seconds (minus days, hours and minutes)
		seconds = secs
		try:
			if(hours != 0):
				durationString = str(standardize(hours)) + ":"
			durationString += str(standardize(minutes)) + ":"
			durationString += str(standardize(seconds))
		except Exception:
			raise

		return durationString.strip()
	else:
		return '00:00'
