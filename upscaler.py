import cv2
from cv2 import dnn_superres
import numpy as np

sr = dnn_superres.DnnSuperResImpl_create()
class Upscaler():
    def __init__(self, file_path, factor):
        
        model_path = "EDSR_Tensorflow-master\\models\\EDSR_x4.pb"  
        model_name = "edsr"      
        if factor == "2x":
            scale_factor = 2
        elif factor == "3x":
            scale_factor = 3
        elif factor == "4x":
            scale_factor = 4
        else:
            scale_factor = factor

        sr.readModel(model_path)

        sr.setModel(model_name, scale_factor)

        image_path = file_path
        image = cv2.imread(image_path)
        print("upscaling the image...")
        upscaled_image = sr.upsample(image)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened_image = cv2.filter2D(upscaled_image, -1, kernel)
        self.filtered_image2 = cv2.GaussianBlur(sharpened_image, (7, 7), 0)
        print("the upscaled image now exists")

    def download(self):
        cv2.imwrite("upscaled_image.png", self.filtered_image2)
        cv2.imshow("upscaled_image", self.filtered_image2)
        print("the upscaled image is now saved")
    def resolve(self, path):
        cv2.imwrite(path, self.filtered_image2)
        print("image has been saved")




