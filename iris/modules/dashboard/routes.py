from flask import render_template
from flask_login import login_required, current_user
from . import bp
from .services import DashboardService


@bp.route('/')
@login_required
def index():
    """Dashboard home page."""
    # Get product idea statistics
    product_idea_stats = DashboardService.get_product_idea_stats()
    
    # Get recent product ideas
    recent_product_ideas = DashboardService.get_recent_product_ideas(limit=5)
    
    # Get user's product ideas
    user_product_ideas = []
    if current_user.is_authenticated:
        user_product_ideas = DashboardService.get_user_product_ideas(current_user.id, limit=5)
    
    return render_template(
        'index.html',
        product_idea_stats=product_idea_stats,
        recent_product_ideas=recent_product_ideas,
        user_product_ideas=user_product_ideas
    )
