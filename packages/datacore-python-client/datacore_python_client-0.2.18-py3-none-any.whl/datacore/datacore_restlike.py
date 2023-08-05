"""
Created on Sep 15, 2016

@author: Vincent Medina, EveryMundo, vincent@everymundo.com


This module represents a RESTful-like end-user interface for interacting with datacore. This is to be distinguished
from the MongoDB-like interface that is currently in development. This provides a lower-level, yet object-oriented
interface into datacore, that is geared to be imported or lend inheritance to specific applications.

Major Structure:

:exception DatacoreException: A custom class that offers a wrapper for http and parsing errors, allowing for greater
    visibliity to bugs that occur during the interaction with the database.
:object Access: An access object that interfaces with datacore.
"""

# Standard library imports
import json
import time
import random
import datetime
import logging
from typing import AnyStr, Any, Dict, Iterable, Sequence

# Non-standard library imports
import requests

# Package imports
from datacore.types import Header, Query, Payload


class DatacoreException(Exception):
    """Datacore exception handler, base class.
    This is a very basic error handler that will throw anything passed to it."""
    def __init__(self, code, message):
        self.code = code
        self.message = message


class Access(object):
    """This class serves as an API/wrapper with the datacore REST API service.

    Serves as a base for any access client.

    Is used currently as a base class for table-specific implementations.
    """

    def __init__(self, user: AnyStr, secret: AnyStr):
        """
        :param user: datacore user
        :type user: AnyStr
        :param secret: datacore secret
        :type secret: AnyStr
        """
        self._user = ''
        self._auth = ''
        self._headers = {}
        self._sync_headers = {}
        self.new_authentication(user, secret)

    @property
    def user(self) \
            -> str:
        """

        :return user: username
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, username: AnyStr) \
            -> None:
        """

        :param username: new value for self.user
        :type username: str
        :return:
        """
        self._user = str(username)

    @property
    def auth(self) \
            -> str:
        """

        :return authentication: secret to access datacore endpoint
        :rtype: str
        """
        return self._auth

    @auth.setter
    def auth(self, authentication: AnyStr) \
            -> None:
        """

        :param authentication: new authentication value
        :type authentication: str
        """
        self._auth = str(authentication)

    @property
    def headers(self) \
            -> Header:
        """

        :return headers: Headers to be used in datacore restful interactions
        :rtype: dict
        """
        return self._headers

    @headers.setter
    def headers(self, headers: Header) \
            -> None:
        """

        :param headers:
        :return:
        """
        assert "Authorization" in headers.keys(), "'Authorization' must be present in the headers"
        self._headers = headers

    @property
    def sync_headers(self) \
            -> Header:
        """
        Same as headers, but with an extra "X-Sync" key and value for synchronous posting for large or real-time
        posts.

        :return sync_headers:
        :rtype: dict
        """
        return self._sync_headers

    @sync_headers.setter
    def sync_headers(self, sync_headers: Header) \
            -> None:
        """

        :param sync_headers:
        :type sync_headers: dict
        """
        self._sync_headers = sync_headers

    def new_authentication(self, user: AnyStr, secret: AnyStr) \
            -> None:
        """
        When setting new authentication for a new table, do not directly use the setters if possible. Use
        new_authentication, which will also update the headers value.

        :param user: Datacore Username
        :param secret: Datacore Secret
        :type user: AnyStr
        :type secret: AnyStr
        """
        self.user = user
        self.auth = secret
        self.headers = {
            'Content-Type': 'application-json',
            'Accept': 'application-json',
            'Authorization': self.auth
        }
        self.sync_headers = {
            'X-Sync': "True",
            'Content-Type': 'application-json',
            'Accept': 'application-json',
            'Authorization': self.auth
        }

    def check_date(self, url: AnyStr, match: Query, group: Query) \
            -> datetime.date:
        """ Checks for a report date (date of data, not of reporting.) If
        the date is in record, returns true, if not, returns false.

        Untested, and as of yet, unsupported for that reason.

        :param url: datacore aggregation endpoint to query form
        :type url: str
        :param match: mongodb json query match object
        :type match: dict
        :param group: mongodb json query group object
        :type group: dict
        :return date_in_datacore:
        :rtype datetime.date:
        """
        response = self.get(
            url=url,
            query=[
                match,
                group
            ],
            agg=True
        )
        logging.info(response)
        if response is None:
            logging.info("No data found")
            # Error in the pull -- bad data
            return None
        elif not response:
            logging.info("No data found-- empty response")
            # No last date
            return None
        else:
            logging.info("Data found, and is valid.")
            # We have a response that we can deal with
            date_str = response[0]["last"].replace("-", "")
            return datetime.date(
                int(date_str[0:4]),
                int(date_str[4:6]),
                int(date_str[6:8])
            )

    def _check_table(self, table_url: AnyStr, query: Query, **kwargs: Dict[str, Any]) \
            -> bool:
        """
        Checks table at table_url for existance of data with conditions query. Returns boolean.

        :param table_url: read endpoint of  table
        :param query: query to pose (<body> in ?q=<body>)
        :arg kwargs: keyword arguments to be passed to Access.get()
        :type table_url: str
        :type query: dict
        :returns in_table:
        :rtype: bool
        """
        data = self.get(table_url, query=query, **kwargs)
        if len(data) >= 1:
            return True
        else:
            return False

    def post_lines(self, dest_url: AnyStr, data: Payload, sync=False, verbose=False) \
            -> None:
        """Posts lines to datacore, one at a time. This is very time exhaustive,
        and is meant to be used only for purposes of debugging and testing.

        :param dest_url: datacore write endpoint
        :type dest_url: str
        :param data: data to upload
        :type data: list of dict
        :param sync: Set to true if accessing synchronous endpoint
        :type sync: bool
        :param verbose: if true, then much more visibility. Exposes data, so only use during development. Defaults to
            False
        :type verbose: bool
        :raises DatacoreException: upon failure
        """
        # Do nothing if there is no data to upload
        if not data:
            return None
        logging.info("="*75)
        logging.info("Uploading to dataCORE")
        data_set = data
        for line in data_set:
            # Line by line
            for j in range(10):
                # Incremental backoff
                try:
                    if verbose:
                        logging.info(json.dumps(line))
                    if not sync:
                        response = requests.post(
                            dest_url.strip(),
                            data=json.dumps(line),
                            headers=self.headers,
                            timeout=180.0
                        )
                    else:
                        response = requests.post(
                            dest_url.strip(),
                            data=json.dumps(line),
                            headers=self.sync_headers,
                            timeout=180.0
                        )
                    if verbose:
                        logging.warning(json.loads(response.text))
                    if response.status_code in [200, 202]:
                        # Success.
                        logging.info("Sub-post uploaded.")
                        logging.info("-" * 75)
                        # Trying to one-up the python garbage collector
                        response = None
                        part = None
                        break
                    elif response.status_code == 413:
                        # This actually should never happen
                        raise DatacoreException(
                            413,
                            "Sub-post still too big: {b}".format(b=response.text)
                        )
                    elif response.status_code == 502:
                        # Internet issues
                        if j == 9:
                            logging.warning("Couldn't communicate with datacore.")
                            raise DatacoreException(
                                response.status_code,
                                "Couldn't establish a connection. Please check your connection." + response.text
                            )
                        logging.info(
                            "Bad Gateway... Possible internet connection issues... will try again shortly.")
                        response = None
                    elif response.status_code >= 500:
                        # Other misc issues
                        if j == 9:
                            logging.warning("Couldn't communicate with datacore.")
                            raise DatacoreException(
                                response.status_code,
                                "Datacore API service is likely down. Please try again at another time." + response.text
                            )
                    else:
                        logging.info("Subpacket post error")
                        logging.info("Status: " + str(response.status_code))
                        logging.info(response.text)
                        raise (DatacoreException(response.status_code, response.text))
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    # Just try again lolol
                    pass
                time.sleep(2 ** j + random.random())
            logging.info("Uploaded a line of data.")
            logging.info("-"*75)

    def get(self, url: AnyStr, query=None, fields=None, sort='', sync=False, agg=False, limit=1000) \
            -> Payload:
        """Returns dataCore results for a given period, defualt first 100 pages.

        Note: In non aggregation endpoint usage, this method paginates based on the number of results that would
        be returned (datacore backend uses COUNT to determine this.) However, this is not entirely the case with
        the aggregation endpoint. In order ot mitigate this, pagination is not supported, however, the maximum
        result package size currently supported is 50000 (rows). If a response would return more entries, please
        select for a more granulated data set in the query.

        :param url: str(endpoint_url)
        :type url: str
        :param fields: (optional)list(*fields)
        :type fields: list
        :param query: (optional)dict(**query)
        :type query: list or dict
        :param agg: (optional) If true, use aggreagation limits
        :type agg: bool
        :param limit: (optional)int(page_size) Defaults to the maximum value 1000
        :type limit: int
        :param sort: (optional)string(sort_condition)
        :type sort: str
        :param sync: (optional)bool Use synchronous headers. Default False.
        :type sync: bool
        :return data: list(data) where entries are dicts. May be empty.
        :rtype List[Dict[Any, Any]]:
        :raises DatacoreException: when the issue is in the interaction with datacore
        """
        base = url
        # Output
        data = []
        # Pagination index
        page = 0
        if not agg:
            max_page = 1
        else:
            # Aggregation case
            # Aggregation does not support pagination, but allows for larger data sets to be returned.
            max_page = 1
            limit = 50000
        # While there are still pages to get
        while page < max_page:
            # Page up to (first index) or (next index)
            page += 1
            # Reset the Query URL
            if not agg:
                qurl = base + "?limit={l}".format(l=limit) + "&page={p}".format(p=page)
            else:
                qurl = base + "?limit={l}".format(l=limit)
            if query:
                par = json.dumps(query)
                qurl += "&q={p}".format(p=par)
                # put in the query parameters
            if fields:
                qurl += "&s="
                for col in fields:
                    # add in each of the urls
                    qurl += "{c},".format(c=col)
                qurl = qurl[0:len(url) - 1]
                # ditch that last comma
            if sort:
                qurl += "&sort=" + sort
            # Loop controls
            i = 0
            getting = True
            # Attempt get of page
            while i <= 2 and getting:
                try:
                    if not sync:
                        response = requests.get(qurl.strip(), headers=self.headers, timeout=180.0)
                    else:
                        response = requests.get(qurl.strip(), headers=self.sync_headers, timeout=180.0)
                    logging.warning("Datacore GET status code: {s}".format(s=response.status_code))
                    if response.status_code in [200, 202]:
                        # We got a good thing going
                        # This should be good
                        body = json.loads(response.text)
                        if ("count" in body.keys()) or ("numOfDocs" in body.keys()):
                            # if there is a non empty response returned
                            logging.info(
                                "Retrieved {l} rows of document from datacore".format(
                                    l=len(body["data"])
                                )
                            )
                            # Count returns the number of rows that fit the query
                            # If we have data in our query, add it to our output
                            data.extend(
                                body["data"]
                            )
                            if len(body["data"]) == 0:
                                logging.warning("Zero Rows returned. Expecting {x} pages total".format(x=max_page))
                        if page == 1:
                            # Important, reset max_page if we have more rows than was given
                            if agg:
                                # Different key name for aggregation endpoint and read endpoint
                                max_page = 1
                            else:
                                # Read endpoint key
                                max_page = (int(body["count"]) // limit) + 1
                                # Visibility
                                logging.info("There are {x} total number of pages to process.".format(x=max_page))
                        getting = False
                    elif response.status_code == 504:
                        logging.warning("STATUS 504")
                        # Bad
                        if i == 0:
                            i += 1
                            time.sleep(4 + random.random())
                        else:
                            raise DatacoreException(504, response.text)
                    elif response.status_code >= 500:
                        # Bad
                        logging.warning("STATUS {r}".format(r=response.status_code))
                        if i == 0:
                            i += 1
                            time.sleep(2 ** i + random.random())
                        else:
                            raise DatacoreException(response.status_code, response.text)
                    else:
                        logging.warning("UNKNOWN ERROR: {e}".format(e=response.text))
                        # Somehow we didn't catch it
                        if i == 0:
                            # Retry
                            time.sleep(4 + random.random())
                            i += 1
                        else:
                            # Assuming this did it
                            raise DatacoreException(response.status_code, response.text)
                except json.decoder.JSONDecodeError:
                    # Bad upload possibly? Probably unlikely, but possible?
                    logging.warning(
                        "Bad string returned from datacore: {t}".format(
                            t=response.text
                        )
                    )
                    raise DatacoreException(
                        "FormatError",
                        "Data was returned in a bad formatting."
                    )
                except requests.exceptions.ConnectionError as error:
                    if i == 2:
                        # This only happens as a client-side connection issue. Only happened once.
                        raise DatacoreException(
                            "ConnectionError",
                            "There was an issue connecting to datacore. (Are you connected to the internet?)"
                        )
                    else:
                        time.sleep(8 + random.random())
                        logging.warning("Connection error during datacore pull... Retrying...")
                        time.sleep(4)
                        i += 1
                except requests.exceptions.Timeout:
                    if i == 2:
                        # This occurs when no data is returned
                        raise DatacoreException(
                            "TimeoutError",
                            "Read connection timed out while attempting to connect."
                        )
                    else:
                        time.sleep(8 + random.random())
                        logging.warning("Connection error during datacore pull... Retrying...")
                        time.sleep(4)
                        i += 1
            # Remind us what page we are on currently
            logging.info("Page: {p}".format(p=page))
        return data

    def yield_get(self, url: AnyStr, query=None, fields=None, sort='', agg=False, limit=1000) \
            -> Iterable[Payload]:
        """Yields dataCore results for a given page by page.

        While there is support for aggregation, this is suboptimal and actually contrary to the lower-overhaed goals
        this method attempts to accomplish.

        :param url: str(endpoint_url)
        :type url: str
        :param fields: (optional)list(*fields)
        :type fields: list
        :param query: (optional)dict(**query)
        :type query: list
        :param limit: (optional)int(page_size) Defaults to the maximum value 1000
        :type limit: int
        :param sort: (optional)string(sort_condition)
        :type sort: str
        :param agg: if true, aggregation endpoint (NOT RECOMMENDED TO USE, UNDEFINED BEHAVIOR, NOT YET IMPLEMENTED)
        :type agg: bool
        :return data: list(data) where entries are dicts. May be empty.
        :rtype list:
        :raises DatacoreException: when the issue is in the interaction with datacore
        """
        base = url
        # Output
        # Pagination index
        page = 0
        if not agg:
            # Standard get request
            head = self.head(
                url + "?q=" + json.dumps(query)
                if query
                else
                url
            )
            if "x-count" in head.keys():
                max_page = int(head["x-count"])
            else:
                logging.warning("No headers while determining max page in datacore GET: {h}".format(h=head))
                max_page = 1
        else:
            # Aggregation case
            # Aggregation does not support pagination, but allows for larger data sets to be returned.
            max_page = 1
            limit = 50000
        # While there are still pages to get
        while page < max_page:
            # Page up to (first index) or (next index)
            page += 1
            # Reset the Query URL
            qurl = base + "?limit={l}".format(l=limit) + "&page={p}".format(p=page)
            if query:
                par = json.dumps(query)
                qurl += "&q={p}".format(p=par)
                # put in the query parameters
            if fields:
                qurl += "&s="
                for col in fields:
                    # add in each of the urls
                    qurl += "{c},".format(c=col)
                qurl = qurl[0:len(url) - 1]
                # ditch that last comma
            if sort:
                qurl += "&sort=" + sort
            # Loop controls
            i = 0
            getting = True
            # Attempt get of page
            while i <= 2 and getting:
                try:
                    response = requests.get(qurl.strip(), headers=self.headers, timeout=180.0)
                    logging.warning("Datacore GET status code: {s}".format(s=response.status_code))
                    if response.status_code in [200, 202]:
                        # We got a good thing going
                        # This should be good
                        body = json.loads(response.text)
                        if ("count" in body.keys()) or ("numOfDocs" in body.keys()):
                            # if there is a non empty response returned
                            logging.info(
                                "Retrieved {l} rows of document from datacore".format(
                                    l=len(body["data"])
                                )
                            )
                            # Count returns the number of rows that fit the query
                            # If we have data in our query, add it to our output
                            yield body["data"]
                        # We have what we came for so...
                        getting = False
                    elif response.status_code == 504:
                        logging.warning("STATUS 504")
                        # Bad
                        if i == 0:
                            i += 1
                            time.sleep(4 + random.random())
                        else:
                            raise DatacoreException(504, response.text)
                    elif response.status_code >= 500:
                        # Bad
                        logging.warning("STATUS {r}".format(r=response.status_code))
                        if i == 0:
                            i += 1
                            time.sleep(2 ** i + random.random())
                        else:
                            raise DatacoreException(response.status_code, response.text)
                    else:
                        logging.warning("UNKNOWN ERROR: {e}".format(e=response.text))
                        # Somehow we didn't catch it
                        if i == 0:
                            # Retry
                            time.sleep(4 + random.random())
                            i += 1
                        else:
                            # Assuming this did it
                            raise DatacoreException(response.status_code, response.text)
                except json.decoder.JSONDecodeError:
                            # Bad upload possibly? Probably unlikely, but possible?
                            logging.warning(
                                "Bad string returned from datacore: {t}".format(
                                    t=response.text
                                )
                            )
                            raise DatacoreException(
                                "FormatError",
                                "Data was returned in a bad formatting."
                            )
                except requests.exceptions.ConnectionError:
                    if i == 2:
                        # This only happens as a client-side connection issue. Only happened once.
                        raise DatacoreException(
                            "ConnectionError",
                            "There was an issuee connecting with datacore. (Are you connected to the internet?)"
                        )
                    else:
                        time.sleep(8 + random.random())
                        logging.warning("Connection error during datacore pull... Retrying...")
                        time.sleep(4)
                        i += 1
                except requests.exceptions.Timeout:
                    if i == 2:
                        # This occurs when no data is returned
                        raise DatacoreException(
                            "TimeoutError",
                            "Read connection timed out while attempting to connect."
                        )
                    else:
                        time.sleep(8 + random.random())
                        logging.warning("Connection error during datacore pull... Retrying...")
                        time.sleep(4)
                        i += 1
            # Remind us what page we are on currently
            logging.info("Page: {p}".format(p=page))

    def post(self, url: AnyStr, data: Payload, sync=False)\
            -> None:
        """Uploads to datacore staging env.

        data should be a list of dictionaries (rows), not yet 'chunked'
        to 1000-row size.

        Note that Google API python client natively handles incremental
        back-off and retries for 5XX response error codes.

        :param url: bulk Url endpoint for the post
        :type url: str
        :param data: data to upload
        :type data: list(dict)
        :param sync: (Optional) Set to True if access to synchronous endpoint is desired. False default.
        :type sync: bool
        :returns None:
        """
        logging.info("="*50)
        logging.info("Uploading to Datacore..")
        logging.info("Number of rows: {d}".format(d=len(data)))
        data_set = self.chunk(data)
        logging.info("Number of chunks: {d}".format(d=len(data_set)))
        logging.info("-"*50)
        i = 1
        dest_url = url
        if not data_set:
            # Just an extra defense in case something changes in clients.py
            return None
        for package in data_set:
            logging.warning("Uploading {i} of {m} chunks to datacore ({r} rows)...".format(
                i=i,
                m=len(data_set),
                r=len(package))
            )
            for j in range(4):
                # Incremental backoff
                try:
                    if not sync:
                        response = requests.post(
                            url=dest_url.strip(),
                            data=json.dumps(package),
                            headers=self.headers,
                            timeout=180.0
                        )
                    else:
                        response = requests.post(
                            url=dest_url.strip(),
                            data=json.dumps(package),
                            headers=self.sync_headers,
                            timeout=180.0
                        )
                    logging.warning("Datacore post status code: {s}".format(s=response.status_code))
                    if response.status_code in [200, 202]:
                        # There is at least some success -- it was recieved
                        logging.info("-" * 50)
                        # But we still must check that there were no issues with specific rows
                        body = json.loads(response.text)
                        if body["count"] != body["success"]:
                            # There is a discrepancy between the number of rows and number of successes
                            index = 0
                            errors = []
                            for row in body["results"]:
                                if "_id" in row.keys():
                                    # This row uploaded to processing correctly
                                    pass
                                else:
                                    # We have an error message at the same index as its source row in the post payload
                                    errors.append([row, package[index]])
                                # Increment index
                                index += 1
                            raise DatacoreException(
                                "post_error",
                                {"errors": errors}
                            )
                        logging.info("Packet upload successful")
                        break
                    elif response.status_code == 413:
                        logging.info("Packet too big; breaking it down and retrying.")
                        logging.info("-"*50)
                        self._sub_post(dest_url.strip(), package, sync=sync)
                        break
                    elif response.status_code == 502:
                        if j == 4:
                            logging.warning("Couldn't communicate with datacore.")
                            raise DatacoreException(
                                response.status_code,
                                "Couldn't establish a connection. Please check connection and try again." \
                                + response.text
                            )
                        logging.info("Bad Gateway... Possible internet connection issues... will try again shortly.")
                    elif response.status_code >= 500:
                        # Something really bad happened.
                        body = json.loads(response.text)
                        if "err" in body.keys():
                            if "field" in body["message"][0]:
                                # User error, easy
                                raise DatacoreException(
                                    response.status_code,
                                    body
                                )
                        else:
                            # In staging, very common -- server-side out of disk space errors
                            logging.warning("Couldn't communicate with datacore.")
                            raise DatacoreException(
                                response.status_code,
                                "Datacore API service is likely down.\n Please try again at another time.\n"
                                + "If this issue persists, please contact EveryMundo to resolve the issue. Ref: \n"
                                + response.text
                            )
                    else:
                        logging.info("Packet post error")
                        logging.info("Status: "+str(response.status_code))
                        logging.info(response.text)
                        raise(DatacoreException(response.status_code, response.text))
                except requests.exceptions.Timeout:
                    # Just try again lol
                    if j < 3:
                        logging.warning("Connection timed out. Retrying...")
                        time.sleep(8 + random.random())
                    else:
                        raise DatacoreException(
                            "TimeoutError",
                            "The connection timed out, and failed retries."
                        )
                except requests.exceptions.ConnectionError:
                    if j == 3:
                        raise DatacoreException(
                            "ConnectionError",
                            "There was an issue connecting with datacore. Are you connected to the internet?"
                        )
                # Allow a wait
                time.sleep(2**j + random.random())
            logging.info("Post chunk successful.")
            logging.info("-"*50)
            i += 1
        logging.warning("Post batch successful.")
        logging.warning("="*50)

    def head(self, qurl: AnyStr)\
            -> Header:
        """
        Performs an HTTP head request given the query onto the target endpoint url.

        :param qurl: endpoint url with the body already assembled
        :type qurl: str
        :return headers: query headers
        :rtype: dict
        """
        i = 0
        while i < 3:
            # Set up a retry loop
            response = requests.head(
                qurl.strip(),
                headers=self.headers,
                timeout=180.0
            )
            logging.info("Datacore HEAD request response status code {s}".format(s=response.status_code))
            if response.status_code in [200, 202]:
                # We're solid and dandy
                headers = response.headers
                return headers
            elif response.status_code == 403:
                raise DatacoreException(
                    403,
                    "Invalid credentials."
                )
            elif response.status_code == 504:
                logging.warning("STATUS 504")
                # Bad
                if i == 0:
                    i += 1
                    time.sleep(4 + random.random())
                else:
                    raise DatacoreException(504, response.text)
            elif response.status_code >= 500:
                # Bad
                logging.warning("STATUS {r}".format(r=response.status_code))
                if i == 0:
                    i += 1
                    time.sleep(2 ** i + random.random())
                else:
                    raise DatacoreException(response.status_code, response.text)
            else:
                logging.warning("UNKNOWN ERROR: {e}".format(e=response.text))
                # Somehow we didn't catch it
                if i == 0:
                    # Retry
                    time.sleep(4 + random.random())
                    i += 1
                else:
                    # Assuming this did it
                    raise DatacoreException(response.status_code, response.text)

    def _sub_post(self, url: AnyStr, data_set: Payload, sync=False)\
            -> None:
        """If a payload (even with < 500 lines) exceeds the datacore upload
        size limit, this breaks it down and uploads the sub-chunks of the
        payload.

        :param url:
        :param data_set:
        :param sync:

        """
        logging.info("Uploading packet as subposts.")
        logging.info("-" * 75)
        data = self.chunk(data_set, chunk_size=len(data_set) // 2)
        for part in data:
            for j in range(5):
                try:
                    if not sync:
                        response = requests.post(
                            url=url.strip(),
                            data=json.dumps(part),
                            headers=self.headers,
                            timeout=180.0
                        )
                    else:
                        response = requests.post(
                            url=url.strip(),
                            data=json.dumps(part),
                            headers=self.sync_headers,
                            timeout=180.0
                        )
                    logging.warning("Datacore post status code: {s}".format(s=response.status_code))
                    if response.status_code in [200, 202]:
                        # There is at least some success -- it was recieved
                        logging.info("-" * 50)
                        # But we still must check that there were no issues with specific rows
                        body = json.loads(response.text)
                        if body["count"] != body["success"]:
                            # There is a discrepancy between the number of rows and number of successes
                            index = 0
                            errors = []
                            for row in body["results"]:
                                if "_id" in row.keys():
                                    # This row uploaded to processing correctly
                                    pass
                                else:
                                    # We have an error message at the same index as its source row in the post payload
                                    errors.append([row, part[index]])
                                # Increment index
                                index += 1
                            raise DatacoreException(
                                "post_error",
                                {"errors": errors}
                            )
                        logging.info("Packet upload successful")
                        break
                    elif response.status_code == 500:
                        # Something really bad happened.
                        body = json.loads(response.text)
                        if "err" in body.keys():
                            if "field" in body["message"][0]:
                                # User error, easy
                                raise DatacoreException(
                                    response.status_code,
                                    body
                                )
                        else:
                            # In staging, very common -- server-side out of disk space errors
                            logging.warning("Couldn't communicate with datacore.")
                            raise DatacoreException(
                                response.status_code,
                                "Datacore API service is likely down.\n Please try again at another time.\n"
                                + "If this issue persists, please contact EveryMundo to resolve the issue. Ref: \n"
                                + response.text
                            )
                    elif response.status_code == 413:
                        logging.info("Sub-post still too big: attempting recursive subpost")
                        logging.info("Do not worry unless this message appears for several pages,")
                        logging.info("consecutively, without end.")
                        logging.info("-" * 75)
                        self._sub_post(url, part)
                        part = None
                        break
                    elif response.status_code == 502:
                        if j == 4:
                            logging.warning("Couldn't communicate with datacore.")
                            raise DatacoreException(
                                response.status_code,
                                "Couldn't establish a connection. Please check connection and try again." \
                                + response.text
                            )
                        logging.info("Bad Gateway... Possible internet connection issues... will try again shortly.")
                        j += 1
                    elif response.status_code >= 500:
                        if j == 4:
                            logging.warning("Couldn't communicate with datacore.")
                            raise DatacoreException(
                                response.status_code,
                                "Datacore API service is likely down. Please try again at another time." + response.text
                            )
                        else:
                            logging.info("Server issues... Retrying shortly...")
                            j += 1
                    else:
                        logging.info("Packet post error")
                        logging.info("Status: " + str(response.status_code))
                        logging.info(response.text)
                        raise (DatacoreException(response.status_code, response.text))
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ConnectionError:
                    # Just try again lolol
                    pass
                time.sleep(2 ** j + random.random())
        data_set = None

    def old_data(self, url: AnyStr, date_to_check: datetime.date, date_field_name: AnyStr, rules=None)\
            -> Payload:
        """

        :param url: datacore read endpoint to check
        :param date_to_check: date to pull data from
        :param date_field_name: name of date field for the table with endpoint url
        :param rules: other rules to put in place
        :type rules: dict
        :type url: str
        :type date_to_check: datetime.date
        :type date_field_name: str
        :return old_data: list whose rows are dict {col_name: value, }
        :rtype: list
        """
        query = rules if rules else {}
        query[date_field_name] = {
            "$date": date_to_check.isoformat()
        }
        old_data = self.get(
            url,
            query=query,
            limit=250
        )
        if old_data:
            return old_data
        else:
            return []

    @staticmethod
    def chunk(data: Payload, chunk_size=500) -> Sequence[Payload]:
        """
        Breaks a collection of rows intended for bulk posting into 'chunks' of len chunk_size (or less). The upload
        size limitations of datacore lead to the necesity of using a method like this in posting batches of length
        greather than 1000, or of sufficiently large size (in bytes).

        Since this is a helper method, it does not check for invalid inputs.

        :param data: data to be uploaded
        :type data: list(dict)
        :param chunk_size: maximum length of each batch desired
        :type chunk_size: int
        :return chunks: the pieced-out partition of data
        :rtype: list(list(dict))
        """
        data = data
        # The number of chunks
        n = len(data) // chunk_size
        # Usual case: len(data) is not integer divisible by chunk_size
        if len(data) % chunk_size > 0:
            # Produce an extra chunk, will have (len(data) % chunk_size) rows in it.
            chunks = [data[i * chunk_size:(i * chunk_size) + chunk_size] for i in range(n + 1)]
        else:
            # Produce exactly as many chunks of exactly chunk_size length
            chunks = [data[i * chunk_size:(i * chunk_size) + chunk_size] for i in range(n)]
        return chunks
