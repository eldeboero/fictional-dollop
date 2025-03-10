import pyotp
import time
import json
import qrcode
import qrcode.image.svg
import urllib.parse
import uuid

class Person:
    def __init__(self, personName="", personId="", personKey=""):
        self.name = personName
        self.id = personId
        self.key = personKey


'''
Main Lambda handler
'''
def lambda_handler(event, context):
    if event['body']['operation'] == "verify":
        return {
            "statusCode": 200,
            "body": verify(event['body']['id'], event['body']['totp'])
        }
    elif event['body']['operation'] == "showQRCode":
        return {
            "statusCode": 200,
            "body": showQRCode(event['body']['id'])
        }

'''
Verify -- returns True or False
'''
def verify(userId: str, submittedTOTP: str) -> bool:
    person = getPersonById(userId)
    personTOTP = pyotp.TOTP(person.key)
    print(f'Expected TOTP: {personTOTP.now()}')
    print(f'User submitted TOTP: {submittedTOTP}')
    
    return personTOTP.verify(submittedTOTP)

'''
showQRCode - returns an html page with embedded QR code
'''

def showQRCode(userId: str) -> str:
    person = getPersonById(userId)
    safePersonName = urllib.parse.quote_plus(person.name)
    uri = "otpauth://totp/RealityCheck:" + safePersonName + "?secret=" + person.key + "&issuer=RealityCheck"
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(uri, image_factory=factory)
    html = "<html><head><title>Temporary QR code</title></head><body>" + img.to_string(encoding='unicode') + "</body></html>"
    return html

def getPersonById(userId: str) -> Person:

    '''
    This function needs to be replaced with something that uses a secure storage
    '''

    ben = Person("Ben DeBoer", "ben_id", "fakekey1")
    bob = Person("Bob Jones", "bob_id", "fakekey2")
    people = [ben, bob]

    for person in people:
        if person.id == userId:
            return person

def registerPerson(userName: str) -> str:
    ...
