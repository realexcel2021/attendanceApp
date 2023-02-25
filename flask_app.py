from flask import Flask, request, jsonify,render_template, redirect, url_for,send_from_directory,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, current_user,login_user
from flask_cors import CORS
from sqlalchemy import inspect
import ast, secrets

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
secret_key = secrets.token_hex(128)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = secret_key

class Person(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	matric_num = db.Column(db.String(10),nullable=False)
	first_name = db.Column(db.String(50),nullable=False)
	last_name = db.Column(db.String(50),nullable=False)
	gender = db.Column(db.String(10),nullable=False)
	status = db.Column(db.Integer,default=0,nullable=False)

class Admin(db.Model):
	with app.app_context():
		if not inspect(db.engine).has_table('authentication'):
			db.create_all()
	admin_id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String,nullable=False)
	user_pass = db.Column(db.String, nullable=False)

	def __init__(self, admin_id):
		self.id = admin_id
		#TODO: Create admin signup route + logic

	def get_admin(self):
		return self.id
	
	def is_authenticated(self):
		exists = db.session.query(Admin).filter_by(user_name=self.user_name, user_pass=self.user_pass).first()
		return bool(exists)

@login_manager.user_loader
def load_user(user_pass):
	return login_details.get(user_pass)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route('/',methods=['GET'])
@login_required
def index():
	return render_template('index.html',user=current_user)


@app.route('/people', methods=['POST'])
def create_student():
	if not inspect(db.engine).has_table('person'):
		db.create_all()
		
	data = request.get_json()
	matric_num = data['matric_num']
	first_name = data['first_name']
	last_name = data['last_name']
	gender = data['gender']
	status = data['status']

	person = Person(
	matric_num=matric_num,
	first_name=first_name,
	last_name=last_name,
	gender = gender,
	status = status)

	exists=Person.query.filter_by(matric_num=matric_num).first()
	if not exists:
		db.session.add(person)
		db.session.commit()
		return jsonify({'message': 'Person created successfully'})
	else:
		exists.status += status
		db.session.commit()
		return jsonify({'message': f"Student with matric {matric_num} already exists, attendance has been updated"})

login_details = ast.literal_eval(open('./static/auth.json').read())['admin']

@app.route('/login', methods=['OPTIONS'])
def handle_options():
    response = app.make_default_options_response()
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
    return response


@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        # Get the user's credentials and authenticate them
        user = authenticate_user(user=request.args.get('username'), passwd=request.args.get('password'))
        if user:
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/auth.json')
def get_auth():
	return send_from_directory('static', 'auth.json')

def authenticate_user(user,passwd):
	return bool(user==login_details['username'] and passwd==login_details['password'])

@app.route('/people/', methods=['GET'])
def get_student():
	matric_num=request.args.get('matric_num')
	person = db.session.query(Person).filter_by(matric_num=matric_num).first()

	if person:
		return jsonify({
			'matric_num': person.matric_num,
			'first_name': person.first_name,
			'last_name' : person.last_name,
			'gender': person.gender,
			'status' : person.status,
		})
	else:
		return jsonify({'message': 'Student not found'})

if __name__ == '__main__':
	app.run(debug=True)