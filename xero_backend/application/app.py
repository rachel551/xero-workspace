import logging
import os
import requests
import sys
from flask import Flask, jsonify
from flask_cors import CORS

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from services.balance_sheet_service import BalanceSheetService
from utilities.logger_setup import LoggerSetup
from utilities.yaml_utils import load_env_from_yaml

class Config:
    @staticmethod
    def load_config():
        yaml_file_path = os.path.join(root_dir, 'config.yaml')
        load_env_from_yaml(yaml_file_path, 'backend')

        log_setup = LoggerSetup(log_file='application', log_dir='logs/app', log_level=logging.INFO)
        logger = log_setup.get_logger()

        host = os.getenv('flask_run_host')
        port = os.getenv('flask_run_port')
        environment = os.getenv('ENVIRONMENT', 'local')
        if environment == 'docker':
            xero_api_url = os.getenv('docker_balance_sheet_api_url')
        else:
            xero_api_url = os.getenv('local_balance_sheet_api_url')
        return logger, host, port, xero_api_url


class XeroApp:
    def __init__(self):
        self.logger, self.host, self.port, self.xero_api_url = Config.load_config()
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/api/*": {"origins": "*"}})
        self.balance_sheet_service = BalanceSheetService(self.xero_api_url)
        self.balance_sheet_data = None  
        self.fetch_balance_sheet_data() 
        self.register_routes()


    def fetch_balance_sheet_data(self):
        try:
            self.logger.info('Fetching balance sheet data from service.')
            self.balance_sheet_data = self.balance_sheet_service.get_balance_sheet_data()
        except Exception as e:
            self.logger.error(f"Error fetching balance sheet data: {e}")
            self.balance_sheet_data = {"error": str(e)}  # Store an error message if fetching fails


    def register_routes(self):
        @self.app.route('/api/balance-sheet', methods=['GET'])
        def get_balance_sheet():
            if self.balance_sheet_data:
                data = jsonify(self.balance_sheet_data)
                logging.info(data)
                return data
            else:
                return jsonify({"error": "No balance sheet data available"}), 500


    def run(self):
        self.app.run(host=self.host, port=self.port)

if __name__ == '__main__':
    app = XeroApp()
    app.run()