# KeePassEX

A simple application to EXpose a KeePass entry to the local host.

This project was created for KeePass users who want to access passwords on devices that do not have access to the filesystem (such as Smart TVs and video game consoles - WiiU in my case) and also do not want to use KeePass with cloud storage (such as [KeeWeb](https://keeweb.info/)).

>NOTE: This project (server-side) was tested only on Gnu/Linux yet.

## Install

Requirements: Python 3.5+
>NOTE: Python 3.8 is not yet supported.

### Dependencies:

- pykeepass
- bullet
- pyspin
- sanic
- Sanic-HTTPAuth
- rsa

Install dependencies using `pip`:
```shell
pip install -r requirements.txt
```


## Usage

Run `kpex.py` passing your KeePass database path, then follow the application prompts:
```shell
python kpex.py tests/passwords.kdbx
```

>Run `python kpex.py --help` for more usage options.

### Demo
> Terminal
>
> [![asciicast](https://asciinema.org/a/JBYywRFVT50NGyYi8zBwbcWmE.svg)](https://asciinema.org/a/JBYywRFVT50NGyYi8zBwbcWmE)

> Web page (video)
>
> [![video](https://bittube.video/static/thumbnails/7c02c862-fffb-48fa-8977-b5bae1f99379.jpg)](https://bittube.video/videos/watch/7c02c862-fffb-48fa-8977-b5bae1f99379)

## Security Info

The server exposes a single entry per execution.

The server uses HTTP Basic authentication.
>NOTE: The credentials for password is the entry title (the username is ignored).

>Use the option `--auth` to change basic auth password.

The password is exposed to the web page using [jsencrypt](https://github.com/travist/jsencrypt) (RSA) because some devices/browsers does not support self-signed SSL Certificates.
>Use the flag `--ssl` to enable encrypted connection.

The web page has a <kbd>:fire:</kbd> button to immediately stop the server remotely.
