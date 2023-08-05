# -*- coding: utf-8 -*-

# Json Schema生成工具请参考http://jsonschema.net/

import json
import jsonschema
from argparse import Namespace


def load_json_from_string (json_string):
    # demo_string = '{"a": 0, "b": 9.6, "c": "Hello World", "d": {"a": 4}}'
    return json.loads (json_string)


def dump_json_to_string (json_obj):
    return json.dumps (json_obj, sort_keys=True, encoding='utf-8', ensure_ascii=False)


def convert_json_data_to_python_object (json_data):
    """
    convert JSON data into a Python object
    :param json_data:
    :return:
    """
    # data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
    # x = convert_json_data_to_python_object(data)
    # print "Name=%s, Hometown Name=%s, Hometown Id=%s" % (x.name, x.hometown.name, x.hometown.id)
    return json.loads (json_data, object_hook=lambda d: Namespace (**d))


def validate_json_schema (json_instance, json_schema):
    try:
        jsonschema.validate (json_instance, json_schema)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, e.message
    except jsonschema.SchemaError as e:
        return False, e.message


def validate_json_schema2 (json_data_file, json_schema_file):
    schema = open (json_schema_file).read ()
    # print schema
    data_instance = open (json_data_file).read ()
    # print data_instance
    try:
        jsonschema.validate (json.loads (data_instance), json.loads (schema))
        return True, ""
    except jsonschema.ValidationError as e:
        return False, e.message
    except jsonschema.SchemaError as e:
        return False, e.message


def Test1():
    demo_string = '{"a": 0, "b": 9.6, "c": "Hello World", "d": {"a": 4}}'
    decoded_data = load_json_from_string (demo_string)

    print decoded_data
    print decoded_data['b']
    print decoded_data.keys ()
    print decoded_data['d']['a']

    target_string = dump_json_to_string (decoded_data)
    if demo_string == target_string:
        print "Equal."
    else:
        print "Not equal."

    # convert JSON data into a Python object
    data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
    x = convert_json_data_to_python_object (data)
    print "Name=%s, Hometown Name=%s, Hometown Id=%s" % (x.name, x.hometown.name, x.hometown.id)


def main():
    schema_file=r"C:\Python27\Lib\site-packages\CodeLibWrapper\RobotFrameworkSample\SampleData\Schema.json"
    json_file=r"C:\Python27\Lib\site-packages\CodeLibWrapper\RobotFrameworkSample\SampleData\Data.json"
    validate_json_schema2(json_file,schema_file)


if __name__ == '__main__':
    main()
