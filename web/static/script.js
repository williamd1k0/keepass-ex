(function() {
    function fallback_copy_text2clipboard(text, successful_callback, unsuccessful_callback) {
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.opacity = "0";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
    
        try {
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
            console.log('Fallback: Copying text command was ' + msg);
            if (successful) {
                successful_callback();
            } else {
                unsuccessful_callback();
            }
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
            unsuccessful_callback();
        }
    
        document.body.removeChild(textArea);
    }

    function copy_text2clipboard(text, successful_callback, unsuccessful_callback) {
        if (!navigator.clipboard) {
            fallback_copy_text2clipboard(text, successful_callback, unsuccessful_callback);
            return;
        }
        navigator.clipboard.writeText(text).then(function() {
            console.log('Async: Copying to clipboard was successful!');
            successful_callback();
        }, function(err) {
            console.error('Async: Could not copy text: ', err);
            unsuccessful_callback();
        });
    }

    var client_keypair = nacl.box.keyPair();
    var server_pubkey;
    var password = {};

    function fetch_password() {
        const key_fingerprint = emoji(nacl.hash(client_keypair.publicKey), 4).join(' ');
        const message = nacl.util.encodeBase64(client_keypair.publicKey);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/pass");
        xhr.addEventListener('load', function(ev) {
            var data = JSON.parse(xhr.responseText);
            var nonce = nacl.util.decodeBase64(data.nonce);
            var ciphertext = nacl.util.decodeBase64(data.ciphertext);
            var decrypted = nacl.box.open(ciphertext, nonce, server_pubkey, client_keypair.secretKey);
            var decrypted_message = nacl.util.encodeUTF8(decrypted);
            password.value = decrypted_message;
            document.querySelector('body').style.display = 'block';
        });
        xhr.send(message);
        window.alert("Confirm key fingerprint: " + key_fingerprint);
    }

    window.addEventListener('load', function(ev) {
        server_pubkey = nacl.util.decodeBase64(document.querySelector('meta[name="kp-server-pubkey"]').content);
        document.getElementById('kp-fire').addEventListener('click', function(ev) {
            password = null;
            document.write('');
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/fire");
            xhr.send();
        });
    
        document.getElementById('kp-copy').addEventListener('click', function(ev) {
            document.getElementById('kp-copy-info').style.display = 'none';
            copy_text2clipboard(password.value, function() {
                var info = document.getElementById('kp-copy-info');
                info.innerText = 'Copied!';
                info.style.display = 'block';
            }, function() {
                var info = document.getElementById('kp-copy-info');
                info.innerText = 'Failed!';
                info.style.display = 'block';
            });
        });

        document.getElementById('kp-show').addEventListener('click', function(ev) {
            var pass_show = document.querySelector('#kp-pass');
            if (pass_show.innerText) {
                pass_show.innerText = '';
            } else {
                pass_show.innerText = password.value;
            }
        });

        twemoji.parse(document.querySelector('h1 button'), {className: 'kp-emoji-fire', base: '/static/'});
        twemoji.parse(document.querySelector('#kp-show'), {className: 'kp-emoji-warn', base: '/static/'});

      fetch_password();
    });

})();