import nacl.utils
from nacl.public import PrivateKey, Box

import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(event)
    }


testValidationPayload = {
    "operation":"validate",
    "totp":"12345"
    }

testEvent = {
    "body": testValidationPayload
}

testContext = {
    "functionName":"Test Function"
}

print(lambda_handler(testEvent, testContext))
