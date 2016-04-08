import sublime, sublime_plugin, os, os.path
# thread module has been renamed to _thread in python 3
try:
    import _thread
except ImportError:
    import thread as _thread

class TagThreadManager(object):
	@classmethod
	def load(cls):
		cls.metadata_files = {}

    @classmethod
    def is_enabled(cls, view):
        try:
            filename = view.file_name()
            if filename[-5:] == "_TAG_":
                if not filename in cls.snapfiles.keys():
                    cls.snapfiles[filename] = open(filename + ".tags", "a")
                return True
            else:
                return False
        except:
            return False

class AddTagRegion(sublime_plugin.TextCommand):
	def run(self, edit, scope):

		v = self.view

		# tag = scope for prototyping purposes
		tag = scope

		v.add_regions(tag, v.sel(), scope, '', (sublime.PERSISTENT|sublime.DRAW_NO_OUTLINE))

