from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField , PasswordField , SubmitField ,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from wtforms.fields.html5 import DateField




class Add_event(FlaskForm):
	name = StringField('Name',
		validators=[DataRequired(),Length(min=2,max=50)])

	content = TextAreaField('Description',
		validators=[DataRequired(),Length(min=2,max=500)])

	address = StringField('Address',
		validators=[DataRequired(),Length(min=2,max=100)])

	startDate = DateField('Start Date',
		validators=[DataRequired()],format='%Y-%m-%d')

	endDate = DateField('End Date',
		validators=[DataRequired()],format='%Y-%m-%d')


	category = SelectField('Category',validators=[DataRequired()], choices=[('Industry Conferences', 'Industry'), ('Private Events', 'Private'), ('Webinars', 'Webinars')])


	photo = FileField(validators=[FileRequired()])


	

	submit = SubmitField('GO')
