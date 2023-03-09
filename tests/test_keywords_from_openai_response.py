import logging
from typing import List
import pytest
from app import keywords_from_openai_response

def test_keywords_from_openai_response():
    # Test case 1: Valid response
    response = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "logprobs": None,
                "text": "\nanswers: Apache Arrow, Neo4j, Graph Projections, Cloud Object Storage, Cloud Data Warehouses, Neo4j Graph Data Science Python Client, Parallelize in Python"
            }
        ],
        "created": 1677274110,
        "id": "cmpl-6nZuAgu4xaX324HJTuf1A2StIvD00",
        "model": "text-davinci-003",
        "object": "text_completion",
        "usage": {
            "completion_tokens": 47,
            "prompt_tokens": 178,
            "total_tokens": 225
        }
    }
    expected_output = [
        "Apache Arrow",
        "Neo4j",
        "Graph Projections",
        "Cloud Object Storage",
        "Cloud Data Warehouses",
        "Neo4j Graph Data Science Python Client",
        "Parallelize in Python"
    ]
    assert keywords_from_openai_response(response) == expected_output

    # Test case 2: Response missing 'choices' key
    response = {
        "created": 1677274110,
        "id": "cmpl-6nZuAgu4xaX324HJTuf1A2StIvD00",
        "model": "text-davinci-003",
        "object": "text_completion",
        "usage": {
            "completion_tokens": 47,
            "prompt_tokens": 178,
            "total_tokens": 225
        }
    }
    assert keywords_from_openai_response(response) is None

    # Test case 3: Response with empty 'choices' list
    response = {
        "choices": [],
        "created": 1677274110,
        "id": "cmpl-6nZuAgu4xaX324HJTuf1A2StIvD00",
        "model": "text-davinci-003",
        "object": "text_completion",
        "usage": {
            "completion_tokens": 47,
            "prompt_tokens": 178,
            "total_tokens": 225
        }
    }
    assert keywords_from_openai_response(response) is None

    # Test case 4: Response missing 'choices.text' key
    response = {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "logprobs": None
            }
        ],
        "created": 1677274110,
        "id": "cmpl-6nZuAgu4xaX324HJTuf1A2StIvD00",
        "model": "text-davinci-003",
        "object": "text_completion",
        "usage": {
            "completion_tokens": 47,
            "prompt_tokens": 178,
            "total_tokens": 225
        }
    }
    assert keywords_from_openai_response(response) is None
