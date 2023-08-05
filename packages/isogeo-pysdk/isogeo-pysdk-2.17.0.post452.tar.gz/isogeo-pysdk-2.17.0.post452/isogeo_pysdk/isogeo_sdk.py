# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, print_function, unicode_literals)
# -----------------------------------------------------------------------------
# Name:         Isogeo
# Purpose:      Python minimalist SDK to use Isogeo API
#
# Author:       Julien Moura (@geojulien)
#
# Python:       2.7.x
# Created:      22/12/2015
# Updated:      10/01/2016
# -----------------------------------------------------------------------------

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import base64
from collections import Counter
import socket
import locale
import logging
from math import ceil
from sys import platform as opersys

# 3rd party library
import arrow
import requests

# modules
try:
    from . import translator
except ValueError:
    import translator

# #############################################################################
# ########## Classes ###############
# ##################################

__all__ = ['Isogeo', 'IsogeoTranslator']


class Isogeo(object):
    """ Abstraction class for Isogeo REST API.
    Full doc at: https://goo.gl/V3iB9R
    Swagger at: http://chantiers.hq.isogeo.fr/docs/Isogeo.Api/latest/Api.V1/
    """
    # -- ATTRIBUTES -----------------------------------------------------------
    api_urls = {"prod": "api",
                "qa": "api.qa"
                }

    sub_resources_available = ["conditions",
                               "contacts",
                               "coordinate-system",
                               "events",
                               "feature-attributes",
                               "keywords",
                               "layers",
                               "limitations",
                               "links",
                               "operations",
                               "serviceLayers",
                               "specifications"
                               ]

    geo_relations_available = ["contains",
                               "disjoint",
                               "equal",
                               "intersects",
                               "overlaps",
                               "within"
                               ]

    thesaurus_available = {"isogeo": "1616597fbc4348c8b11ef9d59cf594c8",
                           "inspire-theme": "",
                           "iso19115-topic": ""
                           }

    # -- BEFORE ALL -----------------------------------------------------------

    def __init__(self, client_id, client_secret,
                 platform="prod", lang="en", proxy=None):
        """ Isogeo connection parameters

        Keyword arguments:
        client_id -- application identifier
        client_secret -- application secret
        platform -- switch between to production or quality assurance platform
        lang -- language asked for localized tags (INSPIRE themes).
        Could be "en" [DEFAULT] or "fr".
        proxy -- to pass through the local
        proxy. Optional. Must be a dict { 'protocol':
        'http://username:password@proxy_url:port' }.\ e.g.: {'http':
        'http://martin:p4ssW0rde@10.1.68.1:5678',\ 'https':
        'http://martin:p4ssW0rde@10.1.68.1:5678'}")
        """
        super(Isogeo, self).__init__()
        self.id = client_id
        self.ct = client_secret

        # checking internet connection
        if self.check_internet_connection:
            logging.info("Your're connected to the world!")
        else:
            logging.error("Internet connection doesn't work.")
            raise EnvironmentError("Internet connection issue.")

        # testing parameters
        if len(client_secret) != 64:
            logging.error("App secret length issue: it should be 64 chars.")
            raise ValueError(1, "Secret isn't good: : it must be 64 chars.")
        else:
            pass

        # platform to request
        if platform == "prod":
            self.base_url = self.api_urls.get(platform)
            logging.info("Using production platform.")
        elif platform == "qa":
            self.base_url = self.api_urls.get(platform)
            logging.info("Using Quality Assurance platform (reduced perfs).")
        else:
            logging.error("Platform must be one of " + self.api_urls)
            raise ValueError(3, "Platform must be one of " + self.api_urls)

        # setting language
        if lang.lower() not in ("fr", "en"):
            logging.info("Isogeo API is only available in English ('en', "
                         "default) or French ('fr'). "
                         "Language has been set on English.")
            self.lang = "en"
        else:
            self.lang = lang.lower()

        # setting locale according to the language passed
        try:
            if opersys == 'win32':
                if lang.lower() == "fr":
                    locale.setlocale(locale.LC_ALL, str("fra_fra"))
                else:
                    locale.setlocale(locale.LC_ALL, str("uk_UK"))
            else:
                if lang.lower() == "fr":
                    locale.setlocale(locale.LC_ALL, str("fr_FR.utf8"))
                else:
                    locale.setlocale(locale.LC_ALL, str("en_GB.utf8"))
        except locale.Error:
            logging.error('Selected locale is not installed')

        # handling proxy parameters
        # see: http://docs.python-requests.org/en/latest/user/advanced/#proxies
        if proxy and type(proxy) is dict and 'http' in proxy.keys():
            logging.info("Proxy activated")
            self.proxies = proxy
        elif proxy and type(proxy) is not dict:
            logging.info("Proxy syntax error. Must be a dict: { 'protocol': "
                         "'http://user:password@proxy_url:port' }."
                         "e.g.: {'http': 'http://martin:1234@10.1.68.1:5678',"
                         "'https': 'http://martin:p4ssW0rde@10.1.68.1:5678'}")
            return
        else:
            self.proxies = {}
            logging.info("No proxy set. Use default configuration.")
            pass

        # get API version
        logging.info("API version in use: {}".format(self.get_api_version()))

    # -- API CONNECTION ------------------------------------------------------

    def connect(self, client_id=None, client_secret=None):
        """
        Isogeo API uses oAuth  2.0 protocol (http://tools.ietf.org/html/rfc6749)
        see: https://docs.google.com/document/d/11dayY1FH1NETn6mn9Pt2y3n8ywVUD0DoKbCi9ct9ZRo/edit?usp=sharing#heading=h.1rjxk9mvjoc0
        """
        # instanciated or direct call
        if not client_id and not client_secret:
            client_id = self.id
            client_secret = self.ct
        else:
            pass

        # Basic Authentication header in Base64 (https://en.wikipedia.org/wiki/Base64)
        # see: http://tools.ietf.org/html/rfc2617#section-2
        credentials = base64.b64encode(client_id + ":" + client_secret)
        headers = {"Authorization": "Basic " + credentials}

        # using Client Credentials Grant method
        # see: http://tools.ietf.org/html/rfc6749#section-4.4
        payload = {"grant_type":"client_credentials"}

        # passing request to get a 24h bearer
        # see: http://tools.ietf.org/html/rfc6750#section-2
        id_url = "https://id.{}.isogeo.com/oauth/token".format(self.base_url)
        try:
            conn = requests.post(id_url,
                                 headers=headers,
                                 data=payload,
                                 proxies=self.proxies)
        except ConnectionError:
            return "No internet connection"

        # just a fast check
        check_params = self.check_api_response(conn)
        if check_params == 1:
            pass
        elif type(check_params) == tuple and len(check_params) == 2:
            raise ValueError(2, check_params)

        # getting access
        axx = conn.json()
        bearer = axx.get("access_token")

        # get the limit date
        expiration_date = arrow.get(arrow.utcnow().timestamp
                          + axx.get("expires_in"))

        # end of method
        return (bearer, expiration_date)

    # -- API PATHS ------------------------------------------------------------

    def shares(self, jeton, prot="https"):
        """ Get information about shares which feed the application
        """
        # checking bearer validity
        jeton = self.check_bearer_validity(jeton)

        # passing auth parameter
        head = {"Authorization": "Bearer " + jeton[0]}
        shares_url = "{}://v1.{}.isogeo.com/shares/".format(prot,
                                                            self.base_url)
        shares_req = requests.get(shares_url,
                                  headers=head,
                                  proxies=self.proxies)

        # checking response
        self.check_api_response(shares_req)

        # end of method
        return shares_req.json()

    def share(self, jeton, share_id, prot="https"):
        """ Get information about a share and its applications
        """
        # checking bearer validity
        jeton = self.check_bearer_validity(jeton)

        # passing auth parameter
        head = {"Authorization": "Bearer " + jeton[0]}
        share_url = "{}://v1.{}.isogeo.com/shares/{}".format(prot,
                                                             self.base_url,
                                                             share_id)
        share_req = requests.get(share_url,
                                 headers=head,
                                 proxies=self.proxies)

        # checking response
        self.check_api_response(share_req)

        # end of method
        return share_req.json()

    def search(self,
               jeton,
               query="",
               bbox=None,
               poly=None,
               georel=None,
               order_by="_created",
               order_dir="desc",
               page_size=100,
               offset=0,
               specific_md=None,
               sub_resources=None,
               whole_share=True,
               prot="https"):
        """ Search request

        Keyword arguments:
        jeton -- API bearer
        query -- search terms. It could be a simple string like 'oil' or a tag
        like 'keyword:isogeo:formations' or 'keyword:inspire-theme:landcover'.
        \nThe AND operator is applied when various tags are passed.\nEmpty by default.
        bbox -- Bounding box to limit the search. Must be a 4 list of coordinates in WGS84 (EPSG 4326).\
        \nCould be completed with the georel parameter
        poly -- Geographic criteria for the search, in WKT format.\
        \nCould be completed by the georel parameter.
        georel -- spatial operator to apply to the bbox or poly parameters.\
        \n\tAvailable values: 'contains', 'disjoint', 'equals', 'intersects' [DEFAULT],\
        'overlaps', 'within'. To get available values: 'isogeo.geo_relations_available'.
        order_by -- to sort results. \n\tAvailable values:\n\t'_created': metadata
        creation date [DEFAULT]\n\t'_modified': metadata last update\n\t'title': metadata title\n\t'created': data
        creation date (possibly None)\n\t'modified': data last update date\n\t'relevance': relevance score.
        order_dir -- sorting direction. \n\tAvailable values:\n\t'desc':
        descending [DEFAULT]\n\t'asc': ascending
        page_size -- limits the number of results. Useful to paginate results display.
        offset -- offset
        specific_md -- Limits the search to the specified identifiers
        sub_resources -- subresources that should be returned. Must be a list of strings.\\n
        To get available values: 'isogeo.sub_resources_available'
        whole_share -- option to return all results or only the page size. True by DEFAULT.
        prot -- https [DEFAULT] or http (useful for development and tracking requests).

        see: https://docs.google.com/document/d/11dayY1FH1NETn6mn9Pt2y3n8ywVUD0DoKbCi9ct9ZRo/edit?usp=sharing#heading=h.yusgqavk96n1
        """
        # checking bearer validity
        jeton = self.check_bearer_validity(jeton)

        # specific resources specific parsing
        if type(specific_md) is list and len(specific_md) > 0:
            specific_md = ",".join(specific_md)
        elif specific_md is None:
            specific_md = ""
        else:
            specific_md = ""

        # sub resources specific parsing
        if sub_resources == "all":
            sub_resources = self.sub_resources_available
        elif type(sub_resources) is list and len(sub_resources) > 0:
            sub_resources = ",".join(sub_resources)
        elif sub_resources is None:
            sub_resources = ""
        else:
            sub_resources = ""
            return "Error: sub_resources arg must be a list, 'all' or empty"

        # handling request parameters
        payload = {'_id': specific_md,
                   '_include': sub_resources,
                   '_lang': self.lang,
                   '_limit': page_size,
                   '_offset': offset,
                   'box': bbox,
                   'geo': poly,
                   'rel': georel,
                   'ob': order_by,
                   'od': order_dir,
                   'q': query,
                   }

        # search request
        head = {"Authorization": "Bearer " + jeton[0]}
        search_url = "{}://v1.{}.isogeo.com/resources/search".format(prot,
                                                                     self.base_url)
        search_req = requests.get(search_url,
                                  headers=head,
                                  params=payload,
                                  proxies=self.proxies)
        # fast response check
        self.check_api_response(search_req)

        # serializing result into dict and storing resources in variables
        search_rez = search_req.json()
        resources_count = search_rez.get('total')  # total of metadatas shared

        # handling Isogeo API pagination
        # see: https://docs.google.com/document/d/11dayY1FH1NETn6mn9Pt2y3n8ywVUD0DoKbCi9ct9ZRo/edit?usp=sharing#heading=h.bg6le8mcd07z
        if resources_count > page_size and whole_share:
            # if API returned more than one page of results, let's get the rest!
            metadatas = []  # a recipient list
            payload['_limit'] = 100  # now it'll get pages of 100 resources
            # let's parse pages
            for idx in range(0, int(ceil(resources_count / 100)) + 1):
                payload['_offset'] = idx * 100
                search_req = requests.get(search_url,
                                          headers=head,
                                          params=payload,
                                          proxies=self.proxies)
                # storing results by addition
                metadatas.extend(search_req.json().get('results'))
            search_rez['results'] = metadatas
        else:
            pass

        # end of method
        return search_rez

    def resource(self, jeton, id_resource, sub_resources=[], prot="https"):
        """ Get complete or partial metadata about one specific resource
        (ie a vector dataset).

        Keyword arguments:
        jeton -- API bearer
        id_resource -- UUID of the resource to get
        sub_resources -- subresources that should be returned. Must be a list of strings.\\n
        To get available values: 'isogeo.sub_resources_available'
        prot -- https [DEFAULT] or http (useful for development and tracking requests).
        """
        # checking bearer validity
        jeton = self.check_bearer_validity(jeton)

        # sub resources specific parsing
        if sub_resources == "all":
            sub_resources = self.sub_resources_available
        elif type(sub_resources) is list:
            sub_resources = ",".join(sub_resources)
        else:
            return "Error: sub_resources argument must be a list or 'all'"

        # handling request parameters
        payload = {'_include': sub_resources
                   }

        # resource search
        head = {"Authorization": "Bearer " + jeton[0]}
        md_url = "{}://v1.{}.isogeo.com/resources/{}".format(prot,
                                                             self.base_url,
                                                             id_resource)
        resource_req = requests.get(md_url,
                                    headers=head,
                                    params=payload,
                                    proxies=self.proxies
                                    )
        self.check_api_response(resource_req)

        # end of method
        return resource_req.json()

    def thesaurus(self, jeton,
                  thez_id="1616597fbc4348c8b11ef9d59cf594c8",
                  page_size=100,
                  offset=0,
                  sub_resources=[],
                  prot="https"):
        """Gets information about thesaurus
        """
        # checking bearer validity
        jeton = self.check_bearer_validity(jeton)

        # sub resources specific parsing
        if sub_resources == "all":
            sub_resources = self.sub_resources_available
        elif type(sub_resources) is list:
            sub_resources = ",".join(sub_resources)
        else:
            return "Error: sub_resources argument must be a list or 'all'"

        # handling request parameters
        payload = {'th': thez_id,
                   '_include': sub_resources,
                   '_limit': page_size,
                   '_offset': offset,
                   }

        # passing auth parameter
        head = {"Authorization": "Bearer " + jeton[0]}
        thez_url = "{}://v1.{}.isogeo.com/groups/08b3054757544463abd06f3ab51ee491/keywords/search".format(prot,
                                                            self.base_url)
        thez_req = requests.get(thez_url,
                                headers=head,
                                params=payload,
                                proxies=self.proxies)

        # checking response
        self.check_api_response(thez_req)

        # end of method
        return thez_req.json()

    # -- DOWNLOADS -----------------------------------------------------------

    def xml19139(self, jeton, id_resource, prot="https"):
        """Gets resource exported into XML ISO 19139"""

        # checking bearer validity
        jeton = self.check_bearer_validity(jeton)

        # resource search
        head = {"Authorization": "Bearer " + jeton[0]}
        md_url = "{}://v1.{}.isogeo.com/resources/{}.xml".format(prot,
                                                                 self.base_url,
                                                                 id_resource)
        xml_req = requests.get(md_url,
                               headers=head,
                               stream=True,
                               proxies=self.proxies
                               )

        # end of method
        return xml_req

    # -- UTILITIES -----------------------------------------------------------

    def check_bearer_validity(self, jeton):
        """ Isogeo ID delivers authentication bearers which are valid during
        24h, so this method checks the validity of the token (jeton in French)
        with a 30 mn anticipation limit, and renews it if necessary.

        jeton = must be a tuple like (bearer, expiration_date)

        see: http://tools.ietf.org/html/rfc6750#section-2
        FI: 24h = 86400 seconds, 30 mn = 1800, 5 mn = 300
        """
        if (jeton[1].timestamp - arrow.utcnow().timestamp) < 60:
            jeton = self.connect(self.id, self.ct)
            logging.info("Your bearer was about to expire, so has been renewed. Just go on!")
        else:
            logging.info("Your bearer is still valid. Just go on!")
            pass

        # end of method
        return jeton

    def check_api_response(self, response):
        """Checks the API response and raise exceptions if needed."""
        if response.status_code == 200:
            logging.info("Everything is OK dude, just go on!")
            pass
        elif response.status_code >= 400:
            logging.error("Something's wrong Houston, check your parameters again!")
            logging.error("{}: {} - {}".format(response.status_code,
                                               response.reason,
                                               response.json().get("error")))
            # logging.error(dir(response))
            return 0, response.status_code
        else:
            pass

        # end of method
        return 1

    def get_api_version(self, prot="https"):
        """Gets Isogeo API version. No need for authentication."""
        # resource search
        api_version_url = "{}://v1.{}.isogeo.com/about".format(prot,
                                                               self.base_url
                                                               )
        api_version_req = requests.get(api_version_url,
                                       proxies=self.proxies
                                       )
        # checking response
        self.check_api_response(api_version_req)

        # end of method
        return api_version_req.json().get("version")

    def check_internet_connection(self, remote_server="www.isogeo.com"):
        """Tests if an internet connection is operational
        source: http://stackoverflow.com/a/20913928/2556577
        """
        try:
            # see if we can resolve the host name -- tells us if there is
            # a DNS listening
            host = socket.gethostbyname(remote_server)
            # connect to the host -- tells us if the host is actually
            # reachable
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        # end of method
        return False

# ##############################################################################
# ##### Stand alone program ########
# ##################################

if __name__ == '__main__':
    """ standalone execution """
    # ------------ Specific imports ----------------
    import ConfigParser     # to manage options.ini
    from os import path

    # ------------ Settings from ini file ----------------
    settings_file = r"isogeo_params.ini"

    if not path.isfile(path.realpath(settings_file)):
        print("ERROR: to execute this script as standalone, you need to store "
              "your Isogeo application settings in a isogeo_params.ini file. "
              "You can use the template to set your own.")
        import sys
        sys.exit()
    else:
        pass

    config = ConfigParser.SafeConfigParser()
    config.read(settings_file)

    share_id = config.get('auth', 'app_id')
    share_token = config.get('auth', 'app_secret')

    # ------------ Real start ----------------
    # instanciating the class
    isogeo = Isogeo(client_id=share_id,
                    client_secret=share_token,
                    lang="fr")

    # getting a token
    jeton = isogeo.connect()

    # get thesauri=
    # thesauri = isogeo.thesaurus(jeton, "http")
    # print(len(thesauri), thesauri)
    # print(len(thesauri))
    # print(thesauri[0].keys())

    # let's search for metadatas!
    search = isogeo.search(jeton,
                           # sub_resources='all',
                           # sub_resources=["conditions", "contacts"],
                           # sub_resources=isogeo.sub_resources_available,
                           # query="keyword:isogeo:2015",
                           prot='https')

    # quick & dirty tests
    assert(type(search) != unicode)
    assert(type(search) == dict)
    assert("envelope" in search.keys())
    assert("limit" in search.keys())
    assert("offset" in search.keys())
    assert("query" in search.keys())
    assert("results" in search.keys())
    assert("tags" in search.keys())
    assert("total" in search.keys())
    assert(type(search.get("results")) == list)

    # API Version
    print("Current Isogeo public API version: ", isogeo.get_api_version())
