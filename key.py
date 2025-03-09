import torch

# Path to the checkpoint
autoencoder_model_path = "C:/Users/HP/OneDrive/Desktop/vehicle_modivication_detection/models/bajaj_dominar_headlight_autoencoder.pth"

# Load the checkpoint
checkpoint = torch.load(autoencoder_model_path, map_location="cpu")

# Print the keys in the checkpoint
print("Keys in the checkpoint:")
for key in checkpoint.keys():
    print(key)

# If the checkpoint contains a state_dict, inspect it
if "state_dict" in checkpoint:
    print("\nKeys in the state_dict:")
    for key in checkpoint["state_dict"].keys():
        print(key)
elif isinstance(checkpoint, dict):
    print("\nKeys in the model state dict:")
    for key in checkpoint.keys():
        print(key)
else:
    print("\nCheckpoint format is not a dictionary. Verify the file format.")
