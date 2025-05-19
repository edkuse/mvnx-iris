from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import bp
from .models import Epic, EpicStatus, PriorityLevel
from .services import EpicService
from iris.modules.auth.models import User
from iris.extensions import db
from iris.utils.helpers import flash_success
from datetime import datetime


@bp.route('/')
@login_required
def index():
    """List all epics."""
    # Get filter parameters
    status = request.args.get('status')
    priority = request.args.get('priority')
    tag = request.args.get('tag')
    
    # Base query
    query = Epic.query
    
    # Apply filters
    if status:
        query = query.filter(Epic.status == status)
    
    if priority:
        query = query.filter(Epic.priority == priority)
    
    # Get all epics first (for tag filtering)
    epics = query.all()
    
    # Filter by tag if specified
    if tag:
        epics = [epic for epic in epics if tag in epic.tags]
    
    # Get all available tags for the filter dropdown
    all_tags = EpicService.get_all_tags()
    
    return render_template(
        'epics/index.html',
        epics=epics,
        statuses=EpicStatus.values(),
        priorities=PriorityLevel.values(),
        all_tags=all_tags,
        current_filters={
            'status': status,
            'priority': priority,
            'tag': tag
        }
    )


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new epic."""
    if request.method == 'POST':
        form_errors = {}
        
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', EpicStatus.DRAFT)
        priority = request.form.get('priority', PriorityLevel.MEDIUM)
        assigned_to_id = request.form.get('assigned_to_id')
        start_date_str = request.form.get('start_date')
        target_date_str = request.form.get('target_date')
        business_value = request.form.get('business_value', '').strip()
        acceptance_criteria = request.form.get('acceptance_criteria', '').strip()
        estimated_effort = request.form.get('estimated_effort')
        tags_str = request.form.get('tags', '').strip()
        
        # Validate required fields
        if not title:
            form_errors['title'] = 'Title is required'
        
        # Convert assigned_to_id
        assigned_to = None
        if assigned_to_id:
            assigned_to = User.query.get(assigned_to_id)
        
        # Convert dates
        start_date = None
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                form_errors['start_date'] = 'Invalid date format'
        
        target_date = None
        if target_date_str:
            try:
                target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
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
                'epics/form.html',
                epic=None,
                statuses=EpicStatus.values(),
                priorities=PriorityLevel.values(),
                users=users,
                form_errors=form_errors
            )
        
        # Create new epic
        epic = Epic(
            title=title,
            description=description,
            status=status,
            priority=priority,
            created_by=current_user,
            assigned_to=assigned_to,
            start_date=start_date,
            target_date=target_date,
            business_value=business_value,
            acceptance_criteria=acceptance_criteria,
            estimated_effort=effort
        )
        
        # Set tags
        epic.tags = tags
        
        # Save to database
        db.session.add(epic)
        db.session.commit()
        
        flash_success('Epic created successfully!')
        return redirect(url_for('epics.view', id=epic.id))
    
    # GET request - render form
    users = User.query.all()
    return render_template(
        'epics/form.html',
        epic=None,
        statuses=EpicStatus.values(),
        priorities=PriorityLevel.values(),
        users=users,
        form_errors={}
    )


@bp.route('/<int:id>')
@login_required
def view(id):
    """View an epic."""
    epic = Epic.query.get_or_404(id)
    return render_template('epics/view.html', epic=epic)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit an epic."""
    epic = Epic.query.get_or_404(id)
    
    if request.method == 'POST':
        form_errors = {}
        
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        status = request.form.get('status', EpicStatus.DRAFT)
        priority = request.form.get('priority', PriorityLevel.MEDIUM)
        assigned_to_id = request.form.get('assigned_to_id')
        start_date_str = request.form.get('start_date')
        target_date_str = request.form.get('target_date')
        business_value = request.form.get('business_value', '').strip()
        acceptance_criteria = request.form.get('acceptance_criteria', '').strip()
        estimated_effort = request.form.get('estimated_effort')
        tags_str = request.form.get('tags', '').strip()
        
        # Validate required fields
        if not title:
            form_errors['title'] = 'Title is required'
        
        # Convert assigned_to_id
        assigned_to = None
        if assigned_to_id:
            assigned_to = User.query.get(assigned_to_id)
        
        # Convert dates
        start_date = None
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            except ValueError:
                form_errors['start_date'] = 'Invalid date format'
        
        target_date = None
        if target_date_str:
            try:
                target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
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
                'epics/form.html',
                epic=epic,
                statuses=EpicStatus.values(),
                priorities=PriorityLevel.values(),
                users=users,
                form_errors=form_errors
            )
        
        # Update epic
        epic.title = title
        epic.description = description
        epic.status = status
        epic.priority = priority
        epic.assigned_to = assigned_to
        epic.start_date = start_date
        epic.target_date = target_date
        epic.business_value = business_value
        epic.acceptance_criteria = acceptance_criteria
        epic.estimated_effort = effort
        epic.tags = tags
        
        # Save to database
        db.session.commit()
        
        flash_success('Epic updated successfully!')
        return redirect(url_for('epics.view', id=epic.id))
    
    # GET request - render form
    users = User.query.all()
    return render_template(
        'epics/form.html',
        epic=epic,
        statuses=EpicStatus.values(),
        priorities=PriorityLevel.values(),
        users=users,
        form_errors={}
    )


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete an epic."""
    epic = Epic.query.get_or_404(id)
    
    db.session.delete(epic)
    db.session.commit()
    
    flash_success('Epic deleted successfully!')
    return redirect(url_for('epics.index'))


@bp.route('/api/tags')
@login_required
def get_tags():
    """API endpoint to get all tags."""
    tags = EpicService.get_all_tags()
    return tags
