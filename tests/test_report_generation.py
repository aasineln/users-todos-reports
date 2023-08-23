import unittest
from unittest.mock import MagicMock, patch
from app.report_generator import ReportClient
from app.schemas import User
from main import main
from tests.fixtures import RESPONSE_USERS_200, RESPONSE_TODOS_200


class TestReportGeneration(unittest.TestCase):
    @patch('api.service.MedrocketClient')
    def test_report_generation(self, mock_api_client):
        mock_get_users = MagicMock(return_value=RESPONSE_USERS_200)
        mock_get_todos = MagicMock(return_value=RESPONSE_TODOS_200)
        mock_api_client.return_value.get_users = mock_get_users
        mock_api_client.return_value.get_todos = mock_get_todos

        mock_report_client = MagicMock(spec=ReportClient)
        mock_report_client.prepare_user_todos_data.return_value = {
            1: {'username': 'Bret', 'company': 'Romaguera', 'email': 'Sincere@april.biz',
                'todos': {'completed': ['et porro tempora'], 'active': ['et porro tempora']}
                }
        }

        with patch('app.report_generator.ReportClient', return_value=mock_report_client):
            main()


if __name__ == '__main__':
    unittest.main()
