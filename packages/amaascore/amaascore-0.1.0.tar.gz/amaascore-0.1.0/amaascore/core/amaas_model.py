import datetime
from decimal import Decimal
import json


def json_handler(value):
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, AMaaSModel):
        return value.to_json()
    raise TypeError("JSON Handler Failed on value '%s': Unknown type '%s'" % (value, type(value)))


def to_json(dict_to_convert):
    return json.loads(json.dumps(dict_to_convert, ensure_ascii=False, default=json_handler, indent=4,
                                 separators=(',', ': ')))


class AMaaSModel(object):

    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.get('created_by') or 'TEMP'  # Should come from logged in user
        self.updated_by = kwargs.get('updated_by') or 'TEMP'  # Should come from logged in user
        self.created_time = kwargs.get('created_time')  # Comes from database
        self.updated_time = kwargs.get('updated_time')  # Comes from database
        self.internal_id = kwargs.get('internal_id')  # The internal ID of the transaction from the database

    def to_json(self):
        return to_json(self.__dict__)

    def __repr__(self):
        """
        # TODO - check the nested dictionaries
        :return:
        """
        return str(self.__dict__)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            # Strip out the database generated fields:
            my_dict = self.__dict__
            other_dict = other.__dict__
            return my_dict == other_dict
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        output = []
        for (key, value) in self.__dict__.items():
            output_value = hash(tuple(sorted(value))) if isinstance(value, dict) else value
            output.append((key, output_value))
        return hash(tuple(sorted(output)))

