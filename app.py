
import streamlit as st
from video_generator import generate_video

st.set_page_config(
    page_title="AI Property Video Generator",
    page_icon="🏡",
    layout="wide"
)

st.title("🏡 AI Property Video Generator")
st.write("Turn property photos and details into a promotional video.")

st.subheader("Property Details")

with st.form("property_form"):
    property_name = st.text_input("Property Name")
    location = st.text_input("Location")
    price = st.text_input("Price (e.g. ₹75 lakh)")

    property_type = st.selectbox(
        "Property Type",
        ["Apartment", "Villa", "Independent House",
         "Commercial Property", "Plot"]
    )

    features = st.text_area(
        "Key Features",
        placeholder="Spacious bedrooms, modern kitchen, balcony"
    )

    contact = st.text_input(
        "Contact / Call to Action",
        placeholder="Contact us today to enquire"
    )

    images = st.file_uploader(
        "Upload 4–8 Property Images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    submitted = st.form_submit_button("Generate Video")

if submitted:
    missing = []

    if not property_name.strip():
        missing.append("Property Name")
    if not location.strip():
        missing.append("Location")
    if not price.strip():
        missing.append("Price")
    if not features.strip():
        missing.append("Key Features")
    if not contact.strip():
        missing.append("Contact / Call to Action")

    if missing:
        st.error("Please complete: " + ", ".join(missing))
    elif not images or not 4 <= len(images) <= 8:
        st.error("Please upload between 4 and 8 images.")
    else:
        try:
            with st.spinner("Generating your property video..."):
                video_path = generate_video(
                    property_name=property_name,
                    location=location,
                    price=price,
                    property_type=property_type,
                    features=features,
                    contact=contact,
                    images=[image.getvalue() for image in images],
                )

            st.success("Your property video is ready!")

            st.subheader("Video Preview")
            st.video(video_path)

            with open(video_path, "rb") as video_file:
                st.download_button(
                    label="Download MP4 Video",
                    data=video_file,
                    file_name="property_video.mp4",
                    mime="video/mp4",
                )

        except Exception as error:
            st.error(f"Video generation failed: {error}")
