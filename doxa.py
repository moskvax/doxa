import sublime, sublime_plugin, shelve

DOXA_ICON = ""
DOXA_FLAGS = sublime.PERSISTENT
DOXA_TAG_TO_SCOPE = {
	"judge": "string",
	"affect": "blah",
	"inscribe": "comment"
}
DOXA_TAGS = [k for k in DOXA_TAG_TO_SCOPE.keys()]

tagshelves = {}

class TagFileManager(sublime_plugin.EventListener):
	def on_load(self, view):
		filename = view.file_name()

		# only do anything if TAGTEST present in filename
		if "TAGTEST" in filename:
			# open the shelve and save a reference to it in the global dictionary
			tagshelve = shelve.open(filename + '.tags')
			tagshelves[filename] = tagshelve
			print("*** on_load ***")
			# add the regions in the shelve to the view
			for tag, saved_regions in tagshelve.items():
				print("tagshelve['%s'] == %s" % (tag, saved_regions))
				view.add_regions(tag, saved_regions, tag, DOXA_ICON, DOXA_FLAGS)

			# # init output window
			# view.window().create_output_panel("doxa")
			# view.window().run_command("show_panel", {"panel": "output.doxa"})

	def on_close(self, view):
		filename = view.file_name()
		if "TAGTEST" in filename:
			tagshelve = tagshelves[filename]
			print("*** on_close ***")
			for tag, saved_regions in tagshelve.items():
				print("tagshelve['%s'] == %s" % (tag, saved_regions))
			tagshelves[filename].close()

class DoxaTagRegion(sublime_plugin.TextCommand):

	def update_tags(self, index):
		if index >= 0:
			v = self.view
			tagshelve = tagshelves[v.file_name()]
			tag = DOXA_TAGS[index]
			scope = DOXA_TAG_TO_SCOPE[tag]

			# get currently tagged regions as a list
			regions = v.get_regions(tag)
			print("(old) regions == %s" % regions)

			# make a list out of the current view selections and add to the list of regions
			regions += [r for r in v.sel()]
			print("(new) regions == %s" % regions)

			# update tagshelve
			tagshelve[tag] = regions
			tagshelve.sync()

			# update regions in current ST session
			v.add_regions(tag, regions, scope, DOXA_ICON, DOXA_FLAGS)

			for tag, saved_regions in tagshelve.items():
				print("tagshelve['%s'] == %s" % (tag, saved_regions))

		else:
			return

	def run(self, edit):
		print("*** run ***")
		v = self.view
		v.window().show_quick_panel(DOXA_TAGS, self.update_tags)

		# # update output window
		# doxa_view = v.window().find_output_panel("doxa")
		# doxa_view.insert(edit, doxa_view.size(), "tagged regions %s with tag %s\n" % (regions, tag))
		# v.window().run_command("show_panel", {"panel": "output.doxa"})

