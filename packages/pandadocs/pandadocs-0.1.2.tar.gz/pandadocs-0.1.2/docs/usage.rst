=====
Usage
=====

First, install the package according to the installation instructions.

Then, use the pandadocs-tokentool to retrieve the client_id and token dict.


Then, create and use a pandadocs Session to interact with the REST API::

    from pandadocs import Session

    panda = Session(client_id=YOUR_CLIENT_ID, token=YOUR_TOKEN_DICT)
    templates = panda.get_templates()

    print templates.json()
