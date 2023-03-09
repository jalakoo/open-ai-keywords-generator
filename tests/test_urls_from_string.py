import pytest
from app import urls_from_string

def test_urls_from_string():
    # Test a string with one URL
    text = "Visit my website at https://www.example.com for more information."
    expected = ["https://www.example.com"]
    assert urls_from_string(text) == expected

    # Test a string with multiple URLs
    text = "Visit my websites at https://www.example.com and http://www.anotherexample.com for more information."
    expected = ["https://www.example.com", "http://www.anotherexample.com"]
    assert urls_from_string(text) == expected

    # Test a string with no URLs
    text = "This string does not contain any URLs."
    expected = []
    assert urls_from_string(text) == expected

    # Test a string with URLs separated by whitespace
    text = "Visit my website at https://www.example.com or http://www.anotherexample.com for more information."
    expected = ["https://www.example.com", "http://www.anotherexample.com"]
    assert urls_from_string(text) == expected

    # Test a string with URLs followed by punctuation
    text = "Visit my website at https://www.example.com! It's a great site."
    expected = ["https://www.example.com"]
    assert urls_from_string(text) == expected
