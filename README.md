# LDAP password expiration notifier

Mail notifier for LDAP password expiration.

## About

The script is designed to be run once a day and sends an email notification to LDAP users whose password is expiring soon.

## Prerequisites

- a LDAP server with configured password expiration policy
- a working local mail relay server (e.g. postfix)
- python3 (version > 3.6)
- python3-pip

## Installing

First clone the repository:
```bash
git clone https://github.com/meroupatate/ldap-password-expiration-notifier.git
```

Install the python dependencies:
```bash
cd ldap-password-expiration-notifier
pip3 install -r requirements.txt
```

Edit config.py to connect to your LDAP server:
```bash
mv config.py.example config.py
vim config.py
```

Test if the script is running correctly:
```bash
python3 notifier.py
```

Finally, set a cron job to launch the script daily:
```
echo '0 0 * * * root /usr/bin/python3 /path/to/notifier.py' >> /etc/cron.d/ldap-password-expiration-notifier
```
