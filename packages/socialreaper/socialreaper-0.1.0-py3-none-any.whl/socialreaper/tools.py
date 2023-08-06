import requests
import json
import csv
from os import path, mkdir
import collections


def flatten(dictionary, parent_key=False, separator='.'):
    """
    Turn a nested dictionary into a flattened dictionary
    :param dictionary:
    :param parent_key:
    :param separator: The string used to separate flattened keys
    :return:
    """

    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            items.append((new_key, str(value)))
        else:
            items.append((new_key, value))
    return dict(items)


def fill_gaps(list_dicts):
    field_names = []  # != set bc. preserving order is better for output
    for datum in list_dicts:
        for key in datum.keys():
            if key not in field_names:
                field_names.append(key)
    for datum in list_dicts:
        for key in field_names:
            if key not in datum:
                datum[key] = ''
    return list(field_names), list_dicts


def to_csv(data, field_names=None, filename='data.csv',
           overwrite=True,
           write_headers=True, append=False, flat=True,
           primary_fields=None, sort_fields=True):
    """
    Write a list of dicts to a csv file

    :param data: List of dicts
    :param field_names: The list column names
    :param filename: The name of the file
    :param overwrite: Overwrite the file if exists
    :param write_headers: Write the headers to the csv file
    :param append: Write new rows if the file exists
    :param flat: Flatten the dictionary before saving
    :param primary_fields: The first columns of the csv file
    :param sort_fields: Sort the field names alphabetically
    :return: None
    """

    # Don't overwrite if not specified
    if not overwrite and path.isfile(filename):
        raise FileExistsError('The file already exists')

    # Replace file if append not specified
    write_type = 'w' if not append else 'a'

    # Flatten if flat is specified, or there are no predefined field names
    if flat or not field_names:
        data = [flatten(datum) for datum in data]

    # Fill in gaps between dicts with empty string
    if not field_names:
        field_names, data = fill_gaps(data)

    # Sort fields if specified
    if sort_fields:
        field_names.sort()

    # If there are primary fields, move the field names to the front and sort
    #  based on first field
    if primary_fields:
        for key in primary_fields[::-1]:
            field_names.insert(0, field_names.pop(field_names.index(key)))

        data = sorted(data, key=lambda k: k[field_names[0]], reverse=True)

    # Write the file
    with open(filename, write_type) as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        if not append or write_headers:
            writer.writeheader()

        # Write rows containing fields in field names
        for datum in data:
            for key in list(datum.keys()):
                if key not in field_names:
                    del datum[key]
                elif type(datum[key]) is str:
                    datum[key] = datum[key].strip()

            writer.writerow(datum)


def to_json(data, filename='data.json', indent=4):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, indent=indent))


def save_file(filename, source, folder="Downloads"):
    r = requests.get(source, stream=True)
    if r.status_code == 200:
        if not path.isdir(folder):
            mkdir(folder)
        with open("%s/%s" % (folder, filename), 'wb') as f:
            for chunk in r:
                f.write(chunk)
