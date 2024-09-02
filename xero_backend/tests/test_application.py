import os
import pytest
import sys
from flask import Flask, jsonify
from unittest.mock import patch, MagicMock

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from application.app import XeroApp
from services.balance_sheet_service import BalanceSheetService


MOCK_URL = 'http://fakeurl.com/api.xro/2.0/Reports/BalanceSheet'

@pytest.fixture
def app():
    return XeroApp().app

@pytest.fixture
def client(app):
    return app.test_client()

@patch('services.balance_sheet_service.BalanceSheetService')
@patch('application.app.Config.load_config')
def test_get_balance_sheet_success(mock_load_config, mock_balance_sheet_service, client):
    mock_logger = MagicMock()
    mock_load_config.return_value = (mock_logger, '0.0.0.0', 5000, MOCK_URL)

    mock_balance_sheet_service_instance = MagicMock()
    mock_balance_sheet_service_instance.get_balance_sheet_data.return_value = {'Reports': [{'ReportID': '1', 'Status': 'OK'}]}
    mock_balance_sheet_service.return_value = mock_balance_sheet_service_instance

    response = client.get('/api/balance-sheet')

    assert response.status_code == 200
    assert response.json == {'status': 'success'}
    mock_balance_sheet_service_instance.get_balance_sheet_data.assert_called_once()


@patch('services.balance_sheet_service.BalanceSheetService')
@patch('application.app.Config.load_config')
def test_get_balance_sheet_failure(mock_load_config, mock_balance_sheet_service, client):
    mock_logger = MagicMock()
    mock_load_config.return_value = (mock_logger, '0.0.0.0', 5000, MOCK_URL)

    mock_balance_sheet_service_instance = MagicMock()
    mock_balance_sheet_service_instance.get_balance_sheet_data.side_effect = Exception("Service error")
    mock_balance_sheet_service.return_value = mock_balance_sheet_service_instance

    response = client.get('/api/balance-sheet')

    assert response.status_code == 500
    assert response.json == {"error": "Service error"}
    mock_balance_sheet_service_instance.get_balance_sheet_data.assert_called_once()