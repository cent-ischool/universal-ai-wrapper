"""
Test script to verify API key authentication for dynamic endpoints.
Run the server first with: uvicorn app.server2:app --reload
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint_without_auth(endpoint: str):
    """Test endpoint without authentication - should fail with 401."""
    print(f"\n--- Testing {endpoint} without auth ---")
    response = requests.post(
        f"{BASE_URL}/{endpoint}/chat/completions",
        json={
            "messages": [
                {"role": "user", "content": "Hello!"}
            ],
            "stream": False
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 401


def test_endpoint_with_wrong_auth(endpoint: str):
    """Test endpoint with wrong API key - should fail with 401."""
    print(f"\n--- Testing {endpoint} with wrong API key ---")
    response = requests.post(
        f"{BASE_URL}/{endpoint}/chat/completions",
        headers={
            "Authorization": "Bearer wrong-api-key-12345"
        },
        json={
            "messages": [
                {"role": "user", "content": "Hello!"}
            ],
            "stream": False
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 401


def test_endpoint_with_correct_auth(endpoint: str, api_key: str):
    """Test endpoint with correct API key - should succeed with 200."""
    print(f"\n--- Testing {endpoint} with correct API key ---")
    response = requests.post(
        f"{BASE_URL}/{endpoint}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "messages": [
                {"role": "user", "content": "Say hello!"}
            ],
            "stream": False
        }
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.text[:100]}...")
    else:
        print(f"Response: {response.json()}")
    return response.status_code == 200


def list_configurations():
    """List all available configurations."""
    print("\n--- Listing all configurations ---")
    response = requests.get(f"{BASE_URL}/configurations")
    configs = response.json()
    print(json.dumps(configs, indent=2))
    return configs


if __name__ == "__main__":
    print("=" * 60)
    print("API Key Authentication Test")
    print("=" * 60)

    # List configurations
    configs = list_configurations()

    # Test with first configuration if available
    if configs["configurations"]:
        first_config = configs["configurations"][0]
        endpoint = first_config["name"]

        print(f"\nTesting endpoint: {endpoint}")
        print(f"Model: {first_config['model']}")
        print(f"Description: {first_config['description']}")

        # Test without auth (should fail)
        assert test_endpoint_without_auth(endpoint), "Should fail without auth"

        # Test with wrong auth (should fail)
        assert test_endpoint_with_wrong_auth(endpoint), "Should fail with wrong auth"

        # Test with correct auth (should succeed)
        # NOTE: You need to replace this with the actual API key from config.yaml
        print("\n⚠️  To test with correct auth, update the api_key in this script")
        print("   Get the key from app/config.yaml for the configuration you're testing")

        # Uncomment and add your API key to test:
        # api_key = "your-api-key-here"
        # assert test_endpoint_with_correct_auth(endpoint, api_key), "Should succeed with correct auth"

        print("\n" + "=" * 60)
        print("✅ Authentication tests completed!")
        print("=" * 60)
