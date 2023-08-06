import json
import logging
from restclients.dao import IASYSTEM_DAO
from restclients.exceptions import DataFailureException
from restclients.util.timer import Timer
from restclients.util.log import log_info


logger = logging.getLogger(__name__)
CAMPUS_SUBDOMAIN = {'seattle': 'uw',
                    'tacoma': 'uwt',
                    'bothell': 'uwb'}


def get_resource_by_campus(url, campus):
    return get_resource(url, CAMPUS_SUBDOMAIN[campus])


def get_resource(url, subdomain):
    """
    Issue a GET request to IASystem with the given url
    and return a response in Collection+json format.
    :returns: http response with content in json
    """
    headers = {"Accept": "application/vnd.collection+json"}
    timer = Timer()
    response = IASYSTEM_DAO().getURL(url, headers, subdomain)

    log_info(logger,
             "%s ==status==> %s" % (url, response.status),
             timer)

    if response.status != 200:
        logger.debug("%s ==data==> %s" % (url,
                                          response.data))
        raise DataFailureException(url, response.status, response.data)

    return json.loads(response.data)
