

class ValidationFault(Exception):
    pass


class AccessForbidden(ValidationFault):
    pass
