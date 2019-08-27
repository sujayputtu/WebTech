from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Resource, Api
from PIL import Image
import pytesseract

class linking:
    def run(self,address):
        #filename1= address[36:]
        output=(pytesseract.image_to_string(Image.open("images/"+address)))
        return output
    