from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
import ast
import secrets
import logging
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
secret_key = secrets.token_hex(128)
app.secret_key = secret_key
db = SQLAlchemy(app)
logging.basicConfig(level=logging.INFO)

# LOGIN MANAGER
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	return db.session.get(Admin, int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
	return redirect(url_for('login'))


# DATABASE MODELS
class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	courses = db.Relationship('Courses', backref='person')
	matric_num = db.Column(db.String(20), nullable=False)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	gender = db.Column(db.String(10), nullable=False)
	ITGY_402 = db.Column(db.Boolean, nullable=False, default=0)
	GEDS_420 = db.Column(db.Boolean, nullable=False, default=0)
	GEDS_420 = db.Column(db.Boolean, nullable=False, default=0)
	GEDS_400 = db.Column(db.Boolean, nullable=False, default=0)
	ITGY_408 = db.Column(db.Boolean, nullable=False, default=0)
	ITGY_312 = db.Column(db.Boolean, nullable=False, default=0)
	ITGY_402 = db.Column(db.Boolean, nullable=False, default=0)
	ITGY_406 = db.Column(db.Boolean, nullable=False, default=0)
	COSC_430 = db.Column(db.Boolean, nullable=False, default=0)
	GEDS_002 = db.Column(db.Boolean, nullable=False, default=0)
	GEDS_400 = db.Column(db.Boolean, nullable=False, default=0)


class Admin(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	role =db.Column(db.String, nullable=False, default='Lecturer')
	username = db.Column(db.String(50), nullable=False)
	password = db.Column(db.String(250), nullable=False)
	
	def __repr__(self):
		return f"{self.id}"
	
	def get_id(self):
		return str(self.id)

	def is_authenticated(self):
		exists = db.session.query(Admin).filter_by(username=self.username, password=self.password).first()
		return bool(exists)

class Courses(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	matric_num = db.Column(db.String(20), db.ForeignKey('person.matric_num'))
	GEDS_420 = db.Column(db.Integer, nullable=False, default=0)
	GEDS_400 = db.Column(db.Integer, nullable=False, default=0)
	ITGY_408 = db.Column(db.Integer, nullable=False, default=0)
	ITGY_312 = db.Column(db.Integer, nullable=False, default=0)
	ITGY_402 = db.Column(db.Integer, nullable=False, default=0)
	ITGY_406 = db.Column(db.Integer, nullable=False, default=0)
	COSC_430 = db.Column(db.Integer, nullable=False, default=0)
	GEDS_002 = db.Column(db.Integer, nullable=False, default=0)
	sick = db.Column(db.Integer, nullable=False, default=0)


# ROUTES

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

# LOGIN MANAGER


@app.route('/login', methods=['OPTIONS'])
def handle_options():
	response = app.make_default_options_response()
	response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
	return response


@app.route('/admin', methods=['GET'])
@login_required
def admin():
	if current_user.is_authenticated:
		return render_template('adminPage.html',user=current_user)
	else:
		return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		data = request.get_json()
		username = data.get('username')
		password = data.get('password')
		if authenticate(username, password):
			admin = db.session.query(Admin).filter_by(username=username).first()
			login_user(admin)
			print(session.items())
			return redirect(url_for('admin'))
		else:
			error = 'Invalid Login details'
			return render_template('login.html', error=error), 401
	elif request.method == 'GET':
		return render_template('login.html')


def authenticate(username, password):
	admin = Admin.query.filter_by(username=username).first()
	if admin:
		return bool(username == admin.username and check_password_hash( admin.password,password))
	return False

# MARK ATTENDANCE

@app.route('/attendance', methods=['POST', 'GET'])
def mark_attendance():
	"""Main attendnance function
	Post request is recieved from FE and json parsed and stored in db
	"""
	if request.method == 'POST':
		data = request.get_json()
		if len(data) == 1:
			matric_num = data['matricNum']
			exist = Person.query.filter_by(matric_num=matric_num).first()
			if exist:
				return jsonify({
					'id': exist.matric_num,
					"GEDS420": exist.GEDS_420,
					"GEDS400": exist.GEDS_400,
					"ITGY408": exist.ITGY_408,
					"ITGY312": exist.ITGY_312,
					"ITGY402": exist.ITGY_402,
					"ITGY406": exist.ITGY_406,
					"COSC430": exist.COSC_430,
					"GEDS002": exist.GEDS_002,
				})
			else:
				return jsonify({'message': f'Student {matric_num} not found'})

		matric_num = data['id']

		ITGY_402 = data.get("ITGY402", 0)
		GEDS_420 = data.get('GEDS420', 0)
		GEDS_400 = data.get('GEDS400', 0)
		ITGY_408 = data.get("ITGY408", 0)
		ITGY_312 = data.get('ITGY312', 0)
		ITGY_402 = data.get('ITGY402', 0)
		ITGY_406 = data.get('ITGY406', 0)
		COSC_430 = data.get('COSC430', 0)
		GEDS_002 = data.get('GEDS002', 0)
		sick = data.get('sick', 0)

	exist = Courses.query.filter_by(matric_num=matric_num).first()
	if not exist:
		return jsonify({'message': 'No user found'})
	else:
		exist.ITGY_402 += ITGY_402
		exist.GEDS_420 += GEDS_420
		exist.GEDS_400 += GEDS_400
		exist.ITGY_408 += ITGY_408
		exist.ITGY_312 += ITGY_312
		exist.ITGY_406 += ITGY_406
		exist.COSC_430 += COSC_430
		exist.GEDS_002 += GEDS_002
		exist.sick += sick
		db.session.commit()
		return {'message': f'Attendance record for {matric_num} updated'}

# CREATE USERS
@app.route('/register', methods=['POST', 'GET'])
def create_student():
	if request.method == 'GET':
		return render_template('RegistrationPage.html')
	data = request.get_json()
	matric_num = data['matricNum']
	first_name = data['fName'].strip().title()
	last_name = data['lName'].strip().title()
	gender = data['gender']
	ITGY_402 = data["ITGY_402"]
	GEDS_420 = data['GEDS_420']
	GEDS_400 = data['GEDS_400']
	ITGY_408 = data["ITGY_408"]
	ITGY_312 = data['ITGY_312']
	ITGY_402 = data['ITGY_402']
	ITGY_406 = data['ITGY_406']
	COSC_430 = data['COSC_430']
	GEDS_002 = data['GEDS_002']

	person = Person(
		matric_num=matric_num,
		first_name=first_name,
		last_name=last_name,
		ITGY_402=ITGY_402,
		GEDS_420=GEDS_420,
		GEDS_400=GEDS_400,
		ITGY_408=ITGY_408,
		ITGY_312=ITGY_312,
		ITGY_406=ITGY_406,
		COSC_430=COSC_430,
		GEDS_002=GEDS_002,
		gender=gender)

	courses = Courses(
		matric_num=matric_num,
		ITGY_402=0,
		GEDS_420=0,
		GEDS_400=0,
		ITGY_408=0,
		ITGY_312=0,
		ITGY_406=0,
		COSC_430=0,
		GEDS_002=0,
		sick=0
	)

	exists = Person.query.filter_by(matric_num=matric_num).first()
	if not exists:
		db.session.add(person)
		db.session.add(courses)
		db.session.commit()
		return jsonify({'message': 'Person created successfully'})
	else:
		return jsonify({'message': f"Student with matric {matric_num} already exists"})

@app.route('/signup',methods=['POST','GET'])
def create_admin():
	if request.method == 'POST':
		data = request.get_json()
		
		name = data.get('name',None)
		role = data.get('role',None)
		username = data.get('username',None)
		password = data.get('password',None)

		admin = Admin(
			name=name,
			role=role,
			username=username,
			password=generate_password_hash(password)
		)
		exist = Admin.query.filter_by(username=username).first()
		if exist:
			return {'message':'User already exists'}
		else:
			db.session.add(admin)
			db.session.commit()
			return f'User {username} created'
	return 'HI'

login_details = ast.literal_eval(open('./static/auth.json').read())['admin']




@app.route('/search-line.png', methods=['GET'])
def send_png():
	return send_from_directory('.', 'search-line.png')


@app.route('/success', methods=['GET'])
def success():
	if request.method == 'GET':
		return render_template('success.html')




@app.route('/auth.json')
def get_auth():
	return send_from_directory('static', 'auth.json')


@app.route('/people/', methods=['GET'])
def get_student():
	matric_num = request.args.get('matric_num')
	person = db.session.query(Person).filter_by(matric_num=matric_num).first()

	if person:
		return jsonify({
			'id': person.matric_num,
			'matric_num': person.matric_num,
			'first_name': person.first_name,
			'last_name': person.last_name,
			'gender': person.gender
		})
	else:
		return jsonify({'message': 'Student not found'})


def matric_format(matric: str) -> str:
	buffer = ''
	for i in matric:
		try:
			n = int(i)
			buffer += str(n)
		except:
			buffer += i.upper()
	return buffer

@app.route('/students.json', methods=['GET'])
def students():
	students = Person.query.join(Courses).all()
	student_arr= []
	course_arr =[]
	for i, student in enumerate(students):
		for course in student.courses:
			course_arr.append({
                'matricNum': course.matric_num,
				'GEDS_400': course.GEDS_400,
				"GEDS_420": course.GEDS_420,
				"GEDS_400": course.GEDS_400,
				"ITGY_408": course.ITGY_408,
				"ITGY_312": course.ITGY_312,
				"ITGY_402": course.ITGY_402,
				"ITGY_406": course.ITGY_406,
				"COSC_430": course.COSC_430,
				"GEDS_002": course.GEDS_002,
				'sick': course.sick
            })
		student_arr.append({
			'matricNum': student.matric_num,
			'first_name': student.first_name,
			'last_name': student.last_name,
			'gender': student.gender,
			'GEDS_400':student.GEDS_400,
			"GEDS_420" : student.GEDS_420,
			"GEDS_400": student.GEDS_400,
			"ITGY_408": student.ITGY_408,
			"ITGY_312": student.ITGY_312,
			"ITGY_402": student.ITGY_402,
			"ITGY_406": student.ITGY_406,
			"COSC_430": student.COSC_430,
			"GEDS_002": student.GEDS_002,
			'attendance' : course_arr[i]
		})
	with open('students.json', 'w') as file:
		json.dump(student_arr, file)
	with open('students.json', 'r') as json_out_file:
		out = json.load(json_out_file)
	return jsonify(out)


if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)
