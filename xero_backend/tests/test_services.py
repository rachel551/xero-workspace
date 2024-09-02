import requests
import os
import pytest
import sys
from unittest.mock import patch, MagicMock

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from services.balance_sheet_service import BalanceSheetService
from application.app import Config 

MOCK_URL = 'http://fakeurl.com/api.xro/2.0/Reports/BalanceSheet'

@patch('services.balance_sheet_service.requests.get')
@patch('application.app.Config.load_config')
def test_get_balance_sheet_data_success(mock_load_config, mock_get):
    mock_logger = MagicMock()
    mock_load_config.return_value = (mock_logger, 'localhost', 5000, MOCK_URL)
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {'status': 'success'}
    mock_get.return_value = mock_response

    service = BalanceSheetService(base_url=MOCK_URL)  # Pass the mock URL directly
    result = service.get_balance_sheet_data()

    assert result == {'status': 'success'}
    mock_get.assert_called_once_with(MOCK_URL)
    mock_response.raise_for_status.assert_called_once()


@patch('services.balance_sheet_service.requests.get')
@patch('application.app.Config.load_config')
def test_get_balance_sheet_data_failure(mock_load_config, mock_get):
    mock_logger = MagicMock()
    mock_load_config.return_value = (mock_logger, 'localhost', 5000, MOCK_URL)

    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    service = BalanceSheetService(base_url=MOCK_URL)
    with pytest.raises(Exception) as excinfo:
        service.get_balance_sheet_data()

    assert 'An error occurred while fetching balance sheet data: Network error' in str(excinfo.value)
    mock_get.assert_called_once_with(MOCK_URL)