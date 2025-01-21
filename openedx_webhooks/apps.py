import logging

from django.apps import AppConfig

learning_signals = [
    "STUDENT_REGISTRATION_COMPLETED",
    "SESSION_LOGIN_COMPLETED",
    "COURSE_ENROLLMENT_CREATED",
    "COURSE_ENROLLMENT_CHANGED",
    "COURSE_UNENROLLMENT_COMPLETED",
    "CERTIFICATE_CREATED",
    "CERTIFICATE_CHANGED",
    "CERTIFICATE_REVOKED",
    "COHORT_MEMBERSHIP_CHANGED",
    "COURSE_DISCUSSIONS_CHANGED",
]

content_authoring_signals = [
    "COURSE_CREATED",
]

logger = logging.getLogger(__name__)


class WebhooksConfig(AppConfig):
    """
    Configuration for the webhooks Django application.
    """

    name = 'openedx_webhooks'

    plugin_app = {
        "settings_config": {
            "lms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
            },
            "cms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
            },
        },
        "signals_config": {
            "lms.djangoapp": {
                "relative_path": "receivers",
                "receivers": [
                    {
                        "receiver_func_name": signal.lower() + "_receiver",
                        "signal_path": "openedx_events.learning.signals." + signal,
                    } for signal in learning_signals
                ] + [
                    {
                        "receiver_func_name": signal.lower() + "_receiver",
                        "signal_path": "openedx_events.content_authoring.signals." + signal,
                    } for signal in content_authoring_signals
                ],
            },
            "cms.djangoapp": {
                "relative_path": "receivers",
                "receivers":  [
                                 {
                                     "receiver_func_name": signal.lower() + "_receiver",
                                     "signal_path": "openedx_events.content_authoring.signals." + signal,
                                 } for signal in content_authoring_signals
                             ],

            }
        },
    }

    logger.info("Signals registered")
