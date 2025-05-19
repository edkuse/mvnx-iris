from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class ProductIdeaForm(FlaskForm):
    """Form for creating and editing product ideas."""
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description')
    problem_statement = TextAreaField('Problem Statement')
    proposed_solution = TextAreaField('Proposed Solution')
    success_metrics = TextAreaField('Success Metrics')
    impact_level = SelectField('Impact Level', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('transformative', 'Transformative')
    ], default='medium')
    tags = StringField('Tags')
    status = SelectField('Status', choices=[
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('implemented', 'Implemented')
    ], default='draft')
