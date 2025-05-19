from flask import current_app

def register_template_context(app):
    """
    Register empty RBAC utility functions in the template context.
    This is a placeholder for future RBAC implementation.
    """
    @app.context_processor
    def inject_rbac_functions():
        return {
            # These functions always return True for now
            'has_role': lambda role_name: True,
            'has_permission': lambda permission_name: True,
        }
    