import json
import inspect



class ObjectEncoder(json.JSONEncoder):

	def default(self, obj):
		if hasattr(obj, "to_json"):
			return self.default(obj.to_json())
		elif hasattr(obj, "__dict__"):
			d = dict(
				(key, value)
				for key, value in inspect.getmembers(obj)
				if not key.startswith("__")
				and not inspect.isabstract(value)
				and not inspect.isbuiltin(value)
				and not inspect.isfunction(value)
				and not inspect.isgenerator(value)
				and not inspect.isgeneratorfunction(value)
				and not inspect.ismethod(value)
				and not inspect.ismethoddescriptor(value)
				and not inspect.isroutine(value)
			)
			return self.default(d)
		return obj
	#

#


