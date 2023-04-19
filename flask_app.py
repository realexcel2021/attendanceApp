from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import ast, secrets, logging, json
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
secret_key = secrets.token_hex(128)
app.secret_key = secret_key

class Person(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	courses=db.Relationship('Courses',backref='person')
	matric_num = db.Column(db.String(20),nullable=False)
	first_name = db.Column(db.String(50),nullable=False)
	last_name = db.Column(db.String(50),nullable=False)
	gender = db.Column(db.String(10),nullable=False)
class Courses(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	matric_num = db.Column(db.String(20),db.ForeignKey('person.matric_num'))
	status = db.Column(db.Integer,default=0)
	sick = db.Column(db.Integer,default=0)
	present = db.Column(db.Integer,default=0)
	ITGY_402 = db.Column(db.Boolean,nullable = False,default=0)
	GEDS_420 = db.Column(db.Boolean,nullable = False,default=0)
	GEDS_420 = db.Column(db.Boolean,nullable = False,default=0)
	GEDS_400 = db.Column(db.Boolean,nullable = False,default=0)
	ITGY_408 = db.Column(db.Boolean,nullable = False,default=0)
	ITGY_312 = db.Column(db.Boolean,nullable = False,default=0)
	ITGY_402 = db.Column(db.Boolean,nullable = False,default=0)
	ITGY_406 = db.Column(db.Boolean,nullable = False,default=0)
	COSC_430 = db.Column(db.Boolean,nullable = False,default=0)
	GEDS_002 = db.Column(db.Boolean,nullable = False,default=0)
	GEDS_400 = db.Column(db.Boolean,nullable = False,default=0)





@app.route('/',methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/attendance',methods=['POST','GET'])
def mark_attendance():
	if request.method=='POST':
		data = request.get_json()
		if len(data) == 1:
			matric_num=data['matricNum']
			exist=Courses.query.filter_by(matric_num=matric_num)
			return jsonify({'message':int(bool(exist))})
		matric_num = data['id']
		course = '_'.join(data['course'].split())
		status=1 if data['attendaceStatus']=='Present' else 0

		courses=Courses(
		matric_num=matric_num,
		course=status
		)

	exist=db.query.filter_by(matric_num=matric_num).first()
	if not exist:
		return jsonify({'message':'No user found'})
	else:
		course_dict= {
			"ITGY_402":"ITGY_402",
			"GEDS_420":"GEDS_420",
			"GEDS_400":"GEDS_400",
			"ITGY_408":"ITGY_408",
			"ITGY_312":"ITGY_312",
			"ITGY_402":"ITGY_402",
			"ITGY_406":"ITGY_406",
			"COSC_430":"COSC_430",
			"GEDS_002":"GEDS_002"
		}
		exist.course += status
@app.route('/register', methods=['POST','GET'])
def create_student():
	if request.method=='GET':
		return render_template('RegistrationPage.html')
	if not inspect(db.engine).has_table('person'):
		db.create_all()
		
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

	person= Person(
	matric_num=matric_num,
	first_name=first_name,
	last_name=last_name,
	gender = gender)

	courses=Courses(
	matric_num=matric_num,
	ITGY_402 =ITGY_402,
	GEDS_420=GEDS_420,
	GEDS_400=GEDS_400,
	ITGY_408=ITGY_408,
	ITGY_312=ITGY_312,
	ITGY_406=ITGY_406,
	COSC_430=COSC_430,
	GEDS_002=GEDS_002
	)

	exists=Person.query.filter_by(matric_num=matric_num).first()
	if not exists:
		db.session.add(person)
		db.session.add(courses)
		db.session.commit()
		return jsonify({'message': 'Person created successfully'})
	else:
		return jsonify({'message': f"Student with matric {matric_num} already exists"})

login_details = ast.literal_eval(open('./static/auth.json').read())['admin']

@app.route('/login', methods=['OPTIONS'])
def handle_options():
	response = app.make_default_options_response()
	response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
	return response

@app.route('/admin',methods=['GET'])
def admin():
	if request.method == 'GET':
		return render_template('adminPage.html')

@app.route('/search-line.png',methods=['GET'])
def send_png():
	return send_from_directory('.','search-line.png')


@app.route('/success',methods=['GET'])
def success():
	if request.method=='GET':
		return render_template('success.html')


@app.route('/login',methods = ['POST','GET'])
def login():
	if request.method == 'POST':
		info = request.get_json()
		user = info['username']
		passwd = info['password']
		if authenticate(user,passwd):
			return redirect(url_for('admin'))
		else:
			return jsonify({'message':'incorrect username or password'})
	elif request.method == 'GET':
		return render_template('login.html')

def authenticate(user,passwd):
	return bool(user==login_details['username'] and passwd==login_details['password'])

@app.route('/auth.json')
def get_auth():
	return send_from_directory('static', 'auth.json')

@app.route('/people/', methods=['GET'])
def get_student():
	matric_num=request.args.get('matric_num')
	person = db.session.query(Person).filter_by(matric_num=matric_num).first()

	if person:
		return jsonify({
			'id' : person.matric_num,
			'matric_num': person.matric_num,
			'first_name': person.first_name,
			'last_name' : person.last_name,
			'gender': person.gender,
			'absent' : person.status,
			'sick' : person.sick,
			'present' : person.present
		})
	else:
		return jsonify({'message': 'Student not found'})

@app.route('/students.json',methods=['GET'])
def get_all():
	students = Person.query.all()
	json_arr  = []
	for student in students:
		json_arr.append({
			'id' : student.matric_num,
			'matricNum': student.matric_num,
			'first_name': student.first_name,
			'last_name' : student.last_name,
			'gender': student.gender,
			'absent' : student.status,
			'sick' : student.sick,
			'present' : student.present})

	with open('students.json','w') as file:
		json.dump(json_arr,file)
	with open('students.json','r') as json_out_file:
		out=json.load(json_out_file)
	return jsonify(out)


def matric_format(matric:str) -> str:
	alpha_buffer =""
	num_buffer = ''
	for i in matric:
		try:
			n = int(i)
			num_buffer+=str(n)
		except:
			alpha_buffer += i
	alpha_buffer=alpha_buffer.upper()
	return alpha_buffer+num_buffer

if __name__ == '__main__':
	app.run(debug=True)