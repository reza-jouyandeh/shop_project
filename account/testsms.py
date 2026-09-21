import os
import ghasedakpack

# The API key must NEVER be hardcoded in the source code.
# Set it as an environment variable before running this script:
#   export GHASEDAK_API_KEY="your-api-key-here"
sms = ghasedakpack.Ghasedak(os.environ.get("GHASEDAK_API_KEY"))

sms.verification({"receptor": os.environ.get("TEST_PHONE_NUMBER"), "type": "1", "template": "Ghasedak", "param1": "1234"})
