import json

from snapp_email.datacontract import classes
from snapp_email.datacontract import iterable_object_mappings


PRIMITIVE_TYPES = ['string', 'integer', 'float', 'double', 'long', 'boolean', 'dateTime']
PRIMITIVE_LIST_TYPES = ['ListOfStrings', 'list']

PYTHON_PRIMITIVE_TYPES = ['str', 'int', 'float', 'double', 'long', 'long']


def get_all_class_members(cls):
    """
    Returns a list of all class members (attributes) including the ones from the inherited class(es).
    """
    members = cls.member_data_items_
    if cls.superclass is not None:
        parent = get_all_class_members(cls.superclass)
        # return {**members, **parent}  # Python 3.5+
        merged = parent.copy()
        merged.update(members)
        return merged
    return members


def export_dict(obj, self_type=None):
    """
    :param obj:
    :param self_type:
    :return:
    """
    try:
        # members = obj.member_data_items_
        members = get_all_class_members(obj)
    except AttributeError:
        return obj

    d = {}
    for member_spec in members.values():
        val = getattr(obj, member_spec.name)
        if val is None:
            continue

        if member_spec.data_type.startswith("ListOf") and 'Page' not in member_spec.data_type:
            if member_spec.data_type in PRIMITIVE_LIST_TYPES:
                d[member_spec.name] = val
            else:
                """
                # This should work, but does not because of how XSD is written
                iterable_attr = getattr(val, member_spec.name)
                encoded = [export_dict(x, type(x).__name__) for x in iterable_attr]
                d[member_spec.name] = encoded
                """

                # Get the iterable attribute through the ListOf wrapper object
                iterable_object_name = member_spec.data_type
                iter_objs = iterable_object_mappings.iterable_details
                iter_obj_attribute_name, iter_obj_attribute_type = iter_objs[iterable_object_name]
                iterable_attr = getattr(val, iter_obj_attribute_name)

                encoded = [export_dict(x, type(x).__name__) for x in iterable_attr]
                d[member_spec.name] = encoded
        else:
            encoded = export_dict(val, member_spec.data_type)
            if type(encoded) is dict:
                pass
                # d['$type'] = member_spec.data_type
                # encoded['$type'] = member_spec.data_type
            d[member_spec.name] = encoded

    if self_type is not None:
        d['$type'] = self_type

    return d


def find_type(cls, attribute_name):
    """
    Returns type (as string) of attribute in a given class.
    """
    for _, attr in cls.member_data_items_.items():
        # print(attr.get_name(), attr.get_data_type())
        if attr.get_name() == attribute_name:
            return attr.get_data_type()

    if hasattr(cls, 'superclass') and cls.superclass is not None:
        return find_type(cls.superclass, attribute_name)

    return None


def fill(cls, data):
    """
    :param cls:
    :param data:
    :return:
    """
    if type(cls).__name__ in PYTHON_PRIMITIVE_TYPES or type(data).__name__ in PYTHON_PRIMITIVE_TYPES or type(data) is list:
        return data

    instance = None
    if '$type' in data:
        cls = getattr(classes, data['$type'])
        instance = cls()
    else:
        instance = cls()

    for (attr_name, attr_value) in data.items():
        if attr_name == '$type':
            continue

        attr_type_name = find_type(cls, attr_name)
        if attr_type_name.__class__.__name__ == 'NoneType' or attr_type_name is None:
            print("Type missing", type(cls), attr_name)

        try:
            attr_setter_method = getattr(instance, 'set_' + attr_name)
        except AttributeError as e:
            raise
            # pass

        if attr_type_name in PRIMITIVE_TYPES or attr_type_name in PRIMITIVE_LIST_TYPES or attr_type_name in PYTHON_PRIMITIVE_TYPES:
            attr_setter_method(attr_value)
        elif attr_type_name.startswith('ListOf') and 'Page' not in attr_type_name:  # ListOfX_*, but not ListOfXPage_*
            # This should work, but does not because of how XSD is written
            # attr_setter_method([fill(getattr(dc_classes, d['$type']), d) for d in attr_value])
            intermediate_object_type = getattr(classes, attr_type_name)
            iter_objs = iterable_object_mappings.iterable_details
            iter_obj_attribute_name, iter_obj_attribute_type = iter_objs[attr_type_name]
            actual_list = [
                fill(getattr(classes, d['$type'] if '$type' in d else iter_obj_attribute_type), d)
                for d in attr_value
            ]
            try:
                intermediate_object = intermediate_object_type(**{iter_obj_attribute_name: actual_list})
            except TypeError:
                raise
            attr_setter_method(intermediate_object)
        else:
            attr_type = getattr(classes, attr_type_name)
            obj = fill(attr_type, attr_value)
            attr_setter_method(obj)

    return instance


def to_json(x, indent=None):
    return json.dumps(export_dict(x), indent=indent)


def to_pretty_json(x):
    return to_json(x, indent=4)
