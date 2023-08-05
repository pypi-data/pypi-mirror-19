
import json
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import (
    Model,
    # Model Types
    # docs: https://docs.djangoproject.com/en/dev/ref/models/fields/#lowercasename
    BooleanField, #
    NullBooleanField, #
    CommaSeparatedIntegerField, #
    EmailField, # max_length
    IPAddressField, #
    GenericIPAddressField, #
    URLField, # max_length=200
    FileField, # upload_to max_length=100
    ImageField, # upload_to max_length=100
    CharField, # max_length
    TextField, #
    DateField, # auto_now=False auto_now_add=False
    DateTimeField, # auto_now=False auto_now_add=False
    TimeField, # auto_now=False auto_now_add=False
    BigIntegerField, #
    DecimalField, # max_digits decimal_places
    FloatField,
    IntegerField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    SmallIntegerField,
    ForeignKey, #(Other) # Use a string name if Other is not yet defined.
    ManyToManyField, #(Other)
    OneToOneField, #(Other) # You need only specify one side of the relationship.
    ManyToManyRel,
)

class JSONable:
    @classmethod
    def from_json_dict(
            cls, 
            dictionary, 
            json_attributes = None,
            whitelist = [],
            blacklist = []):
        if json_attributes == None:
            json_attributes = cls.json_attributes
        json_attributes = list(
            set(json_attributes).union(set(whitelist)) - 
            set(blacklist))
        foreign_keys = {}
        attributes = {}
        for key in json_attributes:
            if key[-4:] == '_set' and \
               key[:-4] + 's' in dictionary:
                key_name = key[:-4] + 's'
                if type(cls.__dict__[key].rel) is ManyToManyRel:
                    RelatedModel = cls.__dict__[key].rel.model
                else:
                    RelatedModel = cls.__dict__[key].rel.related_model
                foreign_keys[key] = (
                    RelatedModel,
                    dictionary[key_name])
            if key in dictionary or \
               (key[-5:] == '_json' and 
                key[:-5] in dictionary):

                if key[-5:] == '_json':
                    key_name = key[:-5]
                    attributes[key_name + '_json_string'] = json.dumps(dictionary[key_name])
                else:
                    attributes[key] = dictionary[key]

        try:
            model = cls.objects.get(id = attributes.get('id'))
            cls.objects.filter(id = attributes['id']).update(**attributes)
            model = cls.objects.get(id = attributes.get('id'))
        except ObjectDoesNotExist:
            model = cls(**attributes)
            model.save()
        for key in foreign_keys:
            (RelatedModel, model_jsons) = foreign_keys[key]
            getattr(model, key).set([
                RelatedModel.from_json_dict(model_json)
                for model_json in model_jsons])
        return model

    def as_json_dict(
            self, 
            json_attributes = None,
            whitelist = [],
            blacklist = [],
            include_deleted = False):
        if json_attributes == None:
            json_attributes = self.json_attributes
        json_attributes = list(
            set(json_attributes).union(set(whitelist)) - 
            set(blacklist))
        dictionary = {}
        for key in json_attributes:
            if key[-4:] == '_set':
                if include_deleted:
                    objects = getattr(self, key).all()
                else:
                    objects = getattr(self, key)
                    if hasattr(objects.model, 'deleted'):
                        objects = objects.filter(deleted = False)
                    objects = objects.all()
                dictionary[key[:-4] + 's'] = list(map(
                    (lambda thing: thing.as_json_dict(
                        include_deleted = include_deleted)),
                    objects))
            else:
                if key[-5:] == '_json':
                    key_name = key[:-5]
                    dictionary[key_name] = \
                        json.loads(self.__dict__[key_name + '_json_string'])
                else:
                    dictionary[key] = self.__dict__[key]

                    if type(dictionary[key]) == ImageField:
                        # TODO
                        pass
        
        # Convert datetimes to strings
        for attribute in dictionary.keys():
            if dictionary[attribute].__class__ == datetime.datetime:
                dictionary[attribute] = str(dictionary[attribute])
        
        return dictionary
    
    def as_json(
            self, 
            json_attributes = None,
            whitelist = [],
            blacklist = [],
            include_deleted = False):
        dictionary = self.as_json_dict(
            json_attributes,
            whitelist,
            blacklist,
            include_deleted)
        return json.dumps(dictionary)
    
    @classmethod
    def all_as_json_dicts(
            self,
            json_attributes = None,
            whitelist = [],
            blacklist = [],
            include_deleted = False):
        if include_deleted or not hasattr(self, 'undeleted'):
            objects = self.objects.all()
        else:
            objects = self.undeleted().all()
        return [ 
            jsonable.as_json_dict(
                json_attributes,
                whitelist,
                blacklist,
                include_deleted)
            for jsonable in objects ]
    
    @classmethod
    def all_as_json(
            self,
            json_attributes = None,
            whitelist = [],
            blacklist = [],
            include_deleted = False):
        return json.dumps(self.all_as_json_dicts(
            json_attributes, 
            whitelist, 
            blacklist,
            include_deleted))

    @classmethod
    def rename_keys(self, thing, rename):
        if type(thing) == dict:
            return {
                rename(key): self.rename_keys(thing[key], rename)
                for key in thing
            }
        elif type(thing) == list:
            return [
                self.rename_keys(item, rename)
                for item in thing ]
        else:
            return thing
