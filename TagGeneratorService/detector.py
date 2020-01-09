import io
import torch
import torchvision.transforms as transforms
from PIL import Image

class Detector:
    def __init__(self, model, label_map, threshold= 0.5):
        self.label_map = label_map
        self.threshold = threshold
        self.model = model
        self.use_cuda = torch.cuda.is_available()
        if self.use_cuda:
            self.model = self.model.cuda()
        self.model.eval()
        self.transforms = transforms.Compose([transforms.Resize(150), transforms.ToTensor()])

    def produce_tag(self, image_bytes):
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        #TODO: handeling the case where image is invalid
        img = self.transforms(img).unsqueeze(0)
        if self.use_cuda:
            img = img.cuda()
        with torch.no_grad():
            result = self.model(img)
        labels = result[0]['labels'].cpu().numpy()
        scores = result[0]['scores'].cpu().numpy()
        tags = set()
        for i in range(len(scores)):
            if scores[i] >= self.threshold:
                tags.add(self.label_map[str(labels[i])])
        return tags

