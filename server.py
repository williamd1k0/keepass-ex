import sys
import base64
import socket
import rsa
from sanic import Sanic
from sanic.response import text, html
from sanic_httpauth import HTTPBasicAuth

app = Sanic(configure_logging=False)
auth = HTTPBasicAuth()

auth_info = {
    'entry': '',
    'entry-password': '',
    'auth-password': '',
}

@auth.verify_password
def verify_password(_, auth_password):
    return auth_info['auth-password'] == auth_password

@app.route('/')
@auth.login_required
async def index(request):
    tmpf = open('web/index.tmp.html', 'r', encoding='utf-8')
    tmp = tmpf.read()
    tmpf.close()
    tmp = tmp.replace('{{kp-entry}}', auth_info['entry'])
    return html(tmp)

@app.route('/pass', ['POST'])
@auth.login_required
async def password(request):
    pub = rsa.PublicKey.load_pkcs1_openssl_pem(request.body)
    message = rsa.encrypt(auth_info['entry-password'].encode('utf-8'), pub)
    return text(base64.b64encode(message).decode())

@app.route('/fire')
async def fire(request):
    app.stop()
    return text('')


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def expose_entry(entry, entry_password, auth_password, port=8000, use_ssl=True):
    auth_info['entry'] = entry
    auth_info['entry-password'] = entry_password
    auth_info['auth-password'] = auth_password

    ssl = None
    protocol = 'http'
    if use_ssl:
        ssl = {'cert': ".keys/ca.crt", 'key': ".keys/ca.key"}
        protocol = 'https'

    print('Password for %s is being exposed to %s://%s:%s' % (entry, protocol, get_local_ip(), port))
    print('Stop the service with ^C (Ctrl+C) or pressing the Fire button on the exposed web page.')

    app.static('/static', './web/static')
    app.run(host='0.0.0.0', port=port, ssl=ssl, access_log=False, debug=False)

if __name__ == '__main__':
    expose_entry('entry', 'entry-password', 'password')
