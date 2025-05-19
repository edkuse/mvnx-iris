from flask import Flask
from iris.config import Config
from iris.extensions import csrf, db, migrate, login_manager, session
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    session.init_app(app)
    
    # Register blueprints
    from iris.modules.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from iris.modules.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from iris.modules.product_ideas import bp as product_ideas_bp
    app.register_blueprint(product_ideas_bp)
    
    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    return app

# Import at the bottom to avoid circular imports
from flask import render_template
