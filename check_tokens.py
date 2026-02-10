import numpy as np
import os

path = r"c:\work\person\hassan\Repos\micro.llama2.c\data\tok512\custom_data.bin"
if os.path.exists(path):
    m = np.memmap(path, dtype=np.uint16, mode="r")
    print(f"Max token ID: {np.max(m)}")
    print(f"Min token ID: {np.min(m)}")
    print(f"Total tokens: {len(m)}")
else:
    print("File not found")
