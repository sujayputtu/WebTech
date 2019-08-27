from PIL import Image
import pytesseract
import json
import os
import re
import queries

lst = list()

lst=[(56, 156, 406, 177), #seller name 
     (446, 150, 768, 197), #customer name
     (50, 350, 340, 460),#order number, order date
     (444, 148, 772, 253)] #billing address


class tess_ocr:
    def run_tesseract(self,filename):
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(APP_ROOT,'images/')    
        img = Image.open(target+filename)
        lst2=list()

        for i in range(4):
             a = img.crop(lst[i])
             output = pytesseract.image_to_string(a)
             #print(output)
             lst2.append(output)
             if i == 0:
                  seller = output
             elif i == 1:
                  x = re.split('\n', output)
                  customer = x[1]
             elif i == 2:
                  x = re.split('\s', output)
                  order_date = x[5]
                  order_number = x[2]
             elif i == 3:
                  x = re.split('\n', output)
                  del x[0]
                  billing_address= " "
                  for i in x:
                       billing_address+=i+" " 
                
        invoice_json={
            "retailer_name": seller, 
            "customer_name": customer,
            "order_date": order_date,
            "order_number": order_number,
            "billing_address": billing_address}      
          
        return invoice_json

   