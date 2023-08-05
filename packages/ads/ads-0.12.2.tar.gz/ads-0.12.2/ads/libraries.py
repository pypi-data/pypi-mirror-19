"""
Interface to the adsws libraries api.
"""

import warnings
import six
import math
from werkzeug.utils import cached_property
import json

from .config import LIBRARIES_URL
from .exceptions import SolrResponseParseError, APIResponseError
from .base import BaseQuery, APIResponse
from .metrics import MetricsQuery
from .export import ExportQuery
from .search import SearchQuery




class Library(list):
    """
    An object to represent a single record in NASA's Astrophysical
    Data System.
    """
    def __init__(self, **kwargs):
        """
        :param kwargs: Set object attributes from kwargs
        """

        # If no ID given, then create one remotely and assign.

        self._raw = kwargs
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)
        return None

    """  
    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        return self.__unicode__().encode("utf-8")

    def __unicode__(self):
        return u"<'{name}' owned by {owner}>".format(
            name=self._raw.get("name", "Unnamed library"),
            owner=self._raw.get("owner", "Unknown owner"))
    """
    

    def __eq__(self, other):
        if self._raw.get("id") is None or other._raw.get("id") is None:
            raise TypeError("Cannot compare libraries without id values")
        return self._raw['id'] == other._raw['id']

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, index):
        return list.__getitem__(index)


    def keys(self):
        return self._raw.keys()

    def items(self):
        return self._raw.items()

    def iteritems(self):
        return six.iteritems(self._raw)


    @property
    def documents(self):

        try:
            return self._documents

        except AttributeError:
            self._documents = self._get_documents()

        return self._documents


    def _get_documents(self, bibcodes=None, **kwargs):

        if bibcodes is None:
            response = BaseQuery().session.get(
                "{}libraries/{}".format(LIBRARIES_URL, self.id))

            # We just get back bibcodes.
            bibcodes = response.json()["documents"]

        return list(SearchQuery(
            q="bibcode:({})".format(" OR ".join(bibcodes)),
            **kwargs))


    # Append/add a document

    # Remove an article

    #num_users,owner,public,permission,date_last_modified,date_created
    #num_documents,description,id,name,permissions,


class LibraryQuery(BaseQuery):

    def __init__(self, library_id):
        """
        Return a library.
        """

        self._query = library_id


    def execute(self):

        response = self.session.get(
            "{}libraries/{}".format(LIBRARIES_URL, self._query))
        json = response.json()

        library = Library(**json["metadata"])
        library._documents = library._get_documents(json["documents"])

        return library 



class LibrariesResponse(APIResponse):
    """
    Data structure that represents a response from the ads library service
    """
    def __init__(self, raw):
        self._raw = raw
        self.json = raw.json()
        self.libraries = [Library(**kwd) for kwd in self.json["libraries"]]

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        return self.__unicode__().encode("utf-8")

    def __unicode__(self):
        return self.libraries




class LibrariesQuery(BaseQuery):
    """
    Represents a query to the adsws libraries service
    """

    HTTP_ENDPOINT = LIBRARIES_URL + "libraries"

    def execute(self):
        """
        Execute the http request to the metrics service
        """

        self.response = LibrariesResponse.load_http_response(
            self.session.get(self.HTTP_ENDPOINT)
        )
        return self.response.libraries



def retrieve():
    """
    Retrieve the list of all libraries that belong to the current user.
    """

    return LibrariesQuery().execute()


#def create():
#def read()/retrieve
#updates should be done by popping or changing the libraries themselves.
#def delete()




"""
Some use-cases:

lib = ads.Library("something", articles=[article1, article2, article3])

lib2 = ads.libraries.LibrariesQuery("name")

# On-demand updates.
lib += article4
lib -= article2

"""


