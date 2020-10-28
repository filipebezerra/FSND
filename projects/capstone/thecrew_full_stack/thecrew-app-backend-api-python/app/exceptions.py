"""Exceptions used for data validation."""

__author__ = "Filipe Bezerra de Sousa"


class ValidationError(ValueError):
    """Validation error holder.
    
    Each instance of a :class:`Validation` holds details about a single 
    validation error.
    """
    def __init__(self, field, code, description):
        """Consctruct a instance of a Validation error providing info about 
        the violated constraints.
        
        :param field: The name of the violated field.
        :param code: The error code name which identifies the violated constraint.
        :param description: The human-readable description of the violation.
        """
        self.field = field
        self.code = code
        self.description = description

    def __repr__(self):
        """Simple string representation of a movie instance.

        :return: The string representation of this movie.
        """
        return f'<ValidationError {self.field} {self.code}>'


class ValidationsError(Exception):
    """Validation error container.
    
    Each instance of a :class:`ValidationsError` contains one or more 
    instances of a :class:`Validation`.
    """
    def __init__(self, message, errors=[]):
        """Construct a instance of a Validations container.

        :param message: A generic description of the contained errors.
        :param errors: Initial list of :class:`ValidationError`.
        """
        self.message = message
        self.errors = errors if errors else []

    def add_error(self, field, code, description):
        """Add a new :class:`ValidationError` to the container.

        :param field: The name of the violated field.
        :param code: The error code name which identifies the violated constraint.
        :param description: The human-readable description of the violation.
        """
        self.errors.append(ValidationError(field, code, description))

    def has_errors(self):
        """Check if the container has at least one :class:`ValidationError`.
        
        :return: True if it has some error, False otherwise.
        """
        return bool(self.errors)

    def get_error(self, field, code):
        """Check if the container has at least one :class:`ValidationError`.
        
        :return: True if it has some error, False otherwise.
        """
        return next(
            filter(lambda x: x.field == field and x.code == code, self.errors),
            None)

    def __repr__(self):
        """Simple string representation of this validation errors container.

        :return: The string representation of this validation errors container.
        """
        return f'<ValidationsError {self.message}; errors={self.errors}>'
