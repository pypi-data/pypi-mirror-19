import six


def pyrecursive(obj, f, transform_dict_keys=False, transform_dict_values=True, custom_rules=None):
    kwargs = {
        'f': f,
        'transform_dict_keys': transform_dict_keys,
        'transform_dict_values': transform_dict_values,
        'custom_rules': custom_rules,
    }

    if custom_rules:
        for custom_rule_type, custom_rule_function in custom_rules.items():
            if isinstance(obj, custom_rule_type):
                return custom_rule_function(obj)

    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if transform_dict_keys:
                key = pyrecursive(key, **kwargs)
            if transform_dict_values:
                value = pyrecursive(value, **kwargs)
            result[key] = value
        return result

    elif hasattr(obj, '__iter__') and not isinstance(obj, six.string_types):
        result = []
        for inner_obj in obj:
            result.append(pyrecursive(inner_obj, **kwargs))
        result = type(obj).__call__(result)  # Cast to proper (original) iterable type.
        return result

    else:
        return f(obj)
