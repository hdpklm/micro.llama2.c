
import torch
import os

ckpt_path = "out/ckpt.pt"
if os.path.exists(ckpt_path):
    try:
        checkpoint = torch.load(ckpt_path, map_location="cpu")
        print(f"Checkpoint iter_num: {checkpoint.get('iter_num')}")
        print(f"Checkpoint best_val_loss: {checkpoint.get('best_val_loss')}")
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
else:
    print(f"Checkpoint not found at {ckpt_path}")
