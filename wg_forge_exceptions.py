import werkzeug.exceptions as exc


class TailLengthIsNegative(exc.BadRequest):
    message = 'tail_length cannot be negative'


class WhiskersLengthIsNegative(exc.BadRequest):
    message = 'whiskers_length cannot be negative'
