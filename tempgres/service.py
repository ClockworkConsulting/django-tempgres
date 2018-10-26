import logging
import requests

logger = logging.getLogger(__name__)

class TempgresDatabaseService:
    """Connection to a tempgres service instance defined by an URL."""

    def __init__(self, url, **kwargs):
        """Setup the Tempgress connection.

        url can be None, in which case kwargs must contain
        the database information as a dictionary.
        """
        self.url = url
        self.response = None
        self.data = kwargs

        # Do POST if we have an URL
        if self.url:
            if kwargs:
                logger.warning(
                    "Tempgres will use the database information "
                    "which has been supllied in kwargs!"
                    )
            self._post()

        # If we still do not have a response use kwargs as data
        if self.response is None:
            if not kwargs:
                raise ValueError("Data dictionary must be supplied")
        else:
            self._parse()

    def _post(self):
        """Get the response to the post request from the tempgress service."""
        self.response = requests.post(url=self.url)

        if not (self.response.status_code == requests.codes.ok):
            self.response.raise_for_status()

    def _parse(self):
        """Parse the response from a tempgres instance.

        Raises an error if the response does not conform.
        """

        if (self.response is None):
            raise ValueError("No response exsists!")

        parsed = self.response.text.splitlines()

        if not (len(parsed) == 5):
            raise TypeError("Response does not conform to expected format!")

        self.data['USER'] = parsed[0]
        self.data['PASSWORD'] = parsed[1]
        self.data['HOST'] = parsed[2]
        self.data['PORT'] = parsed[3]
        self.data['NAME'] = parsed[4]

    def __str__(self):
        a = []
        for k in self.data.keys():
            a.append("{}: {}".format(k, self.data[k]))
        return "\n".join(a)

    def setdefault(self, key, value):
        return self.data.setdefault(key, value)

    def __getitem__(self, value):
        return self.data[value]

    def __contains__(self, value):
        return value in self.data

    def get(self, key, value=None):
        return self.data.get(key, value)


# Main method for rudimentary testing
if __name__ == "__main__":
    print("Test run of TempgresDatabaseService")
    print("")

    db_info = {
        'USER': 'tempgres-client',
        'PASSWORD': 'tempgres-cpass',
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'temp_c23ff99a_ff56_4810_8692_7f779564b073'
    }

    tmpgres = None

    try:
        tmpgres = TempgresDatabaseService(None)
    except ValueError as e:
        logger.exception("Caugth exception with text: {}".format(e))

    try:
        # Should produce a warning (and fails because of the url)
        tmpgres = TempgresDatabaseService('localhost', **db_info)
    except requests.exceptions.MissingSchema:
        print("OK")
        print("")


    # Create a tempgres service with custom data
    tmpgres = TempgresDatabaseService(None, **db_info)

    for key in tmpgres.data.keys():
        print("{}: {}".format(key, tmpgres[key]))
