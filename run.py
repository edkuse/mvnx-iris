from iris.app import create_app
from flask_login import current_user
from datetime import datetime

app = create_app()

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.context_processor
def inject_user():
    return {'current_user': current_user}

# @app.shell_context_processor
# def make_shell_context():
#     return {
#         'db': db, 
#         'app': app,
#         # Import models for shell context
#         'User': __import__('iris.modules.auth.models').modules.auth.models.User,
#         'ProductIdea': __import__('iris.modules.product_ideas.models').modules.product_ideas.models.ProductIdea
#     }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
