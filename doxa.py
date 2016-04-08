import sublime, sublime_plugin, shelve

tagshelves = {}

class TagFileManager(sublime_plugin.EventListener):
	def on_load(self, view):
		global tagshelves
		filename = view.file_name()
		if "TAGTEST_" in filename:
			tagshelve = shelve.open(filename + '.tags')
			tagshelves[filename] = tagshelve
			print("*** on_load ***")
			for tag, saved_regions in tagshelve.items():
				print("tagshelve['%s'] == %s" % (tag, [x for x in saved_regions]))
				view.add_regions(tag, saved_regions, tag, '', sublime.PERSISTENT)

	def on_close(self, view):
		global tagshelves
		filename = view.file_name()
		if "TAGTEST_" in filename:
			tagshelve = tagshelves[filename]
			print("*** on_close ***")
			for tag, saved_regions in tagshelve.items():
				print("tagshelve['%s'] == %s" % (tag, [x for x in saved_regions]))
			tagshelves[filename].close()

class AddTagRegion(sublime_plugin.TextCommand):
	def run(self, edit, tag):
		print("*** run ***")
		global tagshelves
		v = self.view
		tagshelve = tagshelves[v.file_name()]

		# get currently tagged regions as a list
		regions = v.get_regions(tag)
		print("(old) regions == %s" % regions)

		# make a list out of the current view selections and add to the list of regions
		regions += [r for r in v.sel()]
		print("(new) regions == %s" % regions)

		# update tagshelve
		tagshelve[tag] = regions
		tagshelve.sync()

		# scope (third arg) == tag for prototyping purposes
		# update ui
		v.add_regions(tag, regions, tag, '', sublime.PERSISTENT)
		for tag, saved_regions in tagshelve.items():
			print("tagshelve['%s'] == %s" % (tag, [x for x in saved_regions]))

