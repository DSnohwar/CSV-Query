import streamlit as st 
from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import openai
from PIL import Image
from io import BytesIO
import base64
import pandas as pd

page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("Visualize your CSV Data:")

load_dotenv()
# Assuming your API key is stored in the environment variable OPENAI_API_KEY
openai.api_key = os.getenv('OPENAI_API_KEY')


def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)

    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))


lida = Manager(text_gen=llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)

menu = st.sidebar.selectbox("Choose an Option", ["Generate Visualizations", "Summarize your CSV"])

if menu == "Summarize your CSV":
    st.subheader("Summarization of your Data")
    file_uploader = st.file_uploader("Upload your CSV", type="csv")
    if file_uploader is not None:
        path_to_save = "data.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        summary = lida.summarize("data.csv", summary_method="default", textgen_config=textgen_config)
        print(summary)
        # Extract relevant data from the summary dictionary
        data = []
        for field in summary["fields"]:
            column_name = field["column"]
            properties = field["properties"]
            samples = properties["samples"]
            # Concatenate samples as comma-separated string
            if isinstance(samples, list):
                samples_str = ", ".join(map(str, samples))
            else:
                samples_str = str(samples)  # Handle single sample case
            data.append({
                "Column Name": column_name,
                "Data Type": properties["dtype"],
                "Unique Values": properties["num_unique_values"],
                "Min": properties.get("min", None),  # Handle cases where 'min' might not exist
                "Max": properties.get("max", None),  # Handle cases where 'max' might not exist
                "Standard Deviation": properties.get("std", None),  # Handle cases where 'std' might not exist
                "Samples": samples_str
            })

        # Create a pandas DataFrame from the extracted data
        df = pd.DataFrame(data)

        # Display the DataFrame in a table format using Streamlit
        st.table(df)
        goals = lida.goals(summary, n=3, textgen_config=textgen_config)
        # print(goals)
        st.subheader("Suggested Query Plots")
        for i, goal in enumerate(goals):  # Use enumerate to get index and goal
            st.markdown(f"## Goal {i+1}")  # Add a heading for each goal

            # Display question
            st.write("**Question:**", goal.question)

            # Display rationale
            st.write("**Rationale:**", goal.rationale)

            # Display visualization
            library = "seaborn"
            charts = lida.visualize(summary=summary, goal=goal, textgen_config=textgen_config, library=library)
            img_base64_string = charts[0].raster
            img = base64_to_image(img_base64_string)
            st.image(img)


elif menu == "Generate Visualizations":
    st.subheader("Query your Data to Generate Plots")
    file_uploader = st.file_uploader("Upload your CSV", type="csv")
    if file_uploader is not None:
        path_to_save = "data1.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        text_area = st.text_area("Query your Data to Generate Plots", height=200)
        if st.button("Generate Graph"):
            if len(text_area) > 0:
                st.info("Your Query: " + text_area)
                lida = Manager(text_gen=llm("openai"))
                textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
                summary = lida.summarize("data1.csv", summary_method="default", textgen_config=textgen_config)
                user_query = text_area
                charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config)
                image_base64 = charts[0].raster
                img = base64_to_image(image_base64)
                st.image(img)