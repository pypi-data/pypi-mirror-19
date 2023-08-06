import requests
from ClientLogger import ClientLogger


# TODO: add retry logic and automatically increase timeout on retries see:https://pypi.python.org/pypi/retrying
class LoggedRequest(object):

    @staticmethod
    def get(url, params=None, **kwargs):
        logger = ClientLogger.setup()

        try:
            response = requests.get(url, params, **kwargs)
            response.raise_for_status()
        except Exception as e:
            logger.debug('API request failed\n\turl: %s\n\tparams: %s\n\tkwargs: %s.', url, params, kwargs)
            logger.exception(e)
            raise e

        return response
