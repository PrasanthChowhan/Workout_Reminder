def replace_none_with_empty_string(input_dict):
    for key, value in input_dict.items():
        if value is None:
            input_dict[key] = ''
    return input_dict