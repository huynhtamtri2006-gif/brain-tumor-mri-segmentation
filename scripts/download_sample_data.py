import os
import pandas as pd

img_dir = "data/sample/images"
mask_dir = "data/sample/masks"

os.makedirs(img_dir, exist_ok=True)
os.makedirs(mask_dir, exist_ok=True)

print("Reading parquet sample...")
url = "https://huggingface.co/datasets/sergiomadrid/isic-melanoma-segmentation/resolve/main/data/test-00000-of-00006.parquet"
df = pd.read_parquet(url)

print(f"Total rows in chunk: {len(df)}")
# Extract 20 curated samples
num_samples = 20

metadata = []

for i in range(num_samples):
    row = df.iloc[i]
    sample_id = f"ISIC_sample_{i+1:03d}"
    
    img_filename = f"{sample_id}.jpg"
    mask_filename = f"{sample_id}_mask.png"
    
    img_path = os.path.join(img_dir, img_filename)
    mask_path = os.path.join(mask_dir, mask_filename)
    
    with open(img_path, "wb") as f:
        f.write(row["image"]["bytes"])
        
    with open(mask_path, "wb") as f:
        f.write(row["mask"]["bytes"])
        
    metadata.append({
        "sample_id": sample_id,
        "image_file": img_filename,
        "mask_file": mask_filename,
        "image_size_bytes": len(row["image"]["bytes"]),
        "mask_size_bytes": len(row["mask"]["bytes"])
    })

meta_df = pd.DataFrame(metadata)
meta_df.to_csv("data/sample/metadata.csv", index=False)

print(f"DONE! Successfully extracted {num_samples} sample pairs into {img_dir} and {mask_dir}!")
