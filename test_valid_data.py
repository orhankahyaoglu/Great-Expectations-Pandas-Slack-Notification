# slack_test.py
import requests
import json

def test_slack_webhook(webhook_url):
    """Test Slack webhook connection"""
    message = {
        "attachments": [
            {
                "color": "#36a64f",
                "title": "🧪 Test Notification",
                "text": "Great Expectations validation test successful!",
                "fields": [
                    {
                        "title": "Status",
                        "value": "TEST PASSED",
                        "short": True
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            print("✅ Slack webhook test: SUCCESS")
        else:
            print(f"❌ Slack webhook test: FAILED - {response.status_code}")
    except Exception as e:
        print(f"❌ Slack webhook test: ERROR - {e}")

# Test your webhook
WEBHOOK_URL = "https://hooks.slack.com/services/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"
test_slack_webhook(WEBHOOK_URL)