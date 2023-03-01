import requests
import time

data={'matric_num':'ABG423','first_name':'Kola', 'last_name':'Ade','gender':'male', 'absent':1,'sick':1}
url='http://127.0.0.1:5000/people'
header= {'Content-Type':'application/json'}
r1 = requests.post(url,json=data,headers=header)
print(r1.url)
print(r1.text)

time.sleep(5)
r2=requests.get(f"{url}?matric_num=ABG423",headers=header)
print(r2.status_code)
print(r2.json())