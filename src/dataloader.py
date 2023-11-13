import os
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

class Kaggle50K(Dataset):
    def __init__(self, root_dir: str, valid_countries: [str] = None,transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.valid_countries = valid_countries
        self.remove_false_sizes()
        self.image_paths, self.labels = self.load_image_paths_and_labels()
        self.labels_to_idx = {label: idx for idx, label in enumerate(set(self.labels))}

    # remove images that have the wrong size
    def remove_false_sizes(self):
        # iterate over all filenames in the wrong resolution files
        with open(os.path.join(self.root_dir, "wrong_resolution_files.txt"), "r") as f:
            for line in f:
                os.remove(os.path.join(self.root_dir, line.strip()))

    def load_image_paths_and_labels(self):
        image_paths = []
        labels = []
        if not self.valid_countries:
            self.valid_countries = os.listdir(self.root_dir)
        for label in self.valid_countries:
            label_dir = os.path.join(self.root_dir, label)
            if os.path.isdir(label_dir):
                for image_name in os.listdir(label_dir):
                    image_path = os.path.join(label_dir, image_name)
                    image_paths.append(image_path)
                    labels.append(label)
        return image_paths, labels

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label_str = self.labels[idx]
        label = self.labels_to_idx[label_str]
        label = torch.LongTensor([label])

        image = Image.open(image_path).convert("RGB")
        if self.transform:
            image = self.transform(image)

        return image, label, image_path

# Define the transforms to apply to the images
transform = transforms.Compose([
    #transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# Specify the root directory of your dataset
root_dir = "data/kaggle_dataset/"

# Create an instance of the custom dataset
#dataset = Kaggle50K(root_dir, transform=transform)

# Create an instance of the custom dataset
dataset = Kaggle50K(root_dir, transform=None)  # No transform for visualization

# Select a random sample from the dataset
# sample_index = 8000  # Change this to the desired index
# sample_image, sample_label = dataset[sample_index]

# print("label: " + str(sample_label))
# sample_image.show()


# Create a DataLoader to handle batching and shuffling
#batch_size = 64
#dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Iterate over the dataset using the DataLoader
#for images, labels in dataloader:
    # Your training/validation loop here
    # images and labels contain the batch of images and their labels
#    pass