import pyotp
import time
import json
import qrcode
import qrcode.image.svg
import urllib.parse
import uuid
import csv

class Person:
    def __init__(self, personName="", personId="", personKey=""):
        self.name = personName
        self.id = personId
        self.key = personKey

    def __repr__(self):
            return f"Person(name={self.name}, id={self.id}, key={self.key})"


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
    
    people = loadFromDisk()

    for person in people:
        if person.id == userId:
            return person

def registerPerson(userName: str) -> str:
    ...

def loadFromDisk() -> list[Person]:
    file_path = 'appData/people.csv'
    people = []
    with open(file_path, 'r') as file:
        for line in file:
            personArray = (line.strip()).split(',')
            #print(personArray)
            personRecord = Person(personArray[0],personArray[1],personArray[2])
            people.append(personRecord)
    return people

if __name__ == "__main__":
    ...
