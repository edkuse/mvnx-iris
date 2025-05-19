from flask import flash


def flash_success(message):
    """Flash a success message."""
    flash(message, 'success')

def flash_error(message):
    """Flash an error message."""
    flash(message, 'error')

def flash_info(message):
    """Flash an info message."""
    flash(message, 'info')

def flash_warning(message):
    """Flash a warning message."""
    flash(message, 'warning')
