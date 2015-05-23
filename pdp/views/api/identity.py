# identity apis

import logging
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseBadRequest
import json
from restclients.exceptions import DataFailureException, IRWSPersonNotFound
from restclients.irws import IRWS
from pdp.views.rest_dispatch import RESTDispatch
from pdp.util import Util

logger = logging.getLogger(__name__)

# get/set publish flag


class Publish(RESTDispatch):

    def GET(self, request):
        logger.info("identity/publish api for " + request.user.username)
        netid = Util.netid_from_remote_user(request.user.username)
        try:
            person = IRWS().get_hepps_person_by_netid(netid)
            response = HttpResponse(
                self._person_object_to_json(person),
                content_type='application/json')
        except IRWSPersonNotFound as ipnf:
            response = HttpResponseNotFound()
        except DataFailureException as dfe:
            logger.info(str(dfe))
            raise dfe
        return response

    def PUT(self, request):
        logger.info('identity/publish api put for' + request.user.username)
        netid = Util.netid_from_remote_user(request.user.username)

        irws = IRWS()
        try:
            # success or exception
            irws.post_hepps_person_by_netid(
                netid,
                self._json_to_irws_json(request.body))
            response = HttpResponse(json.dumps({'message': 'successful put'}),
                                    content_type='application_json',
                                    status=200)
        except DataFailureException as dfe:
            logger.info(str(dfe))
            raise dfe
        except IRWSPersonNotFound as ipnf:
            logger.info('attempted to post for non-hepps person ' + netid)
            response = HttpResponseNotFound()
        except Exception as e:
            logger.info('exception {} occurred: {}'.format(
                type(e).__name__, str(e)))
            response = HttpResponseBadRequest()

        return response

    def _person_object_to_json(self, person):
        return json.dumps({'publish': person.wp_publish})

    def _json_to_irws_json(self, data):
        try:
            person = json.loads(data)
            irws_json = json.dumps({'wp_publish': person['publish']})
        except:
            raise ValueError('bad json from browser')
        return irws_json
