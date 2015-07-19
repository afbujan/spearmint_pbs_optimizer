#!/usr/bin/env python
import smtplib

sender = 'NERSC@nersc.gov'
receivers = ['afbujan.python@gmail.com']
message = """From: NERSC <NERSC@nersc.gov>
To: Alex <afbujan.python@gmail.com>
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
