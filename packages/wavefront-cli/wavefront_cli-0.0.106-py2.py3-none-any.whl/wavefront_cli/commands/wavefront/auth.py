
import os
import sys
from api import validate_token
from os.path import expanduser


WF_URL_ENVKEY = "WAVEFRONT_URL"
WF_TOKEN_ENVKEY = "WAVEFRONT_TOKEN"

user_token = ""
user_url = ""

def do_auth(options):

    if options['--lib-url']:
        user_url = options['--lib-url']
    else:
        user_url = raw_input("Please enter your Wavefront URL: ")


    if options['--api-token']:
        user_token = options['--api-token']
    else:
        user_token = raw_input("Please enter your Wavefront API Token: ")

    save_auth(user_url,user_token)


def save_auth(user_url, user_token):
    home = expanduser("~") + "/.lib/"
    # make sure the lib home directory exists
    if not os.path.exists(home):
        os.makedirs(home)

    # validate the user's info
    valid = validate_token(user_url, user_token)
    if valid:
        creds = open(home + "credentials", "w")
        creds.write("%s\n%s" % (user_url,user_token))
        creds.close()
    return valid

def get_or_set_auth(options):

    # did the user pass options?
    if options['--lib-url'] and options['--api-token']:
        # yes, save auth
        save_auth(options['--lib-url'],options['--api-token'])
        return get_auth()
    else:
        # the user didn't pass options, are there existing creds saved?
        creds = get_auth()
        if creds != None:
            return creds
        else:
            do_auth(options)
            return get_auth()

def get_auth():
    try:
        home = expanduser("~") + "/.lib/"
        creds = open(home + "credentials", "r")
        text = creds.read()
        user_url = text.split("\n")[0]
        user_token = text.split("\n")[1]
        valid = validate_token(user_url, user_token)
        if valid:
            return {
                "user_url": user_url,
                "user_token": user_token
            }
        else:
            print "Your previously saved API Token failed to validate. Was it deactivated?"
            return None
    except:
       return None
