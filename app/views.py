from flask import request, abort, Blueprint, render_template
from app.models import Employee, Position, Division, Job
from app import db
from flask_login import login_required, current_user

bp = Blueprint('bp', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('employees.html', name=current_user.name)

@bp.route('/employees', methods=['GET'])
@login_required
def get_employees_list():
    employees_query = Employee.query.join(Job).order_by(Job.date_of_employment)
    if not employees_query:
        abort(404)
    else:
        if request.args.get('division_id'):
            employees_query = employees_query.filter(Job.division_id == request.args.get('division_id'))
        elif request.args.get('employment_after_date'):
            employees_query = employees_query.filter(Job.date_of_employment > request.args.get('employment_after_date'))
        employees = employees_query.all()
        return render_template("employees.html", name=current_user.name, list_of_employees=employees)