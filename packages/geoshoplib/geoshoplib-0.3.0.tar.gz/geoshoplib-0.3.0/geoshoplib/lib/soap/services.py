# -*- coding: iso-8859-1 -*-

# Copyright (c) 2012 - 2016, GIS-Fachstelle des Amtes für Geoinformation des Kantons Basel-Landschaft
# All rights reserved.
#
# This program is free software and completes the GeoMapFish License for the geoview.bl.ch specific
# parts of the code. You can redistribute it and/or modify it under the terms of the GNU General 
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# With respect to the origin code of Karsten Deininger: https://github.com/camptocamp/bl_geoview/tree/geoshop_client/bl_gis2012_geoshop/lib
#
import httplib2
import untangle

__author__ = 'Clemens Rudert'
__create_date__ = '21.12.16'


class BaseService(object):
    __XML_HEADER__ = """
        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope
           xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soap:Body>
    """

    __XML_FOOTER__ = """
        </soap:Body>
        </soap:Envelope>
    """
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/xml"}

    def __init__(self, host, port, service, headers=None, disable_ssl_certificate_validation=False):
        """
        The case class service offers a simple connect able object. It can execute a request to the configured
        service.

        :param host: The host to connect to.
        :type host: str
        :param port: The port number which.
        :type port: int
        :param service: The path to the service which completes the host.
        :type service: str
        :param headers: The headers which should be sent to the server. The standard will be used if they are None.
        :type headers: None or dict default is None
        :param disable_ssl_certificate_validation:
        :type disable_ssl_certificate_validation: bool
        """
        self.host = host
        self.port = port
        self.service = service
        self.disable_ssl_certificate_validation = disable_ssl_certificate_validation
        if headers is not None:
            self.headers = headers

    def _connect(self):
        """

        :return: The connection.
        :rtype: httplib2.HTTPSConnectionWithTimeout
        """
        return httplib2.HTTPSConnectionWithTimeout(
            self.host,
            self.port,
            disable_ssl_certificate_validation=self.disable_ssl_certificate_validation
        )

    def request(self, request_type, body):
        """
        The central method. It requests the configured service.

        :param request_type: The HTTP request type which should be used for the request. (POST,PUT,DELETE,GET)
        :type request_type: str
        :param body: The xml body which should be sent to the server vie this request.
        :type body: str
        :return: The result
        :rtype: str
        :raises: KeyError
        """
        if request_type not in ['POST', 'PUT', 'GET', 'DELETE']:
            raise KeyError('Not a valid request method: {0}'.format(request_type))

        request_body = ''.join([
            self.__XML_HEADER__,
            body,
            self.__XML_FOOTER__,
        ])
        try:
            connection = self._connect()
            connection.request(request_type, self.service, request_body, self.headers)
            response = connection.getresponse()
            result = response.read()
            connection.close()
            return result
        except Exception as e:
            raise e


class Product(object):
    key_error_text = u'''
        Product "{product}" has no key "{key}" This means it is not set in geoshop.
        No problem - skipping it... (original error was: {error})
    '''
    xml_body = """
        <getProductDefinition xmlns="http://www.infogrips.ch/geoshop/user/">
            <user xmlns="">{user}</user>
            <password xmlns="">{password}</password>
            <product xmlns="">{product_id}</product>
        </getProductDefinition>
    """

    def __init__(self, product_id, user, password, service, display_name=None):
        """
        This is an abstraction class for the geoshop product. Once created it is able to obtain its own definition from
        the assigned service.

        :param product_id: The ID of the product which is used by geoshop
        :type product_id: str
        :param user: The user which is used to request the server.
        :type user: str
        :param password: The password which is used to request the server.
        :type password: str
        :param service: The service which is used to execute the requests
        :type service: BaseService
        :param display_name: The name of the product which is used by geoshop
        :type display_name: str or None default is None
        """
        self.service = service
        self.user = user
        self.password = password
        self.product_id = product_id
        self.display_name = display_name

        self.xml_body = self.xml_body.format(user=user, password=password, product_id=product_id)

        self.params = None
        self.price_function = None
        self.models = None

    def get_definition(self):
        """
        Requests the definition from the assigned service/server

        :return: The updated product instance
        :rtype: Product
        """
        result_object = untangle.parse(self.service.request('POST', self.xml_body))
        try:
            self.display_name = result_object.soap_Envelope.soap_Body.getProductDefinitionResponse.productdefinition.display_name.cdata
        except IndexError, e:
            raise e
        try:
            self.params = result_object.soap_Envelope.soap_Body.getProductDefinitionResponse.productdefinition.params.cdata
        except IndexError, e:
            print self.key_error_text.format(product=self.product_id, key='params', error=e)
        try:
            self.price_function = result_object.soap_Envelope.soap_Body.getProductDefinitionResponse.productdefinition.price_function.cdata
        except IndexError, e:
            print self.key_error_text.format(product=self.product_id, key='price_function', error=e)
        try:
            self.models = result_object.soap_Envelope.soap_Body.getProductDefinitionResponse.productdefinition.models.cdata
        except IndexError, e:
            print self.key_error_text.format(product=self.product_id, key='models', error=e)
        return self


class UserService(object):
    xml_body = """
        <getProducts xmlns="http://www.infogrips.ch/geoshop/user/">
            <user xmlns="">{user}</user>
            <password xmlns="">{password}</password>
        </getProducts>
    """

    def __init__(self, user, password, service):
        """
        This is the high level abstraction for the so called "user service" in the geoshop eco system. It provides an
        basic abstraction of the methods of this service.

        :param user: The user which is used to request the server.
        :type user: str
        :param password: The password which is used to request the server.
        :type password: str
        :param service: The service which is used to execute the requests
        :type service: BaseService
        """
        self.service = service
        self.user = user
        self.password = password

        self.xml_body = self.xml_body.format(user=user, password=password)

        self.products = []

    def get_products(self):
        """
        Reads all products from the assigned service/server and wraps them in the Product class.

        :return: All products in a list
        :rtype: list of Product
        """
        result_object = untangle.parse(self.service.request('POST', self.xml_body))
        for product in result_object.soap_Envelope.soap_Body.getProductsResponse.products.product:
            self.products.append(
                Product(
                    product.name.cdata,
                    self.user,
                    self.password,
                    self.service,
                    display_name=product.display_name.cdata
                )
            )
        return self.products
