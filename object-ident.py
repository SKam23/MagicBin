import cv2
import os
import time
from arduino import comm_arduino

#thres = 0.45 # Threshold to detect object

classNames = []
ROOT_DIR = os.getcwd()
classFile = os.path.join(ROOT_DIR,"coco.names")
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

config = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weight = "frozen_inference_graph.pb"
configPath = os.path.join(ROOT_DIR,'mobilenet.pbtxt')
weightsPath = os.path.join(ROOT_DIR,'mobilenet.pb')

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

delay = 10


def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)
    lastDetected = time.time()
     
    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.65,0.2, objects=['bottle'])
        #print(objectInfo)
        if len(objectInfo) > 0:   
            print(objectInfo[0][1])
            objectName = objectInfo[0][1]
            currTime = time.time()
            if objectName == "bottle" and currTime - lastDetected > delay:
                comm_arduino('A')
                lastDetected = currTime
        cv2.imshow("Output",img)
        cv2.waitKey(1)
