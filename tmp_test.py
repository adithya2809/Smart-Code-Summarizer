import http.client, uuid
boundary='----WebKitFormBoundary'+uuid.uuid4().hex
parts=[]
parts.append('--'+boundary)
parts.append('Content-Disposition: form-data; name="project_name"\r\n')
parts.append('mytest')
parts.append('--'+boundary)
parts.append('Content-Disposition: form-data; name="file"; filename="app.py"')
parts.append('Content-Type: text/plain\r\n')
parts.append(open('app.py','rb').read().decode('utf-8','replace'))
parts.append('--'+boundary+'--\r\n')
body='\r\n'.join(parts).encode('utf-8')
conn=http.client.HTTPConnection('127.0.0.1',8001,timeout=10)
conn.request('POST','/summarize',body,{'Content-Type':f'multipart/form-data; boundary={boundary}'})
res=conn.getresponse()
print('status',res.status,res.reason)
print('body',res.read(2000).decode('utf-8','replace'))
