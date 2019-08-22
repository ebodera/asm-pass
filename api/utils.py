
#** Functions **#

def assert_keys(form, keys):
    """assert keys exists in the form"""
    assert isinstance(form, dict) and isinstance(keys, list)
    # ensure all keys are valid
    for key in keys:
        if key not in form:
            raise KeyError('invalid fields')
    # error if number of keys is off
    if len(keys) != len(form.keys()):
        raise KeyError('missing required fields')

def find_keys(form, keys):
    """retrieve keys if found, but do not error if missing"""
    assert isinstance(form, dict) and isinstance(keys, list)
    data = form.copy()
    # add keys if they are missing
    for key in keys:
        if key not in data:
            data[key] = None
    # ensure there are not any extra keys
    if len(keys) != len(form.keys()):
        raise KeyError('invalid fields')
