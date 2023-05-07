import sys
import base64
import socket
import nacl.utils
import nacl.encoding, nacl.hash
from nacl.public import PrivateKey, PublicKey, Box
import emojihash
from sanic import Sanic
from sanic.response import html, json, empty
from bullet import Bullet
import theme


app = Sanic(name="kpex", configure_logging=False)

auth_info = {
    'entry': '',
    'entry-password': '',
}
server_privkey = PrivateKey.generate()
server_pubkey = server_privkey.public_key
can_exchange_keys = True

@app.route('/')
async def index(request):
    tmpf = open('web/index.tmp.html', 'r', encoding='utf-8')
    tmp = tmpf.read()
    tmpf.close()
    tmp = tmp.replace('{{ kp-entry }}', auth_info['entry'])
    tmp = tmp.replace('{{ kp-server-pubkey }}', server_pubkey.encode(encoder=nacl.encoding.Base64Encoder).decode('utf-8'))
    return html(tmp)

@app.route('/pass', ['POST'])
async def password(request):
    global can_exchange_keys
    if can_exchange_keys:
        can_exchange_keys = False
        client_pubkey = PublicKey(request.body, encoder=nacl.encoding.Base64Encoder)
        key_hash = nacl.hash.sha512(client_pubkey._public_key, nacl.encoding.RawEncoder)
        fingerprint = ' '.join(emojihash.emoji(key_hash, 4))
        fingerprint += " %s" % [i for i in key_hash[:4]]
        cli = Bullet(prompt='Confirm key fingerprint: %s' % fingerprint, choices=['Yes', 'No'], margin=1, pad_right=1, **theme.BULLET)
        result = cli.launch()
        can_exchange_keys = True
        if result == 'Yes':
            box = Box(server_privkey, client_pubkey)
            message = auth_info['entry-password'].encode('utf-8')
            encrypted = box.encrypt(message)
            return json({
                'nonce': base64.b64encode(encrypted.nonce).decode('utf-8'),
                'ciphertext': base64.b64encode(encrypted.ciphertext).decode('utf-8'),
            })
    return empty(status=401)

@app.route('/fire')
async def fire(request):
    app.stop()
    return empty()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def expose_entry(entry, entry_password, port=8000):
    auth_info['entry'] = entry
    auth_info['entry-password'] = entry_password

    print('Password for %s is being exposed to http://%s:%s' % (entry, get_local_ip(), port))
    print('Stop the service with ^C (Ctrl+C) or pressing the Fire button on the exposed web page.')

    app.static('/static', './web/static')
    app.run(host='0.0.0.0', port=port, access_log=False, debug=False)

if __name__ == '__main__':
    expose_entry('entry', 'entry-password')
