import wg_forge_api_exceptions as _exc


GET_CATS_VALID_PARAMETERS = (
    'attribute',
    'limit',
    'offset',
    'order',
)

CATS_VALID_ATTRIBUTES = (
    'name',
    'color',
    'tail_length',
    'whiskers_length',
)


def _validate_cats_select_kwar(key, value):
    """
    Stupid implementation of KV-parameter checking.
    :param key: Name of parameter to be validated.
    :param value: Value of parameter to be validated.
    :return: None
    """
    if key == 'attribute' and value not in CATS_VALID_ATTRIBUTES and value != '1':
        raise _exc.UnexpectedParameterValue(f'Got unexpected value {value!r} of {key!r} parameter')

    # Ensure LIMIT and OFFSET are non-negative integers.
    if (key == 'limit' and value.upper() != 'ALL') or key == 'offset':
        try:
            value = float(value)
            if value % 1 or value < 0:
                raise ValueError
        except ValueError:
            raise _exc.UnexpectedParameterValue(f'Got unexpected value {value!r} of {key!r} parameter')

    if key == 'order' and value.upper() not in ('ASC', 'DESC'):
        raise _exc.UnexpectedParameterValue(f'Got unexpected value {value!r} of {key!r} parameter')


def validate_cats_select_parameters(params):
    """
    Ensures all parameters given in request make sense to the server.
    :param params: Parameters extracted from request URL.
    :return: None
    """
    if len(params) > 4:
        raise _exc.TooManyParameters(f'The cat request takes up to 4 parameters, got {len(params)}')

    # Loop over given parameters to ensure they are valid.
    for p, v in params.items():
        if p not in GET_CATS_VALID_PARAMETERS:
            raise _exc.UnexpectedParameter(f'Got unexpected parameter {p!r}')

        # Values checking implemented within the loop to speed up the procedure.
        _validate_cats_select_kwar(p, v)


def validate_cat_tail_and_whiskers(cat_dict):
    """
    Ensures both tail and whiskers length of cat have not negative values.
    :param cat_dict: Cat description retrieved from request.
    :return: None
    """
    if cat_dict['tail_length'] < 0:
        raise _exc.TailLengthIsNegative
    if cat_dict['whiskers_length'] < 0:
        raise _exc.WhiskersLengthIsNegative


def validate_no_extra_parameters(cat_dict):
    if len(cat_dict) > 4:
        extra_params = ['\'' + k + '\'' for k in cat_dict.keys() if k.lower() not in CATS_VALID_ATTRIBUTES]
        extra_params_as_string = ', '.join(extra_params)
        raise _exc.TooManyParameters(f'Got unexpected parameter(s) {extra_params_as_string}')
