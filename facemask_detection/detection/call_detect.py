from PIL import Image
import detect

source = 'D:/Thesis/upload/20211111_154356/dogddd.jpg'
target = 'D:/Thesis/upload/20211111_154356/'
detect.run(source=source,
           project=target,
           view_img=True,
           save_txt=False,
           conf_thres=0.5,
           weights='yolov5s.pt',
           nosave=False,
           imgsz=[640, 640],)




