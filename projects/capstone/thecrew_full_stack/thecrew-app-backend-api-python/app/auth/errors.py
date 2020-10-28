"""Exceptions used for authentication and validation verification."""

__author__ = "Filipe Bezerra de Sousa"


class AuthError(Exception):
    """A standardized way to communicate auth failure modes."""
    def __init__(self, code, description, status_code):
        """Create a new instance of the :class:`AuthError.

        :param code: The error code name which identifies the error.
        :param description: The human-readable description of the error.
        :param status_code: The HTTP status code.
        """
        self.code = code
        self.description = description
        self.status_code = status_code

    def __repr__(self):
        """Simple string representation of the :class:`AuthError instance.

        :return: The string representation of this :class:`AuthError instance.
        """
        return f'<AuthError {self.code}: {self.description}>'
