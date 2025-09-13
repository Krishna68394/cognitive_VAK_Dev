import os
from huggingface_hub import HfApi

# Load token from secrets
token = os.environ.get("HUGGINGFACE_API_TOKEN")

if token:
    print("✅ Token found in environment!")

    # Test API connection
    api = HfApi(token=token)
    user = api.whoami()
    print("👤 Logged in as:", user["name"])
else:
    print(
        "❌ No token found. Please set HUGGINGFACE_API_TOKEN in Replit secrets."
    )
