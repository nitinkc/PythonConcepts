#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 21:53:26 2018

@author: nitin
"""

import twilio

print (twilio.__version__)

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC56e0753aee90cf5e8f5391576cb6d25f'
auth_token = '0d26fc6ec3e623ac96e0b691b65e3f53'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+1(650) 480-1846',
                              body='body',
                              to='+19255686511'
                          )

print(message.sid)