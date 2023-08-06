import webbrowser

from pprint import pprint
from .api import Session


ENTRY_MSG = """
    This is the Pandadocs token tool built to make your use of Pandadocs a breeze.

    First, you need to create an application on the PandaDocs developer portal: 

        https://app.pandadoc.com/developers/

    After registering on the Developer portal, you need to enter some data below to generate your tokens.
"""

AUTH_MSG = """
    We've opened a browser for your to complete the authorization at the URL: 

        {0}

    After authorization, copy the URL you are redirected to. It might look something like this:

        {1}

    You will be prompted to paste the callback URL containing your authorization code.
"""

def main():
    print ENTRY_MSG

    raw_input("Ready? Press Enter to continue.")

    client_id = raw_input('Enter the Client ID: ')
    client_secret = raw_input('Enter the Client Secret: ')
    redirect_uri = raw_input('Enter the Redirect URI: ')


    panda = Session(client_id=client_id, redirect_uri=redirect_uri)
    authorization_url, state = panda.authorization_url()


    print AUTH_MSG.format(authorization_url, redirect_uri+'?state=<long state code>&code=<auth code>')
    raw_input("Ready? Press Enter to continue")

    webbrowser.open_new_tab(authorization_url)

    authorization_response = raw_input('Enter the full callback URL: ')

    token = panda.fetch_token(authorization_response=authorization_response,
                              client_secret=client_secret)


    panda = Session(client_id=client_id, token=token)

    templates = panda.get_templates()

    if templates.status_code == 200:
        print "Authorization succeeded! Copy the token dict below and use it in your code. Here's your token:\n"
        pprint(token)

        print "\n\nEnjoy!"
    else:
        print templates.json()