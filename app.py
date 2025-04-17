import streamlit as st
import os
import shutil
from continuous_stitch import run_pipeline
from PIL import Image

st.title("🔗 Image Stitching with SuperGlue")
st.write("Upload any sequence of images. We'll automatically rename them to a standard format (1.jpg, 2.jpg, ...) for stitching.")

uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    input_dir = "uploaded_images"
    output_dir = os.path.join(input_dir, "output")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Clear previous files (optional)
    for f in os.listdir(input_dir):
        if f.endswith((".jpg", ".jpeg", ".png")):
            os.remove(os.path.join(input_dir, f))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    # Save uploaded files with new sequential names
    renamed_filenames = []
    for idx, file in enumerate(sorted(uploaded_files, key=lambda f: f.name), start=1):
        ext = os.path.splitext(file.name)[-1]
        new_name = f"{idx}.jpg"  # Convert all to .jpg
        new_path = os.path.join(input_dir, new_name)

        with open(new_path, "wb") as f:
            f.write(file.read())

        renamed_filenames.append(new_name)

    start_idx = 1
    end_idx = len(renamed_filenames)

    if st.button("▶️ Run Stitching"):
        with st.spinner("Running SuperGlue and stitching images..."):
            try:
                final_image = run_pipeline(start_idx, end_idx, input_dir, output_dir)
                st.success("✅ Stitching Complete!")

                final_path = os.path.join(input_dir, f"stitched_up_to_{end_idx}.jpg")
                st.image(Image.open(final_path), caption="Final Stitched Image", use_column_width=True)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
