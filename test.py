"""Tests for CredExpoAud.py — covers API parsing, hashing, k-Anonymity, and main flow."""

import hashlib
import unittest
from unittest.mock import patch

import CredExpoAud


# ── helpers ───────────────────────────────────────────────────────────────────

class MockResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code


def _mock_response_for(password):
    """Build a MockResponse whose text contains the correct suffix for `password`."""
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return MockResponse(f"{sha1[5:]}:42"), sha1


# ── get_password_leaks_count ──────────────────────────────────────────────────

class TestGetPasswordLeaksCount(unittest.TestCase):

    def test_match_found_returns_count(self):
        r = MockResponse("ABCDE:5\nFGHIJ:10\nKLMNO:15")
        self.assertEqual(CredExpoAud.get_password_leaks_count(r, "FGHIJ"), "10")

    def test_no_match_returns_zero(self):
        r = MockResponse("ABCDE:5\nFGHIJ:10")
        self.assertEqual(CredExpoAud.get_password_leaks_count(r, "ZZZZZ"), 0)

    def test_first_entry_matches(self):
        r = MockResponse("AAAAA:99\nBBBBB:1")
        self.assertEqual(CredExpoAud.get_password_leaks_count(r, "AAAAA"), "99")

    def test_last_entry_matches(self):
        r = MockResponse("AAAAA:1\nBBBBB:2\nCCCCC:50")
        self.assertEqual(CredExpoAud.get_password_leaks_count(r, "CCCCC"), "50")

    def test_empty_response_returns_zero(self):
        r = MockResponse("")
        self.assertEqual(CredExpoAud.get_password_leaks_count(r, "AAAAA"), 0)

    def test_match_is_case_sensitive(self):
        # Hash suffixes from the HIBP API are always uppercase — lowercase must not match
        r = MockResponse("ABCDE:5")
        self.assertEqual(CredExpoAud.get_password_leaks_count(r, "abcde"), 0)


# ── request_api_data ──────────────────────────────────────────────────────────

class TestRequestApiData(unittest.TestCase):

    @patch("CredExpoAud.requests.get")
    def test_successful_request_returns_response(self, mock_get):
        mock_get.return_value = MockResponse("AAAAA:1", status_code=200)
        result = CredExpoAud.request_api_data("CBFDA")
        self.assertEqual(result.status_code, 200)
        mock_get.assert_called_once_with(
            "https://api.pwnedpasswords.com/range/CBFDA", timeout=10
        )

    @patch("CredExpoAud.requests.get")
    def test_non_200_raises_runtime_error(self, mock_get):
        mock_get.return_value = MockResponse("", status_code=503)
        with self.assertRaises(RuntimeError) as ctx:
            CredExpoAud.request_api_data("CBFDA")
        self.assertIn("503", str(ctx.exception))

    @patch("CredExpoAud.requests.get")
    def test_404_raises_runtime_error(self, mock_get):
        mock_get.return_value = MockResponse("", status_code=404)
        with self.assertRaises(RuntimeError):
            CredExpoAud.request_api_data("XXXXX")


# ── pwned_api_check ───────────────────────────────────────────────────────────

class TestPwnedApiCheck(unittest.TestCase):

    @patch("CredExpoAud.request_api_data")
    def test_pwned_password_returns_count(self, mock_request):
        mock_response, _ = _mock_response_for("password123")
        mock_request.return_value = mock_response
        self.assertEqual(CredExpoAud.pwned_api_check("password123"), "42")

    @patch("CredExpoAud.request_api_data")
    def test_clean_password_returns_zero(self, mock_request):
        # Response contains no suffix that matches our password
        mock_request.return_value = MockResponse("AAAAA:1\nBBBBB:2")
        self.assertEqual(CredExpoAud.pwned_api_check("unique_password_xyz_123"), 0)

    @patch("CredExpoAud.request_api_data")
    def test_only_prefix_sent_to_api(self, mock_request):
        # k-Anonymity guarantee: only the first 5 chars of the SHA-1 hash are transmitted
        mock_request.return_value = MockResponse("AAAAA:1")
        CredExpoAud.pwned_api_check("testpassword")
        expected_prefix = hashlib.sha1("testpassword".encode()).hexdigest().upper()[:5]
        mock_request.assert_called_once_with(expected_prefix)

    @patch("CredExpoAud.request_api_data")
    def test_hash_prefix_is_uppercase(self, mock_request):
        # HIBP requires uppercase hex — confirm the prefix is always uppercase
        mock_request.return_value = MockResponse("AAAAA:1")
        CredExpoAud.pwned_api_check("test")
        call_arg = mock_request.call_args[0][0]
        self.assertEqual(call_arg, call_arg.upper())

    @patch("CredExpoAud.request_api_data")
    def test_prefix_is_exactly_5_chars(self, mock_request):
        # Only 5 characters must ever leave the local environment
        mock_request.return_value = MockResponse("AAAAA:1")
        CredExpoAud.pwned_api_check("test")
        call_arg = mock_request.call_args[0][0]
        self.assertEqual(len(call_arg), 5)


# ── main ──────────────────────────────────────────────────────────────────────

class TestMain(unittest.TestCase):

    @patch("CredExpoAud.clear_screen")
    @patch("CredExpoAud.getpass.getpass", return_value="")
    def test_empty_input_returns_none(self, mock_getpass, mock_clear):
        # Empty input should abort early; sys.exit(None) = clean exit code 0
        self.assertIsNone(CredExpoAud.main())

    @patch("CredExpoAud.clear_screen")
    @patch("CredExpoAud.pwned_api_check", return_value="1337")
    @patch("CredExpoAud.getpass.getpass", return_value="compromised")
    def test_pwned_password_returns_zero(self, mock_getpass, mock_check, mock_clear):
        self.assertEqual(CredExpoAud.main(), 0)

    @patch("CredExpoAud.clear_screen")
    @patch("CredExpoAud.pwned_api_check", return_value=0)
    @patch("CredExpoAud.getpass.getpass", return_value="safe_password")
    def test_clean_password_returns_zero(self, mock_getpass, mock_check, mock_clear):
        self.assertEqual(CredExpoAud.main(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
