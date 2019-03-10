import werkzeug.exceptions as exc


class TailLengthIsNegative(exc.BadRequest):
    description = '\'tail_length\' cannot be negative'


class TooManyParameters(exc.BadRequest):
    pass


class UnexpectedParameter(exc.BadRequest):
    pass


class UnexpectedParameterValue(exc.BadRequest):
    pass


class WhiskersLengthIsNegative(exc.BadRequest):
    description = '\'whiskers_length\' cannot be negative'
