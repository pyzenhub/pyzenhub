"""ZenHub API Custom Exeptions."""


class ZenhubError(Exception):
    pass


class InvalidTokenError(ZenhubError):
    pass


class APILimitError(ZenhubError):
    pass


class NotFoundError(ZenhubError):
    pass
