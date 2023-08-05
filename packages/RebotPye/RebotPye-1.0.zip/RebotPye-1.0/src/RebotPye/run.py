# -*- coding: utf-8 -*-

# External Imports
import sys
import glob

# Internal imports
import _original_templates
import _new_templates

def main(args):
	"""
	
	Author:			Olivier Verville
	Date:			December 21st 2016
	Last Revision:		N/A
	
	RebotPye (Rebot Pie) is a Robot Framework module plugin meant to add a visual pie chart representing
	the fail vs. success ratio in your tests html report file(s). Much alike Robot Framework's module, robot.rebot,
	RebotPye is a post-test processing tool.
	
	Usage Example:
	
	RebotPye report.html
	RebotPye *.html
	RebotPye results/*.html
	
	"""

	# Iter through given arguments
	for arg in args:
	
		# Iter through files that match our current arg
		for file in glob.glob(arg):
			
			# Open & read matched file
			with open(file, 'r') as f:
				html_report_source = f.read()

			# Inject our custom code into the read report html output
			html_report_source = html_report_source.replace(_original_templates.js_function, _new_templates.js_function)
			html_report_source = html_report_source.replace(_original_templates.html_template, _new_templates.html_template)

			# Rewrite the file with our injected code
			new_file = open(file, "w")
			new_file.write(html_report_source)
		
if __name__ == '__main__':
	main(sys.argv[1:])