import FilterModel
import cv2

FM = FilterModel.FilterModule()

img_T =cv2.imread("inf.png")
img_F = cv2.imread("non-inf.png")

T_pred=FM.process_one(img_T)
F_pred=FM.process_one(img_F)

print("La imagen informativa ha sido clasificada como "+T_pred.__str__())
print("La imagen no informativa ha sido clasificada como "+F_pred.__str__())
