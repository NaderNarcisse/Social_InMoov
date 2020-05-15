import cv2

name = input("who do you want to capture?")

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0



while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = ("people/"+name + ".png").format(img_counter)
        
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        f=open("people.txt", 'a+')
        f.write("\n")
        f.write(name +"//"+img_name+"// \n")
       
        f.close()
        break

cam.release()

cv2.destroyAllWindows()
