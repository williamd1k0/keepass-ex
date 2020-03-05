import sys
import base64
import socket
import rsa
from sanic import Sanic
from sanic.response import text, html
from sanic_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Sanic(configure_logging=False)

auth_info = {
    'entry': '',
    'entry-password': '',
    'db_password': '',
}

@auth.verify_password
def verify_password(entry, db_password):
    return auth_info['entry'].lower() == entry.lower() and auth_info['db_password'] == db_password

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


def expose_password(entry, entry_password, db_password, port=8000):
    auth_info['entry'] = entry
    auth_info['entry-password'] = entry_password
    auth_info['db_password'] = db_password
    app.static('/static', './web/static')

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print('Password for %s is being exposed to http://%s:%s' % (entry, s.getsockname()[0], port))
    print('Stop the service with ^C (Ctrl+C) or pressing the Fire button on the exposed web page.')
    s.close()
    app.run(host='0.0.0.0', port=port, access_log=False)

if __name__ == '__main__':
    expose_password('entry', 'entry-password', 'db-password')
