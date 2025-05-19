from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import bp
from .models import ProductIdea, ProductIdeaStatus, PriorityLevel, ImpactLevel
from .services import ProductIdeaService
from iris.modules.auth.models import User
from iris.extensions import db
from iris.utils.helpers import flash_success
from datetime import datetime


@bp.route('/')
@login_required
def index():
    """List all product ideas."""
    # Get filter parameters
    status = request.args.get('status')
    priority = request.args.get('priority')
    impact = request.args.get('impact')
    tag = request.args.get('tag')
    
    # Base query
    query = ProductIdea.query
    
    # Apply filters
    if status:
        try:
            query = query.filter(ProductIdea.status == status)
        except KeyError:
            pass
    
    if priority:
        try:
            query = query.filter(ProductIdea.priority == priority)
        except KeyError:
            pass
    
    if impact:
        try:
            query = query.filter(ProductIdea.impact_level == impact)
        except KeyError:
            pass
    
    # Get all ideas first (for tag filtering)
    ideas = query.all()
    
    # Filter by tag if specified
    if tag:
        ideas = [idea for idea in ideas if tag in idea.tags]
    
    # Get all available tags for the filter dropdown
    all_tags = ProductIdeaService.get_all_tags()
    
    return render_template(
        'product_ideas/index.html',
        ideas=ideas,
        statuses=ProductIdeaStatus.values(),
        priorities=PriorityLevel.values(),
        impacts=ImpactLevel.values(),
        all_tags=all_tags,
        current_filters={
            'status': status,
            'priority': priority,
            'impact': impact,
            'tag': tag
        }
    )

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new product idea."""
    if request.method == 'POST':
        form_errors = {}
        
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status_name = request.form.get('status', 'DRAFT')
        priority_name = request.form.get('priority', 'MEDIUM')
        impact_name = request.form.get('impact_level', 'MODERATE')
        assigned_to_id = request.form.get('assigned_to_id')
        target_date_str = request.form.get('target_date')
        business_value = request.form.get('business_value', '').strip()
        technical_feasibility = request.form.get('technical_feasibility', '').strip()
        estimated_effort = request.form.get('estimated_effort')
        tags_str = request.form.get('tags', '').strip()
        
        # Validate required fields
        if not title:
            form_errors['title'] = 'Title is required'
        
        # Convert enums
        try:
            status = getattr(ProductIdeaStatus, status_name.upper())
        except KeyError:
            status = ProductIdeaStatus.DRAFT
            form_errors['status'] = f'Invalid status: {status_name}'
        
        try:
            priority = getattr(PriorityLevel, priority_name.upper())
        except KeyError:
            priority = PriorityLevel.LOW
            form_errors['priority'] = f'Invalid priority: {priority_name}'
        
        try:
            impact_level = getattr(ImpactLevel, impact_name.upper())
        except KeyError:
            impact_level = ImpactLevel.MODERATE
            form_errors['impact_level'] = f'Invalid impact level: {impact_name}'
        
        # Convert assigned_to_id
        assigned_to = None
        if assigned_to_id:
            assigned_to = User.query.get(assigned_to_id)
        
        # Convert target_date
        target_date = None
        if target_date_str:
            try:
                target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
            except ValueError:
                form_errors['target_date'] = 'Invalid date format'
        
        # Convert estimated_effort
        effort = None
        if estimated_effort:
            try:
                effort = int(estimated_effort)
                if effort < 0:
                    form_errors['estimated_effort'] = 'Effort must be a positive number'
            except ValueError:
                form_errors['estimated_effort'] = 'Effort must be a number'
        
        # Process tags
        tags = []
        if tags_str:
            tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        # If there are errors, re-render the form
        if form_errors:
            users = User.query.all()
            return render_template(
                'product_ideas/form.html',
                idea=None,
                statuses=ProductIdeaStatus.values(),
                priorities=PriorityLevel.values(),
                impacts=ImpactLevel.values(),
                users=users,
                form_errors=form_errors
            )
        
        # Create new product idea
        idea = ProductIdea(
            title=title,
            description=description,
            status=status,
            priority=priority,
            impact_level=impact_level,
            created_by=current_user,
            assigned_to=assigned_to,
            target_date=target_date,
            business_value=business_value,
            technical_feasibility=technical_feasibility,
            estimated_effort=effort
        )
        
        # Set tags
        idea.tags = tags
        
        # Save to database
        db.session.add(idea)
        db.session.commit()
        
        flash_success('Product idea created successfully!')
        return redirect(url_for('product_ideas.view', id=idea.id))
    
    # GET request - render form
    users = User.query.all()
    return render_template(
        'product_ideas/form.html',
        idea=None,
        statuses=ProductIdeaStatus.values(),
        priorities=PriorityLevel.values(),
        impacts=ImpactLevel.values(),
        users=users,
        form_errors={}
    )


@bp.route('/<int:id>')
@login_required
def view(id):
    """View a product idea."""
    idea = ProductIdea.query.get_or_404(id)
    return render_template('product_ideas/view.html', idea=idea)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a product idea."""
    idea = ProductIdea.query.get_or_404(id)
    
    if request.method == 'POST':
        form_errors = {}
        
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status_name = request.form.get('status', 'DRAFT')
        priority_name = request.form.get('priority', 'MEDIUM')
        impact_name = request.form.get('impact_level', 'MODERATE')
        assigned_to_id = request.form.get('assigned_to_id')
        target_date_str = request.form.get('target_date')
        business_value = request.form.get('business_value', '').strip()
        technical_feasibility = request.form.get('technical_feasibility', '').strip()
        estimated_effort = request.form.get('estimated_effort')
        tags_str = request.form.get('tags', '').strip()
        
        # Validate required fields
        if not title:
            form_errors['title'] = 'Title is required'
        
        # Convert enums
        try:
            status = getattr(ProductIdeaStatus, status_name.upper())
        except KeyError:
            status = ProductIdeaStatus.DRAFT
            form_errors['status'] = f'Invalid status: {status_name}'
        
        try:
            priority = getattr(PriorityLevel, priority_name.upper())
        except KeyError:
            priority = PriorityLevel.MEDIUM
            form_errors['priority'] = f'Invalid priority: {priority_name}'
        
        try:
            impact_level = getattr(ImpactLevel, impact_name.upper())
        except KeyError:
            impact_level = ImpactLevel.MODERATE
            form_errors['impact_level'] = f'Invalid impact level: {impact_name}'
        
        # Convert assigned_to_id
        assigned_to = None
        if assigned_to_id:
            assigned_to = User.query.get(assigned_to_id)
        
        # Convert target_date
        target_date = None
        if target_date_str:
            try:
                target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
            except ValueError:
                form_errors['target_date'] = 'Invalid date format'
        
        # Convert estimated_effort
        effort = None
        if estimated_effort:
            try:
                effort = int(estimated_effort)
                if effort < 0:
                    form_errors['estimated_effort'] = 'Effort must be a positive number'
            except ValueError:
                form_errors['estimated_effort'] = 'Effort must be a number'
        
        # Process tags
        tags = []
        if tags_str:
            tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        # If there are errors, re-render the form
        if form_errors:
            users = User.query.all()
            return render_template(
                'product_ideas/form.html',
                idea=idea,
                statuses=ProductIdeaStatus.values(),
                priorities=PriorityLevel.values(),
                impacts=ImpactLevel.values(),
                users=users,
                form_errors=form_errors
            )
        
        # Update product idea
        idea.title = title
        idea.description = description
        idea.status = status
        idea.priority = priority
        idea.impact_level = impact_level
        idea.assigned_to = assigned_to
        idea.target_date = target_date
        idea.business_value = business_value
        idea.technical_feasibility = technical_feasibility
        idea.estimated_effort = effort
        idea.tags = tags
        
        # Save to database
        db.session.commit()
        
        flash_success('Product idea updated successfully!')
        return redirect(url_for('product_ideas.view', id=idea.id))
    
    # GET request - render form
    users = User.query.all()
    return render_template(
        'product_ideas/form.html',
        idea=idea,
        statuses=ProductIdeaStatus.values(),
        priorities=PriorityLevel.values(),
        impacts=ImpactLevel.values(),
        users=users,
        form_errors={}
    )


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a product idea."""
    idea = ProductIdea.query.get_or_404(id)
    
    db.session.delete(idea)
    db.session.commit()
    
    flash_success('Product idea deleted successfully!')
    return redirect(url_for('product_ideas.index'))


@bp.route('/api/tags')
@login_required
def get_tags():
    """API endpoint to get all tags."""
    tags = ProductIdeaService.get_all_tags()
    return tags
