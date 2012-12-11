import urllib
import httplib as http
img = open('test.jpg', 'rb').read()
img = img.decode('unicode_escape')
boundary = '----------OmNaOmNaOmNamo'
body = '''--%s
Content-Disposition: form-data; name="method"
post
--%s
Content-Disposition: form-data; name="key"
213453243244
--%s
Content-Disposition: form-data; name="file"; filename="kartinka.jpg"
Content-Type: image/pjpeg
%s
--%s--
''' % (boundary, boundary, boundary, img, boundary)
headers = {'Content-type': 'multipart/form-data; boundary=%s' % boundary}
h = http.HTTPConnection('http://localhost:8000')
h.request('POST', '/', body, headers)
resp = h.getresponse()
data = resp.read()
h.close()