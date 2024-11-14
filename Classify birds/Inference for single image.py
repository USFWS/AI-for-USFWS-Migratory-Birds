import torch
import PIL
from PIL import Image
from torchvision import transforms

# Inputs: source = jpg image to run through classification algorithm
# model_path = pytorch classification model saved as script file
# Optional (if new model is applied): idx_to_label = index to the corresponding label in the model
## transform_test = transform to be applied prior to inference

source = "C:/users/bpickens/Desktop/Crops/C1_L3_F1192_T20210828_120211_440_1012_1223_22_62.jpg"
model_path = 'F:/MODELS FOR USE/2024_Nov12_swin_s_augment_focal_scripted.pt'

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")  # must print "Using cuda device" to work

# load model
model = torch.jit.load(model_path)
model.to(device)

transform_test = transforms.Compose([
    transforms.Resize((224, 224)), transforms.ToTensor(),
    transforms.Normalize(mean=(0.2335, 0.2444, 0.2143), std=(0.1369, 0.1149, 0.1031))
])

idx_to_label = {0: "ABDU", 1: "ATPU", 2: "BCPE",
                3: "BLSC", 4: "BOGU", 5: "BRAN",
                6: "BRPE", 7: "BUFF", 8: "CANG", 9: "COEI",
                10: "COGO", 11: "COLO", 12: "DCCO",
                13: "GBBG_adult", 14: "GBBG_subadult",
                15: "GREG", 16: "HERG_adult",
                17: "HERG_subadult", 18: "HOGR",
                19: "LAGU_adult", 20: "LAGU_subadult", 21: "LTDU",
                22: "MALL", 23: "NOGA", 24: "not_wildlife",
                25: "RAZO", 26: "RBME", 27: "REDH",
                28: "ROYT", 29: "RTLO", 30: "SCAU", 31: "SNGO", 32: "SUSC",
                33: "TUSW", 34: "WWSC"
                }

species_list = list(idx_to_label.values())

def classify(model, transform_test, source):
    model = model.eval()
    image = PIL.Image.open(source)
    image = transform_test(image).float()
    image = image.to(device)
    image = image.unsqueeze(0)
    output = model(image)
    # print(output.data)
    softmax = torch.nn.functional.softmax(output, dim=1)

    top3_prob, top3_label = torch.topk(softmax, 3)
    # print("tops: ", top3_prob,top3_label)
    label1 = top3_label[0, 0]
    label2 = top3_label[0, 1]
    label3 = top3_label[0, 2]
    score1 = top3_prob[0, 0]
    score2 = top3_prob[0, 1]
    score3 = top3_prob[0, 2]
    label1 = label1.data.cpu().numpy()
    label2 = label2.data.cpu().numpy()
    label3 = label3.data.cpu().numpy()
    score1 = score1.data.cpu().numpy()
    score2 = score2.data.cpu().numpy()
    score3 = score3.data.cpu().numpy()
    species_list = list(idx_to_label.values())

    label1 = species_list[label1]
    label2 = species_list[label2]
    label3 = species_list[label3]
    print("Top 3 labels: ", label1,",", label2, ",", label3)
    print("Top 3 probabilities: ", score1, ",", score2, "," , score3)

classify(model, transform_test, source)

