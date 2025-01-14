import os
from shutil import copyfile

def split_dataset(dataset_path, output_path, split_ratio=(0.7, 0.2, 0.1)):
    images = [f for f in os.listdir(dataset_path) if f.endswith(('.png', '.jpg'))]
    total = len(images)
    train_count = int(total * split_ratio[0])
    val_count = int(total * split_ratio[1])

    datasets = {
        "train": images[:train_count],
        "valid": images[train_count:train_count + val_count],
        "test": images[train_count + val_count:]
    }

    for split, files in datasets.items():
        split_dir = os.path.join(output_path, split)
        os.makedirs(split_dir, exist_ok=True)
        for file in files:
            copyfile(os.path.join(dataset_path, file), os.path.join(split_dir, file))
