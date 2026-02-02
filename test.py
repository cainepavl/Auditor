import unittest
from unittest.mock import patch
import hashlib
from auditor import get_password_leaks_count, pwned_api_check

class TestCredentialAuditor(unittest.TestCase):

    def test_get_password_leaks_count_success(self):
        """Test parsing logic when a matching hash suffix is found."""
        # Mocking the API response object
        class MockResponse:
            text = "ABCDE:5\nFGHIJ:10\nKLMNO:15"
        
        count = get_password_leaks_count(MockResponse(), "FGHIJ")
        self.assertEqual(count, "10")

    def test_get_password_leaks_count_not_found(self):
        """Test parsing logic when no match exists in the API response."""
        class MockResponse:
            text = "ABCDE:5\nFGHIJ:10"
        
        count = get_password_leaks_count(MockResponse(), "ZZZZZ")
        self.assertEqual(count, 0)

    @patch('auditor.request_api_data')
    def test_pwned_api_check_integration(self, mock_request):
        """Test the end-to-end hashing and check logic using a mock API call."""
        # Setup mock to return a suffix that matches our test password 'password123'
        # SHA-1 of 'password123' starts with CBFDAC6008...
        # Suffix is C6008...
        test_password = 'password123'
        sha1hash = hashlib.sha1(test_password.encode('utf-8')).hexdigest().upper()
        suffix = sha1hash[5:]
        
        class MockResponse:
            text = f"{suffix}:420"
            status_code = 200

        mock_request.return_value = MockResponse()
        
        result = pwned_api_check(test_password)
        self.assertEqual(result, "420")
        # Verify only the first 5 chars were sent to the 'API'
        mock_request.assert_called_with(sha1hash[:5])

if __name__ == '__main__':
    unittest.main()
