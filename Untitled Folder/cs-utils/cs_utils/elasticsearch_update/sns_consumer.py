from cs_utils.service_locations import get_service_endpoint
from cs_utils import requests
from django.conf import settings
from requests_aws4auth import AWS4Auth
from college_profile.models import (OWNERSHIP, MODE_OF_STUDY,
                                    COURSE_LEVEL,
                                    COURSE_STATUS,
                                    COLLEGE_TYPE, UNIVERSITY_TYPE)
import logging
import uuid


def handle_college_update(event, context):
    logger = logging.getLogger(__name__)
    logger.info("event : %s , \n context: %s, \n "
                " message: initail college event logging",
                event, context
                )
    try:
        institution_info = event['Records'][0]['Sns']['Message']
        info_list = institution_info.split('|')
        institution_id = info_list[0]
        action_type = info_list[1]
        uuid.UUID(institution_id)
    except (TypeError, ValueError, KeyError, IndexError) as err:
        logger.error("Error: %s",
                     err, exc_info=True)
    else:
        end_point = '/_doc/{}'.format(institution_id)
        BASE_ELASTIC_URL = get_service_endpoint('cs-elasticsearch')
        aws_url = BASE_ELASTIC_URL + end_point
        ELASTIC_UPDATE_AUTH = settings.ELASTIC_UPDATE_AUTH
        awsauth = AWS4Auth(ELASTIC_UPDATE_AUTH['AWS_ACCESS_KEY'],
                           ELASTIC_UPDATE_AUTH['AWS_SECRET_KEY'],
                           ELASTIC_UPDATE_AUTH['region'],
                           ELASTIC_UPDATE_AUTH['service'])
        BASE_URL = get_service_endpoint('cs-college-profile')
        url = BASE_URL + '/api/institution/{}/'.format(institution_id)
        if action_type == 'deleted':
            requests.delete(aws_url, auth=awsauth)
            logger.info("college id: %s , \n"
                        "message: elastic search data deleted",
                        institution_id,
                        )
        else:
            r = requests.get(url)
            if r.status_code == 200:
                institution = r.json()
                payload = {
                    "name": institution.get("name"),
                    "slug": institution.get("slug_name"),
                    "type": 'university'
                    if 'university_type' in institution.keys()
                    else 'college',
                    "url": institution.get("url"),
                    "rating": institution.get("rating"),
                    "override_rating": institution.get("override_rating"),
                    "total_rating_count": institution.get(
                        "total_rating_count"),
                    "ownership": dict(OWNERSHIP)[institution.get('ownership')]
                    if institution.get('ownership', None) else None,
                    "description": institution.get('description'),
                    "univ_type": dict(UNIVERSITY_TYPE)
                    [institution.get('university_type')]
                    if institution.get('university_type', None) else None,
                    "college_type": dict(COLLEGE_TYPE)
                    [institution.get('college_type')]
                    if institution.get('college_type', None) else None,
                    "accreditations": [
                        {
                            "accreditation_body_name": acc.get(
                                'accreditation_name'),
                            "accreditation_body_abbrv": acc.get(
                                'abbreviation'),
                            "score": acc.get('score')
                        }
                        for acc in institution.get('accreditation')
                    ],
                    "contacts": [
                        {
                            "contact_no": contact.get('contact_no'),
                            "alternate_contact_no": contact.get(
                                "alternate_contact_no"),
                            "name": contact.get('name'),
                            "email": contact.get('email'),
                            "alternate_email": contact.get('alternate_email'),
                        }
                        for contact in institution.get('contacts')],
                    "courses": [
                        {
                            "cat": course.get('grand_parent_name'),
                            "sub_cat": course.get('parent_name'),
                            "programme": course.get('name'),
                            "num_seats_intake": course.get('course_intake'),
                            "num_seats_enrolled": course.get(
                                'course_enrolled'),
                            "override_rating": course.get('override_rating'),
                            "mode_of_study": dict(MODE_OF_STUDY)
                            [course.get('mode_of_study')],
                            "course_level": dict(COURSE_LEVEL)
                            [course.get('course_level')],
                            "course_status": dict(COURSE_STATUS)
                            [course.get('course_status')]
                        }
                        for course in institution.get('courses')],
                    "addresses": [
                        {
                            "street": address.get('street'),
                            "city": address.get('city'),
                            "district": address.get('district'),
                            "state": address.get('state'),
                            "location": '{}, {}'.format(
                                address.get('latitude') if address.get(
                                    'latitude')
                                else 0.0,
                                address.get('longitude')
                                if address.get('longitude')
                                else 0.0)
                        }
                        for address in institution.get('addresses')
                    ],
                    "facilities": [
                        {
                            "infra_type": infra.get('infra_type'),
                            "infra_count": infra.get('infra_entity_count')
                        }
                        for infra in institution.get('infrastructure')
                    ],
                    "images": [
                        {
                            "description": image.get('description'),
                            "media_label": image.get('media_label'),
                            "media_type": image.get('media_type'),
                            "url": image.get('url'),
                        }
                        for image in institution.get('images')
                        if image.get('media_label') in {3, 5}
                        # 3 : srp image, 5: Brochure
                    ]
                }
                requests.put(aws_url, auth=awsauth, json=payload)
                logger.info("college id: %s , \n"
                            "message: elastic search updated successfully",
                            institution_id,
                            )
            else:
                logger.error("request failed and cant do the update")
