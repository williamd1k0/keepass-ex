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

[![asciicast](https://asciinema.org/a/JBYywRFVT50NGyYi8zBwbcWmE.svg)](https://asciinema.org/a/JBYywRFVT50NGyYi8zBwbcWmE)

>Run `python kpex.py --help` for more usage options.

## Security Info

The server exposes a single entry per execution.

The server requires a HTTP Basic authentication.
>NOTE: The credentials for user and password are the entry title and the password of the database, respectively.

The password is exposed to the web page using RSA encryption.

The web page has a "fire" button to immediately stop the server.
