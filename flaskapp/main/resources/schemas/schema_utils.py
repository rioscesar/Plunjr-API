def copy_dict_values_to_object_attrs(keys, source, dest):
    for key in keys:
        if key in source.keys():
            setattr(dest, key, source[key])