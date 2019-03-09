import werkzeug.exceptions as exc


class TailLengthIsNegative(exc.BadRequest):
    message = '<p>tail_length cannot be negative</p>'


class WhiskersLengthIsNegative(exc.BadRequest):
    message = '<p>whiskers_length cannot be negative</p>'
