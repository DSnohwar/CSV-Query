# CSV Data Visualization App

This Streamlit web application allows users to visualize CSV data and summarize it using natural language processing techniques. It leverages the OpenAI Lida library for text summarization, goal extraction, and data visualization.

## Installation

To run this application locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

## Usage

1. Run the Streamlit app by executing `streamlit run app.py` in your terminal.
2. Choose an option from the sidebar:
   - **Generate Visualizations**: Upload a CSV file and query your data to generate plots.
   - **Summarize your CSV**: Upload a CSV file to view a summary of the data along with suggested query plots.

## Dependencies

- Streamlit
- OpenAI GPT-3 Microsoft Lida library
- dotenv
- pandas
- openai
- Pillow

## Background Image Source

The background image used in the application is sourced from Unsplash.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
