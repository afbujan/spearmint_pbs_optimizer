#!/usr/bin/env python
import smtplib

sender = 'yourcluster@somewhere.uni'
receivers = ['you.python@mail.com']
message = """From: yourcluster <yourcluster@somewhere.uni>
To: you <you.python@mail.com>
Subject: Daemon crashed!
This is bad luck! :-(.
"""
try:
    global smtpObj
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)
    print "Successfully sent email"
except SMTPException:
    print "Error: unable to send email"
