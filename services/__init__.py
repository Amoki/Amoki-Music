import importlib
from django.conf import settings

modules = {}
for name, path in settings.SERVICES.items():
    modules[name] = importlib.import_module(path)


def search(service, query):
    return modules[service].search(query)


def check_validity(service, id):
    # Mock check during test suite
    if settings.TESTING:
        return True
    return modules[service].check_validity(id)
