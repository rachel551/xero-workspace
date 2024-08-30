import requests
import os
import pytest
import sys
from unittest.mock import patch, MagicMock

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from services.balance_sheet_service import BalanceSheetService


@patch('services.balance_sheet_service.requests.get')
@patch('services.balance_sheet_service.os.getenv')
def test_get_balance_sheet_data_success(mock_getenv, mock_get):
    mock_getenv.return_value = 'http://fakeurl.com/api.xro/2.0/Reports/BalanceSheet'

    # Mock the response of requests.get
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {'status': 'success'}
    mock_get.return_value = mock_response

    service = BalanceSheetService()
    result = service.get_balance_sheet_data()

    assert result == {'status': 'success'}
    mock_get.assert_called_once_with('http://fakeurl.com/api.xro/2.0/Reports/BalanceSheet')
    mock_response.raise_for_status.assert_called_once()


@patch('services.balance_sheet_service.requests.get')
@patch('services.balance_sheet_service.os.getenv')
def test_get_balance_sheet_data_failure(mock_getenv, mock_get):
    mock_getenv.return_value = 'http://fakeurl.com/api.xro/2.0/Reports/BalanceSheet'
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    service = BalanceSheetService()
    with pytest.raises(Exception) as excinfo:
        service.get_balance_sheet_data()

    assert 'Failed to fetch balance sheet data: Network error' in str(excinfo.value)
    mock_get.assert_called_once_with('http://fakeurl.com/api.xro/2.0/Reports/BalanceSheet')