import logging
import os
import requests
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from utilities.logger_setup import LoggerSetup

log_setup = LoggerSetup(log_file='balance_sheet', log_dir='logs/service', log_level=logging.INFO)
logger = log_setup.get_logger()


class BalanceSheetService:
    def __init__(self, base_url):
        self.base_url = base_url
        
    def get_balance_sheet_data(self):
        try:
            logger.info(f'Fetching balance sheet data from {self.base_url}')
            response = requests.get(self.base_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Failed to fetch balance sheet data: {e}")
        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error occurred.")
            raise Exception(f"Failed to connect to Xero API: {e}")
        except requests.exceptions.Timeout as e:
            logger.error("Timeout occurred.")
            raise Exception(f"Request to Xero API timed out: {e}")
        except requests.exceptions.RequestException as e:
            logger.error("Error occurred while making request to Xero API.")
            raise Exception(f"An error occurred while fetching balance sheet data: {e}")
