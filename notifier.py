#!/usr/bin/python3

import ldap
import smtplib
from datetime import datetime
from config import *


def send_mail(uid, mail, lastPwdUpdate):
    mailTo = mail
    mailFrom = MAIL_FROM
    mailSubject = "LDAP Password Expiry Details"
    remainingDays = pwdMaxAge - lastPwdUpdate
    mailBody = """From: %s
To: %s
Subject: %s
Hi %s,

Your password will expire in %s day(s).

We're sorry for the \
inconvenience, but we will need you to change your password soon.

The last time your password was changed was %s day(s) ago.

Thanks,
Your system administrator
""" % (mailFrom, mailTo, mailSubject, uid, remainingDays, lastPwdUpdate)
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(mailFrom, mailTo, mailBody)
    smtp.close()
    return


def get_user_details():
    l = ldap.initialize(LDAP_URL)
    l.simple_bind_s(LDAP_USER,LDAP_PASSWORD)
    # Perform LDAP Search
    data = l.search_s(LDAP_USER_SEARCH_BASE_DN, ldap.SCOPE_SUBTREE, '(uid=*)', ['uid','pwdChangedTime', 'mail'])
    return [ d[1] for d in data ]


def check_password_expiry(ldap_users):
    for user in ldap_users:
        uid = user['uid'][0].decode()
        if 'pwdChangedTime' not in user:
            # No password update since user creation
            pwd_expire_in_days = 0
            user.update({'trigger': True})
            print(f'User {uid} password never updated')
        else:
            # Count days before next mandatory password update
            pwdChangedTime = user['pwdChangedTime'][0].decode()
            d0 = datetime.strptime(pwdChangedTime, '%Y%m%d%H%M%SZ')
            d1 = datetime.now()
            delta = d1 - d0
            # Get number of days since last password update
            lastPwdUpdate = delta.days

            if lastPwdUpdate in pwdWarnDays:
                if 'mail' in user:
                    mail = user['mail'][0].decode()
                    print(f'Sending email to user {uid}: password expires in {pwdMaxAge - lastPwdUpdate} days')
                    send_mail(uid, mail, lastPwdUpdate)
                    print(f"Email sent")
            elif lastPwdUpdate > pwdMaxAge:
                print(f'User {uid}: password expired for {lastPwdUpdate - pwdMaxAge} days')
            else:
                print(f'User {uid}: last password update {lastPwdUpdate} days ago')


if __name__ == '__main__':
    ldap_users = get_user_details()
    check_password_expiry(ldap_users)
