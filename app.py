import base64
import os
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Product Image Tool", layout="wide")
st.title("🧼 Product Image Tool")

if not OPENAI_API_KEY:
    st.error("Missing OPENAI_API_KEY in .env")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)


def edit_image(uploaded_file, prompt):
    result = client.images.edit(
        model="gpt-image-1",
        image=uploaded_file,
        prompt=prompt,
        size="1024x1024",
    )

    image_base64 = result.data[0].b64_json
    return base64.b64decode(image_base64)


tab1, tab2 = st.tabs(["🧼 Clear Logo", "📸 Generate Different Angle"])

with tab1:
    st.subheader("Clear Logo / Text / Watermark")

    uploaded_file = st.file_uploader(
        "Upload product image",
        type=["png", "jpg", "jpeg", "webp"],
        key="clear_logo_upload",
    )

    prompt = st.text_area(
        "Edit prompt",
        value=(
            "Remove all visible logos, brand names, supplier names, watermarks, stickers, and printed text. "
            "Keep the exact same product, same camera angle, same shape, same material, same lighting, and same background. "
            "Do not redesign the product. Fill removed areas naturally so it looks clean and unbranded."
        ),
        height=150,
        key="clear_logo_prompt",
    )

    if uploaded_file:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Original", use_container_width=True)

        if st.button("Clear Logo", key="clear_logo_button"):
            with st.spinner("Cleaning image..."):
                image_bytes = edit_image(uploaded_file, prompt)
                output_path = OUTPUT_DIR / f"cleaned_{int(time.time())}.png"
                output_path.write_bytes(image_bytes)

                with col2:
                    st.image(image_bytes, caption="Cleaned Image", use_container_width=True)
                    st.download_button(
                        "Download cleaned image",
                        data=image_bytes,
                        file_name=output_path.name,
                        mime="image/png",
                    )

with tab2:
    st.subheader("Generate Different Product Angle")

    uploaded_file_angle = st.file_uploader(
        "Upload reference product image",
        type=["png", "jpg", "jpeg", "webp"],
        key="angle_upload",
    )

    angle_prompt = st.text_area(
        "Angle prompt",
        value=(
            "Using the uploaded product as reference, generate a new clean catalog product image from a front three-quarter angle. "
            "Keep the same product identity, material, structure, proportions, and components. "
            "Remove all logos, brand names, supplier names, stickers, and text. "
            "Use a white studio background, realistic biomedical equipment photography, soft shadow, and professional ecommerce style."
        ),
        height=170,
        key="angle_prompt",
    )

    if uploaded_file_angle:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file_angle, caption="Reference Image", use_container_width=True)

        if st.button("Generate New Angle", key="angle_button"):
            with st.spinner("Generating new angle..."):
                image_bytes = edit_image(uploaded_file_angle, angle_prompt)
                output_path = OUTPUT_DIR / f"angle_{int(time.time())}.png"
                output_path.write_bytes(image_bytes)

                with col2:
                    st.image(image_bytes, caption="New Angle Image", use_container_width=True)
                    st.download_button(
                        "Download new angle image",
                        data=image_bytes,
                        file_name=output_path.name,
                        mime="image/png",
                    )