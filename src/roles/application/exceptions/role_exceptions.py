class RoleApplicationError(Exception):
    """Base exception for role application errors."""


class RoleNotFoundApplicationError(RoleApplicationError):
    """Raised when a role is not found."""


class RoleConflictError(RoleApplicationError):
    """Raised when a role conflicts with an existing resource."""