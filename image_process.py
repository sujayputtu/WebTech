from PIL import Image
import pytesseract
import re

lst = list()
lst_img = list()
lst=[(56, 156, 406, 177), #seller name 
     (446, 150, 768, 197), #customer name
     (50, 350, 340, 460),#order number, order date
     (444, 148, 772, 253)] #billing address
img = Image.open("invoice1.png")

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
          a.show()
     elif i == 2:
          x = re.split('\s', output)
          order_date = x[5]
          order_number = x[2]
     elif i == 3:
          billing_address= " "
          #x = re.split('\s', output)
          billing_address = output 
     
print("seller:", seller)
print("customer:", customer)
print("order_date:", order_date)
print("order_number:", order_number)
print("billing_address:", billing_address)

#print(lst2)