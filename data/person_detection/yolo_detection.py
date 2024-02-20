import cv2
import numpy as np
from yoloface import face_analysis


face=face_analysis()        #  Auto Download a large weight files from Google Drive.
                            #  only first time.
                            #  Automatically  create folder .yoloface on cwd.
weights_path = './yolov3.weights'
cfg_path = './yolo3.cfg'
classes = ['person']
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))


# def get_output_layers(net):
    
#     layer_names = net.getLayerNames()
#     try:
#         output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
#     except:
#         output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

#     return output_layers


# def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

#     label = str(classes[class_id])

#     color = COLORS[class_id]

#     cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

#     cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    
# def detect_people(img_path):
#     image = cv2.imread(img_path)

#     Width = image.shape[1]
#     Height = image.shape[0]
#     scale = 0.00392

#     net = cv2.dnn.readNet(weights_path, cfg_path)

#     blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

#     net.setInput(blob)

#     outs = net.forward(get_output_layers(net))

#     class_ids = []
#     confidences = []
#     boxes = []
#     conf_threshold = 0.5
#     nms_threshold = 0.4


#     for out in outs:
#         for detection in out:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.5:
#                 center_x = int(detection[0] * Width)
#                 center_y = int(detection[1] * Height)
#                 w = int(detection[2] * Width)
#                 h = int(detection[3] * Height)
#                 x = center_x - w / 2
#                 y = center_y - h / 2
#                 class_ids.append(class_id)
#                 confidences.append(float(confidence))
#                 boxes.append([x, y, w, h])


#     indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

#     for i in indices:
#         try:
#             box = boxes[i]
#         except:
#             i = i[0]
#             box = boxes[i]
        
#         x = box[0]
#         y = box[1]
#         w = box[2]
#         h = box[3]
#         draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

#     return image, box, confidences[i]


def detect_faces_helper(img_path):
    # box = (x, y , h, w) where x, y are the coordinates of top right corner
    img, box, conf = face.face_detection(image_path=img_path,model='tiny')
    if len(box) == 0 or max(conf) < 0.8:
        return False, None, None, None
    
    return True, img, box, conf

def detect_faces(img_path):
    repeat = 3
    result = False, None, None, None

    for i in range(repeat):
        new_result = detect_faces_helper(img_path)
        if new_result[0]:
            if result[0] == False:
                result = new_result
            elif len(new_result[1] > len(result[1])):
                result = new_result

    return result
