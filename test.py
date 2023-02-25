import requests
import time

data={'matric_num':'ABG423','first_name':'Kola', 'last_name':'Ade','gender':'male', 'status':1}
url='http://127.0.0.1:5000/people'
header= {'Content-Type':'application/json'}
r = requests.post(url,json=data,headers=header)
print(r.url)
print(r.text)

time.sleep(5)
r=requests.get(f"{url}?matric_num=ABC323")
print(r.status_code)
print(r.url)
new=r.json()
new['status']=1
for _ in range(3):
	print(requests.post(url,json=new,headers=header).text)
	time.sleep(2)
