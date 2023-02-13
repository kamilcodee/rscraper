import requests

from rscraper import RScraperConfig
from rscraper import util
from rscraper.RSLogger import RSLogLevel
from rscraper.RSLogger import RSLogger


class RScraper:
    """
    Reddit Scraper
    """

    def __init__(self, rsconfig: RScraperConfig):
        """
        :param rsconfig Config instance
        """

        self.rsconfig = rsconfig
        self.logger = RSLogger(self.rsconfig)

    def scrape_reddits(self, limit: int | None) -> None:
        """
        Scrape reddit data
        :param limit: amount of reddits fetched, can be None for all
        :raises ValueError if limit not None or type int
        :return: None
        """

        def _process_reddit(in_data: dict[str, str], keys: list[str]) -> dict[str, str]:
            """
            Parse reddit data
            :param in_data Input data of a reddit
            :param keys keys of interest, example: ['id', 'name']
            :return:
            """

            # TODO: process keys of interest
            return in_data

        # TODO: add metrics (time taken etc)

        if limit and not isinstance(limit, int):
            raise ValueError(f'Limit has to be an int or be None, got {limit} type {type(limit)}')

        component = 'Reddit Scraper'

        after = None
        finished = False

        # if limit is lower than max request limit in config use the lower value
        limit_per_request = self.rsconfig.reddits_per_request
        if limit and limit < self.rsconfig.reddits_per_request:
            limit_per_request = limit

        reddits_fetched = list()

        print()
        self.logger.log(RSLogLevel.INFO, 'Reddit Scraper', f'Scraping with limit = {limit_per_request}')

        while not finished:
            request_url = ''.join(
                [self.rsconfig.base_url, self.rsconfig.reddits_sub_url, '.json', f'?limit={limit_per_request}',
                 f'&after={after}' if after else ''])

            self.logger.log(RSLogLevel.INFO, component, f'Requesting {request_url}')

            req = requests.get(request_url, headers={'User-Agent': util.get_random_user_agent()})
            req_data = req.json().get('data')

            if not req_data:
                # TODO: handling on error/ etc
                pass

            after = req_data['after']
            if not after:
                finished = True

            for reddit in req_data['children']:
                reddits_fetched.append(_process_reddit(reddit, []))

                if limit and len(reddits_fetched) >= limit:
                    finished = True
                    break

            self.logger.log(RSLogLevel.INFO, component, f'Fetch count = {len(reddits_fetched)}')
