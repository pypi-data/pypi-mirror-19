import os

def get_webapp_taskrunner(webapp_root):
	"""Return gulp or gruntfile as the taskrunner if applicable."""
	if webapp_root.endswith('/'):
		parent = webapp_root.rsplit('/', 2)[0]
	else:
		parent = webapp_root.rsplit('/', 1)[0]
	task_runner = None
	if os.path.exists(parent + '/Gruntfile.js') or os.path.exists(parent + '/Gruntfile.coffee'):
		task_runner = 'grunt'
	elif os.path.exists(parent + '/gulpfile.js') or os.path.exists(parent + '/gulpfile.coffee'):
		task_runner = 'gulp'
	return parent, task_runner
