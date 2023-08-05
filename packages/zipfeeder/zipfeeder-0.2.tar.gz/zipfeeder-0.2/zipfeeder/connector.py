from __future__ import absolute_import, division, print_function, unicode_literals
import re, json
import requests

class Connector(object):

    base_url = "http://zipfeeder.us/"
    v2_path = "api/v2/"

    def __init__(self, key):
        """ Initialize the class wit the key
        :param key: your zipfeeder key
        :return: None
        """
        self.key = key

    def _valid_zip(self, zip):
        """
        Ensures a zip is valid, wrapper for re.match
        :param zip: the zip code to test
        :return: match object on success, None on fail
        """
        return re.match(r'.*(\d{5}(\-\d{4})?)$', zip)

    def _make_request(self, path):
        """
        Makes a request to zipfeeder
        :param path: the zipfeder url to be requested
        :return: the json response
        """
        print("{}/{}".format(self.base_url, path))
        r = requests.get("{}/{}".format(self.base_url, path))

        if r.status_code == 401:
            raise Exception("You are not authorized to get this endpoint, is your key correct?")

        return json.loads(r.text)

    def zipcode(self, zip_code, full=None):
        """
        Gets basic and fullzip code data from zipfeeder
        :param zip_code: the zip code to request
        :param full: set to true to get the full zipcode data (premium only)
        :return: a dict representing the result
        """

        if not self._valid_zip(zip_code):
            raise ValueError("Please ensure you have submitted a valid zip code")

        path = ["{}/zipcode/{}?key={}".format(self.v2_path, zip_code, self.key)]
        if full:
            path.append("{}?full=1".format(path))

        return self._make_request("".join(path))

    def zipcodes(self, zip_codes):
        """
        Gets basic zipcode data from zipfeeder
        :param zip_codes: a list of zip codes to search on
        :return: a dict representing the result
        """

        if type(zip_codes) != list:
            raise ValueError("The zip_codes parameter must be a list")

        zips = [z for z in zip_codes if self._valid_zip(z)]

        if len(zips) == 0:
            raise ValueError("The strings in the zip_codes parameter must be zip codes")

        path = ["{}/zipcodes/{}?key={}".format(self.v2_path, ",".join(zips), self.key)]

        return self._make_request("".join(path))

    def nearby_zips(self, zip_code, radius=10):
        """
        Gets zipcodes near the specified @zip_code.
        :param zip_code: the zipcode to search on
        :param radius: the disatnce in miles to search on
        :return: a dict representing the result set
        """

        if not self._valid_zip(zip_code):
            raise ValueError("Please ensure youve entered a valid zip code")

        path = "{}/zipcodes/near/{}/?key={}&radius={}".format(self.v2_path, zip_code, self.key, radius)

        return self._make_request(path)

    def zipcodes_startwith(self, zip):
        """
        Looks for zipcodes that start with @zip
        :param zip: the zip string to search on
        :return: a dict
        """

        if not zip.isdigit():
            raise ValueError("zip parameter must be numeric")

        path = "{}/zipcodes/startswith/{}/?key={}".format(self.v2_path, zip, self.key)

        return self._make_request(path)

    def zipcodes_by_state(self, state, city_filter=None):
        """
        filters zipcodes based on state
        :param state: the 2 character state code
        :param city_filter: (optional) filter based on city string (starts with filter)
        :return:
        """

        path = ["{}/zipcodes/state/{}/?key={}".format(self.v2_path, state, self.key)]

        if city_filter:
            path.append("&q={}".format(city_filter))

        return self._make_request("".join(path))







