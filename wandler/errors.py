class WandlerError(Exception):
    """Base exception for Wandler operations"""
    pass

class ConfigError(WandlerError):
    """Configuration-related errors"""
    pass

class TaskError(WandlerError):
    """Task execution errors"""
    pass