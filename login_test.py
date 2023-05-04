import requests

headers = {
	'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
	'sec-ch-ua-platform': '"Windows"',
	'Referer': 'http://127.0.0.1:5000/',
	'DNT': '1',
	'sec-ch-ua-mobile': '?0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
	'Content-Type': 'application/json'
}

url = 'http://localhost:5000'


def test_create_student(url,headers,matric):
	"""Manual test for student creation route"""
	url += '/register'
	data = {
	'ITGY_402' : 1,
	'GEDS_420' : 1,
	'GEDS_400' : 0,
	'ITGY_408' : 1,
	'ITGY_312' : 0,
	'ITGY_402' : 1,
	'ITGY_406' : 1,
	'COSC_430' : 1,
	'GEDS_002' : 1,
	'gender' : 'female',
	'fName' : 'Ave',
	'lName' : 'Ooh',
	'matricNum' : matric
	}
	r = requests.post(url, headers=headers, json=data)
	print(r.text)

def test_attendance(url, headers, matric):
	"""Manual test for attendance record"""
	url = url+'/attendance'
	data ={
		'matricNum' : matric
	}

	r = requests.post(url, headers=headers, json=data)
	print(r.text)

	data = {
		'id' : r.json()['id'],
		'ITGY402' : 0,
		'GEDS420' : 1,
		'GEDS400' : 1,
		'ITGY408' : 0,
		'ITGY312' : 0,
		'ITGY402' : 0,
		'ITGY406' : 0,
		'COSC430' : 1,
		'GEDS002' : 1,
		"sick" : 1
	}
	r = requests.post(url, headers=headers, json=data )
	print(r.text)



def login_test(url):
	data = {
		'username': 'user2',
		'password': 'password2'
	}
	r = requests.post(url, headers=headers, json=data)
	print(r.status_code,r.headers)

def create_admin(url):
	for i in range(3):
		data = {
			'username' : f'user{i}',
			'password' : f'password{i}',
			'name' : f'Admin{i}'
		}
		r = requests.post(url, json=data, headers=headers)
		print(r.status_code,r.headers)

# uncomment one or both to test

matric = 123321
test_create_student(url, headers, matric)
test_attendance(url, headers, matric)

matric = 131222
test_create_student(url, headers, matric)
test_attendance(url, headers, matric)

matric = 112233
test_create_student(url, headers, matric)
test_attendance(url, headers, matric)

matric = 344555
test_create_student(url, headers, matric)
test_attendance(url, headers, matric)



# Admin Creation and Login
create_admin(url+'/signup')
login_test(url+'/login')

r = requests.get(url+'/students.json', headers=headers)
print(r.text)