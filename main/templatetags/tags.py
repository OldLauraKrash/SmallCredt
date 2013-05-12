from django import template

register = template.Library()

@register.simple_tag
def split_filename(filename):
	filename = str(filename)
	return filename.split('/')[3]