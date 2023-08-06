import os
import sys
from shutil import copyfile
import markdown
import errno
import argparse
import codecs

Markdown = markdown.Markdown(extensions=['markdown.extensions.fenced_code'])	
class main:
	def __init__(self):
		parser = argparse.ArgumentParser(description='Duplicate and then recursively convert markdown to html')
		parser.add_argument('source', metavar='Source', type=str, help="Location of the folder you wan't to convert")
		parser.add_argument('destination', metavar='Destination', type=str, help="Location where you wan't to save the folder")
		args = parser.parse_args()	
		self.duplicate_directory(args.source, args.destination)

	def ignore_function(self, ignore):
		def _ignore_(path, names):
			print('Working on %s' % path)			
			ignored_names = []
			if ignore in names:
				ignored_names.append(ignore)
			return set(ignored_names)
		return _ignore_

	def duplicate_directory(self, src, dest, ignore=None):
		errors = []		
		if os.path.isdir(src):
			if not os.path.isdir(dest):
				os.makedirs(dest)
			files = os.listdir(src)
			if ignore is not None:
				ignored = ignore(src, files)
			else:
				ignored = set()
			for file in files:
				if file not in ignored:
					sourceName = os.path.join(src, file)
					destName = os.path.join(dest, file)
					self.duplicate_directory(sourceName, destName, ignore)
		else:
			if src.endswith('.md'):			
				copyfile(src, dest)
				self.convertToHtml(src, dest)

	def convertToHtml(self, src, dest):
		f = codecs.open(dest, mode="r", encoding="utf-8", errors="replace")
		md = f.read()
		f.close()
		try:
			html = Markdown.reset().convert(md)
			output = codecs.open(dest, "w", encoding="utf-8", errors="replace")
			output.seek(0)
			output.truncate()
			output.write(html)
			output.close()
		except: 
			print("Skipping ?", dest)
