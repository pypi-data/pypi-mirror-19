Low-Level Connection for HubSpot API Clients
============================================

:Download: `<http://pypi.python.org/pypi/hubspot-conn>`_

**hubspot-connection** provides a lightweight abstraction layer for making
requests to the HubSpot API.

Here's an example of how it can be used:

.. code-block:: python

    from hubspot.connection import APIKey
    from hubspot.connection import PortalConnection

    authentication_key = APIKey('HUBSPOT-API-KEY')
    with PortalConnection(authentication_key, 'client') as connection:
        contacts_data = connection.send_get_request('/contacts/v1/contacts/statistics')
        print("Number of contacts: {}".format(contacts_data.get('contacts')))


This project is officially supported under Python 2.7 and Python 3.4, may work with Python 2.6.
