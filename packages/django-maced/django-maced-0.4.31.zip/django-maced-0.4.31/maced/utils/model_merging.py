# The original version of this code was written by xaralis and posted here: https://djangosnippets.org/snippets/2283/
# Some modifications were made by Keith Hostetler to reflect django changes since the original version was written
# and a few minor bug fixes and edge cases.
import sys
from django.db import transaction
from django.apps import apps
from django.db.models import Model
from django.contrib.contenttypes.fields import GenericForeignKey


def get_all_related_objects(MyModel):
    # Taken from https://docs.djangoproject.com/en/1.9/ref/models/meta/#migrating-from-the-old-api
    return [
        f for f in MyModel._meta.get_fields()
        if (f.one_to_many or f.one_to_one)
        and f.auto_created and not f.concrete
    ]


def get_all_related_many_to_many_objects(MyModel):
    # Taken from https://docs.djangoproject.com/en/1.9/ref/models/meta/#migrating-from-the-old-api
    return [
        f for f in MyModel._meta.get_fields(include_hidden=True)
        if f.many_to_many and f.auto_created
    ]


@transaction.atomic
def merge_model_objects(primary_object, original_alias_objects=None, keep_old=False):
    """
    Use this function to merge model objects (i.e. Users, Organizations, Polls,
    etc.) and migrate all of the related fields from the alias objects to the
    primary object.

    Usage:
    from django.contrib.auth.models import User
    primary_user = User.objects.get(email='good_email@example.com')
    duplicate_user = User.objects.get(email='good_email+duplicate@example.com')
    merge_model_objects(primary_user, duplicate_user)
    """
    if not isinstance(original_alias_objects, list):
        original_alias_objects = [original_alias_objects]

    # check that all aliases are the same class as primary one and that
    # they are subclass of model
    primary_class = primary_object.__class__

    if not issubclass(primary_class, Model):
        raise TypeError('Only django.db.models.Model subclasses can be merged')

    alias_objects = []

    for alias_object in original_alias_objects:
        if not isinstance(alias_object, primary_class):
            raise TypeError('Only models of same class can be merged')

        # If any alias_objects given were accidentally the primary_object, they will be ignored.
        # Merging oneself with oneself results in oneself.
        if primary_object != alias_object:
            alias_objects.append(alias_object)

    # Get a list of all GenericForeignKeys in all models
    # TODO: this is a bit of a hack, since the generics framework should provide a similar
    # method to the ForeignKey field for accessing the generic related fields.
    generic_fields = []

    # Get all models from all apps
    models = apps.get_models()

    for model in models:
        # I don't know if this is necessary, but the 2.7 version used iteritems for the filter and so I am preserving
        # it just in case. Some day I'll test it and see if it is necessary.
        if sys.version_info > (3, 0):
            for field_name, field in filter(lambda x: isinstance(x[1], GenericForeignKey), model.__dict__.items()):
                generic_fields.append(field)
        else:
            for field_name, field in filter(lambda x: isinstance(x[1], GenericForeignKey), model.__dict__.iteritems()):
                generic_fields.append(field)

    blank_local_fields = set([field.attname for field in primary_object._meta.local_fields if getattr(primary_object, field.attname) in [None, '']])

    # Loop through all alias objects and migrate their data to the primary object.
    for alias_object in alias_objects:
        # Migrate all foreign key references from alias object to primary object.
        for related_object in get_all_related_objects(alias_object):
            # The variable name on the alias_object model.
            alias_varname = related_object.get_accessor_name()
            # The variable name on the related model.
            obj_varname = related_object.field.name

            # Needed to add a check here. The original design was faulty if there was a OneToOneField not on the
            # alias_object directly and if that related_object was empty.
            if not hasattr(alias_object, alias_varname):
                break

            related_objects = getattr(alias_object, alias_varname)

            for obj in related_objects.all():
                setattr(obj, obj_varname, primary_object)
                obj.save()

        # Migrate all many to many references from alias object to primary object.
        for related_many_object in get_all_related_many_to_many_objects(alias_object):
            alias_varname = related_many_object.get_accessor_name()
            obj_varname = related_many_object.field.name

            if alias_varname is not None:
                # standard case
                related_many_objects = getattr(alias_object, alias_varname).all()
            else:
                # special case, symmetrical relation, no reverse accessor
                related_many_objects = getattr(alias_object, obj_varname).all()

            for obj in related_many_objects.all():
                getattr(obj, obj_varname).remove(alias_object)
                getattr(obj, obj_varname).add(primary_object)

        # Migrate all generic foreign key references from alias object to primary object.
        for field in generic_fields:
            filter_kwargs = {}
            filter_kwargs[field.fk_field] = alias_object._get_pk_val()
            filter_kwargs[field.ct_field] = field.get_content_type(alias_object)

            for generic_related_object in field.model.objects.filter(**filter_kwargs):
                setattr(generic_related_object, field.name, primary_object)
                generic_related_object.save()

        # Try to fill all missing values in primary object by values of duplicates
        filled_up = set()

        for field_name in blank_local_fields:
            val = getattr(alias_object, field_name)

            if val not in [None, '']:
                setattr(primary_object, field_name, val)
                filled_up.add(field_name)

        blank_local_fields -= filled_up

        if not keep_old:
            alias_object.delete()

    primary_object.save()

    return primary_object
