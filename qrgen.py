import os
import qrcode

def make_qr(uuidName):
    text= os.path.join(os.curdir, "download/" + uuidName.__str__())
    print text
    img=qrcode.make(text)
    qr_file = os.path.join(os.curdir, "static/uuidImages/" + uuidName.__str__() + ".jpg")
    img_file = open(qr_file, 'wb')
    img.save(img_file, 'JPEG')
    img_file.close()