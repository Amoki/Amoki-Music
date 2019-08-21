from rest_framework import serializers
from rest_framework.utils import model_meta

def bind_parents_on_create(Cls):
    class WrappedClass(Cls):
        def create(self, validated_data):
            if hasattr(self, "parent_save_kwargs"):
                kwargs = {
                    self.parent_save_kwargs.get(key, key): value
                    for key, value in self.context["view"].kwargs.items()
                }
            else:
                kwargs = {
                    key.replace("_pk", ""): value
                    for key, value in self.context["view"].kwargs.items()
                }
            info = model_meta.get_field_info(self.Meta.model)
            for field_name, relation_info in info.relations.items():
                if relation_info.related_model and field_name in kwargs:
                    validated_data[f"{field_name}_id"] = kwargs[field_name]
            return super().create(validated_data)

    WrappedClass.__name__ = Cls.__name__
    return WrappedClass


class ScopeLimitedMixin:
    """
    Limit FK queryset with parent_lookup_kwargs
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = {}
        if hasattr(self.context["view"], "parent_lookup_kwargs"):
            for kwarg, field in self.context["view"].parent_lookup_kwargs.items():
                filters[field] = self.context["view"].kwargs.get(kwarg)

        return queryset.filter(**filters)


class ScopeLimitedPKRelatedField(ScopeLimitedMixin, serializers.PrimaryKeyRelatedField):
    pass