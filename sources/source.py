import importlib
from django.conf import settings

modules = {}
for source in settings.SOURCES:
    modules[source] = importlib.import_module('sources.' + source)


def search(source, query):
    return modules[source].search(query)


def check_validity(source, id):
    # Mock check during test suite
    if settings.TESTING:
        return True
    return modules[source].check_validity(id)
