import sublime, sublime_plugin, shelve
# thread module has been renamed to _thread in python 3
try:
    import _thread
except ImportError:
    import thread as _thread

class TagManager(object):
	@classmethod
	def load(cls):
		cls.tagshelves = {}

TagManager.load()

class AddTagRegion(sublime_plugin.TextCommand):
	def run(self, edit, tag):
		v = self.view
		tagshelve = TagManager.tagshelves[v.file_name()]

		old_regions = v.get_regions(tag)
		print("old_regions == %s" % old_regions)
		new_regions = v.sel()
		new_regions.add_all(old_regions)
		print("new_regions == %s" % new_regions)
		tagshelve[tag] = new_regions
		tagshelve.sync()
		# scope (third arg) == tag for prototyping purposes
		v.add_regions(tag, new_regions, tag, '')

class InitTagFile(sublime_plugin.EventListener):
	def on_load(self, view):
		filename = view.file_name()
		if "TAGTEST_" in filename:
			tagshelve = shelve.open(filename + '.tags')
			TagManager.tagshelves[filename] = tagshelve
			for tag, saved_regions in tagshelve.items():
				view.add_regions(tag, saved_regions, tag, '')

	def on_close(self, view):
		filename = view.file_name()
		if "TAGTEST_" in filename:
			TagManager.tagshelves[filename].close()
