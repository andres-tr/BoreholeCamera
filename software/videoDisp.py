import cv2

vcap = cv2.VideoCapture("http://192.168.1.77/video.mjpg")
frame_width = int(vcap.get(3))
frame_height = int(vcap.get(4))
out = cv2.VideoWriter('outpyt.avi',cv2.cv.CV_FOURCC('M','P','4','2'), 30, (frame_width,frame_height))


while(True):

    ret, frame = vcap.read()
    out.write(frame)
    cv2.imshow('VIDEO', frame)
	
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
vcap.release()
out.release()
cv2.destroyAllWindows()




