import importlib

modules = {}
for source in ['youtube', 'soundcloud']:
    modules[source] = importlib.import_module('sources.' + source)


class Source():
    @staticmethod
    def source(source, query):
        return modules[source].source(query)

    @staticmethod
    def check_validity(source, id):
        return modules[source].check_validity(id)
