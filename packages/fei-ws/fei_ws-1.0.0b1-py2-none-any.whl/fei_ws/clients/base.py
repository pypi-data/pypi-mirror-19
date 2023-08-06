from fei_ws import config
from urlparse import urljoin
from suds.client import Client


class FEIWSBaseClient(object):
    """FEI Base Client contains logic shared among FEI Clients. It should not
    be used on its own.

    """
    def __init__(self, version, username=None, password=None):
        """ Initializes the base client.

        Params:
            version: A tuple containing the version numbering.
            username: The username used to authenticate. The username from the
                config file is used when it is not supplied.
            password: The password used to authenticate. The password from the
                config file is used when it is not supplied.

        """
        self.__AUTH_WSDL = urljoin(config.FEI_WS_BASE_URL,
                                   '/_vti_bin/Authentication.asmx?WSDL')
        self.__ORGANIZER_WSDL = urljoin(
            config.FEI_WS_BASE_URL, '/_vti_bin/FEI/OrganizerWS_%s_%s.asmx?WSDL'
                                 % version)
        self.__COMMON_WSDL = urljoin(config.FEI_WS_BASE_URL,
                                     '/_vti_bin/FEI/CommonWS.asmx?WSDL')

        self._version = version
        self._common_data = {}
        self._username = username if username else config.FEI_WS_USERNAME
        self._password = password if password else config.FEI_WS_PASSWORD
        self._ows_client = Client(self.__ORGANIZER_WSDL)
        self._cs_client = Client(self.__COMMON_WSDL)
        self._authenticate([self._ows_client, self._cs_client])

    def _authenticate(self, clients):
        """Used to authenticate clients with the FEI WS.

        """
        auth_client = Client(self.__AUTH_WSDL)
        if not self._username or not self._username:
            raise Exception("Could not login: username and password are empty. "
                            "Please provide a username and password to init or "
                            "set the username and password in the settings "
                            "file.")
        auth_login = auth_client.service.Login(self._username, self._password)
        if auth_login['ErrorCode'] != 'NoError':
            #TODO create own Exception class for these kind of exceptions.
            raise Exception('Could not login: %s' % auth_login['ErrorCode'])
        for client in clients:
            client.options.transport.cookiejar = \
                auth_client.options.transport.cookiejar
            auth_header = self._ows_client.factory.create('AuthHeader')
            auth_header['UserName'] = self._username
            auth_header['Language'] = 'en'
            client.set_options(soapheaders=auth_header)

    def _handle_messages(self, result):
        """Generic message handler, used to determine if an exception needs to
        be thrown.

        """
        #TODO How to feedback warnings back to the user?
        warnings = ''
        message_types = self.get_common_data('getMessageTypeList')
        if not result['Messages']:
            return
        for message in result['Messages'].Message:
            msg = filter(lambda x: x.Id == message.UID,
                         message_types.MessageType)[0]
            description = ('%s: %s\nDetails: %s' %
                           (msg.Id, msg.Description, message.Detail))
            if msg.IsCritical or msg.IsError:
                raise Exception(description)
            warnings += '%s\n' % description
        if warnings:
            print warnings

    def get_common_data(self, method, **kwargs):
        """Generic method for retrieving data from the common data web service.

        Params:
            method: The name of the common data WS method you want to use.
            **kwargs: Contains the keyword arguments you want to pass to the
                method you are calling.

        Return value: The raw result from the Common Data WS.

        """
        if not kwargs and method in self._common_data:
            return self._common_data[method]
        result = getattr(self._cs_client.service, method)(**kwargs)
        self._common_data['method'] = result
        return result
