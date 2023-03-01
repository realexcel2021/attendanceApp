import requests
import threading

# Define a function that pings your server once
def ping_server():
	data={'matric_num':'ABG423','first_name':'Kola', 'last_name':'Ade','gender':'male', 'absent':1,'sick':1}
	url='http://127.0.0.1:5000/people'
	header= {'Content-Type':'application/json'}
	r1 = requests.post(url,json=data,headers=header)
	print(r1.url)
	print(r1.text)

	r2=requests.get(f"{url}?matric_num=ABG423")
	print(r2.status_code)
	print(r2.text)

# Create an empty list to store the threads
threads = []

# Create 10 threads that call the ping_server function
for i in range(10):
	t = threading.Thread(target=ping_server)
	threads.append(t)

# Start all the threads
for t in threads:
	t.start()

# Wait for all the threads to finish
for t in threads:
	t.join()