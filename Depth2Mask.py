import torch
import comfy.utils
def upscale(image, upscale_method, width,height):
    samples = image.movedim(-1,1)
    s = comfy.utils.common_upscale(samples, width, height, upscale_method, "disabled")
    s = s.movedim(1,-1)
    return (s,)

class Depth2Mask:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "image": ("IMAGE",),
 
                "image_depth":("IMAGE",),
            
            "depth": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001, #The value represeting the precision to round to, will be set to the step value by default. Can be set to False to disable rounding.
                    "display": "number"}),
                    },
                    
        }

    RETURN_TYPES = ("MASK",)
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "test"

    #OUTPUT_NODE = False

    CATEGORY = "Depth2Mask"

    def test(self, image,image_depth,depth):

        #do some processing on the image, in this example I just invert it
        bs = image.size()[0]
        width = image.size()[2]
        height = image.size()[1]  
        mask1 = torch.zeros((bs,height,width))

        # print(image_deep[0][512][512])
        # image_back = upscale(image_back, 'lanczos', width,height)[0]
        image_depth = upscale(image_depth, 'lanczos', width,height)[0]

        for k in range(bs):
             for i in range(width):
                 for j in range(height):
                     now_depth = image_depth[k][j][i][0].item()
                    #  if now_deep<shallow:
                        #  image_back[k][j][i]=image_front[k][j][i]
                        #  mask2[k][j][i]=1
                     if now_depth<depth:
                        #  image_back[k][j][i]=image_front[k][j][i]
                         mask1[k][j][i]=1
        return (mask1,)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {

    "Depth2Mask": Depth2Mask
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {

    "Depth2Mask":"Depth2Mask"
}
