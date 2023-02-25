from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Person(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	matric_num = db.Column(db.String(10),nullable=False)
	first_name = db.Column(db.String(50),nullable=False)
	last_name = db.Column(db.String(50),nullable=False)
	gender = db.Column(db.String(10),nullable=False)
	status = db.Column(db.Integer,default=0,nullable=False)

@app.route('/',methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/people', methods=['POST'])
def create_student():
	if not inspect(db.engine).has_table('person'):
		# Create the person table if it does not exist
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