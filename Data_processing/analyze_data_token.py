from utils import read_json_file
import matplotlib.pyplot as plt

from transformers import AutoModel, AutoTokenizer
from pyvi.ViTokenizer import tokenize

tokenizer = AutoTokenizer.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base") 

# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

dataset = read_json_file("data/data.json")
# print(dataset)

list_len = []

for data in dataset:
    sentence = tokenize(data['user'])
    print(sentence)
    list_len.append(len(tokenizer.tokenize(sentence)))


# data = list_len
data = list_len

xpoints = [i for i in range(len(data))]
ypoints = data
print(xpoints)
print(ypoints)
plt.bar(xpoints, ypoints)
addlabels(xpoints, ypoints)
plt.ylabel("Số lượng token")
plt.xlabel("Câu hỏi của user")

plt.show()

