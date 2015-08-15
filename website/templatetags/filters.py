from django import template
import time

register = template.Library()


@register.filter(name='secToDuration')
def secToDuration(value):
	"""Convert seconds int into hh:mm:ss string"""
	durationString = time.strftime('%H:%M:%S', time.gmtime(value))
	if(durationString[0] + durationString[1] == "00"):
		durationString = durationString[3:]
	return durationString.strip()
