# -*- coding: utf-8 -*-
#
#
#
__doc__="""This module provides sending SMS via Twilio

The code is tested in tests/test_lib_smsprovider
"""
from twilio.rest import Client
from privacyidea.lib.smsprovider.SMSProvider import ISMSProvider
import logging
log = logging.getLogger(__name__)

class TwilioSMSProvider(ISMSProvider):

    # We do not need to overwrite the __init__ and
    # the loadConfig functions!
    # They provide the self.config dictionary.

    def submit_message(self, phone, message):
        if self.smsgateway:
            account_sid = self.smsgateway.option_dict.get("ACCOUNT_SID")
            auth_token = self.smsgateway.option_dict.get("AUTH_TOKEN")
            service_sid = self.smsgateway.option_dict.get("SERVICE_SID")
        else:
            account_sid = self.config.get("ACCOUNT_SID")
            auth_token = self.config.get("AUTH_TOKEN")
            service_sid = self.config.get("SERVICE_SID")

        client = Client(account_sid, auth_token)
        try:
            msg = client.messages.create(
                to=phone,
                messaging_service_sid=service_sid,
                body=message)
        except TwilioRestException as e:
            log.error(e)
        log.debug("SMS submitted: {0!s}".format(msg.sid))

        return True

    @classmethod
    def parameters(cls):
        """
        Return a dictionary, that describes the parameters and options for the
        SMS provider.
        Parameters are required keys to values.

        :return: dict
        """
        from privacyidea.lib.smtpserver import get_smtpservers
        params = {"options_allowed": False,
                  "parameters": {
                      "ACCOUNT_SID": {
                          "required": True,
                          "description": "Twilio accout sid."},
                      "AUTH_TOKEN": {
                          "required": True,
                          "description": "Twilio auth token."},
                      "SERVICE_SID": {
                          "required": True,
                          "description": "Twilio service sid."}
                  }
                  }
        return params
