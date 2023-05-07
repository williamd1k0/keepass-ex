# KeePassEX

A simple application to **EX**pose a KeePass entry to the local host.

This project was created for KeePass users who want to access passwords on devices that do not have access to the filesystem (such as Smart TVs and video game consoles - WiiU in my case) and also do not want to use KeePass with cloud storage (such as [KeeWeb](https://keeweb.info/)).

>NOTE: This project (server) was tested only on Gnu/Linux yet.

## Install

Requirements: Python 3.5+

### Dependencies:

- pykeepass
- bullet
- pyspin
- sanic
- PyNaCl

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

## Security Info

The server exposes a single entry per execution.

The password is encrypted and exposed to the webpage using Diffie-Hellman key exchange with manual key fingerprint validation, eliminating the need for an SSL connection (because some devices/browsers do not support self-signed SSL certificates).

Encryption is done using PyNaCl (server) and TweetNaCl (client).

The webpage has a <kbd>:fire:</kbd> button to immediately stop the server remotely.
