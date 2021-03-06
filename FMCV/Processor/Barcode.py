import cv2
import copy
import traceback

qr_detector = cv2.QRCodeDetector()

try:
    from pyzbar.pyzbar import decode
    from pylibdmtx.pylibdmtx import decode as dm_decode
except:
    traceback.print_exc()
    
def process_barcode(self, result, frm, src_n, step_n, roi_n):

    h,w = frm.shape[:2]
    roi = self.Main.results[src_n][step_n][roi_n]
    result = roi

    m = roi['margin']
    x1 = roi['x1'] - m
    y1 = roi['y1'] - m
    x2 = roi['x2'] + m
    y2 = roi['y2'] + m
    cropped = frm[y1:y2,x1:x2]
    
    result.update({"CODE":""})
    result.update({'result_image':copy.deepcopy(cropped)})
    
    is_pass = False
    if 'decode' in globals():
        detectedBarcodes = decode(cropped)
        if not detectedBarcodes:
            #result.update({"PASS":False})
            print("Barcode/QR Code Not Detected or your barcode is blank/corrupted!")
        else:
            # Traverse through all the detected barcodes in image
            for barcode in detectedBarcodes:
                if barcode.data != "":               
                # Print the barcode data
                    is_pass = True
                    result.update({"CODE":barcode.data.decode("utf-8")})
                    print(barcode.data)
                    print(barcode.type)                        
    else:
        res,points, rectifiedImg = qr_detector.detectAndDecode(cropped)   
        # Detected outputs.
        if len(res) > 0:            
            print('Output : ', res[0])
            print('Bounding Box : ', points)
            result.update({"PASS":True})
            result.update({"CODE":res[0]})
        else:
            result.update({"PASS":False})
            print('QRCode not detected')
    
    # Workable code, just slow
    
    if not is_pass:
        print("Checking 2d matrix")
        if 'dm_decode' in globals():
        
            #cropped = cv2.imread("123.png")
            #cv2.imshow('image', cropped)
            #cv2.waitKey(0)
            
            scale_percent = 30
            width = int(cropped.shape[1] * scale_percent / 100)
            height = int(cropped.shape[0] * scale_percent / 100)
            dsize = (width, height)
            
            resized = cv2.resize(cropped, dsize, interpolation = cv2.INTER_AREA)
            if len(resized.shape) ==3:
                resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            
            detectedBarcodes = dm_decode(resized,max_count=1,threshold=50)
            print(detectedBarcodes)
            if not detectedBarcodes:
                #result.update({"PASS":False})
                print("Datamatrix Not Detected or your barcode is blank/corrupted!")
            else:
                # Traverse through all the detected barcodes in image
                for barcode in detectedBarcodes:
                    if barcode.data != "":               
                    # Print the barcode data
                        is_pass = True
                        result.update({"CODE":barcode.data.decode("utf-8")})
                        print(barcode.data)
                        #print(barcode.type) 
                        
    result.update({"PASS":is_pass})
    
    return result