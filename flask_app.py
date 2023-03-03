from flask import Flask, request, jsonify,render_template, redirect, url_for,send_from_directory
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
	matric_num = db.Column(db.String(10),nullable=False)
	first_name = db.Column(db.String(50),nullable=False)
	last_name = db.Column(db.String(50),nullable=False)
	gender = db.Column(db.String(10),nullable=False)
	status = db.Column(db.Integer,default=0,nullable=False)
	sick = db.Column(db.Integer,default=0,nullable=False)

@app.route('/',methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/people', methods=['POST'])
def create_student():
	if not inspect(db.engine).has_table('person'):
		db.create_all()
		
	data = request.get_json()
	matric_num = data['matricNum']
	first_name = str(data['name']).split()[0]
	last_name = str(data['name']).split()[0]
	gender = data['gender']
	status = data['absent']
	sick = data['sick']

	person = Person(
	matric_num=matric_num,
	first_name=first_name,
	last_name=last_name,
	gender = gender,
	status = status,
	sick = sick)

	exists=Person.query.filter_by(matric_num=matric_num).first()
	if not exists:
		db.session.add(person)
		db.session.commit()
		return jsonify({'message': 'Person created successfully'})
	else:
		exists.status += status
		exists.sick += sick
		db.session.commit()
		return jsonify({'message': f"Student with matric {matric_num} already exists, attendance has been updated"})

login_details = ast.literal_eval(open('./static/auth.json').read())['admin']

@app.route('/login', methods=['OPTIONS'])
def handle_options():
	response = app.make_default_options_response()
	response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
	return response

@app.route('/adminPage.html',methods=['GET'])
def admin():
	if request.method == 'GET':
		return render_template('adminPage.html')
	
@app.route('/success',methods=['GET'])
def success():
	if request.method=='GET':
		return render_template('success.html')

@app.route('/login.html',methods = ['POST','GET'])
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
			'sick' : person.sick
		})
	else:
		return jsonify({'message': 'Student not found'})

@app.route('/student.json',methods=['GET'])
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
			'sick' : student.sick})

	with open('students.json','w') as file:
		json.dump(json_arr,file)
	with open('students.json','r') as json_out_file:
		out=json.load(json_out_file)
	return jsonify(out)

if __name__ == '__main__':
	app.run(debug=True)