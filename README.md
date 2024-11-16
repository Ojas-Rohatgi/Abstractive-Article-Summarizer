# Abstractive Article Summarizer

An interactive web application that extracts and summarizes articles from URLs. Built with Streamlit, Hugging Face's BART model, and various Python libraries, this tool is designed to efficiently generate concise, meaningful summaries of long articles, making it perfect for students, professionals, and casual readers.

## Features

- **Article Extraction**: Automatically extracts content from an article URL, cleaning up HTML and retaining only the main text.
- **Abstractive Summarization**: Uses the Hugging Face `BART` model to create a summary of the article, ensuring key points are captured in a brief format.
- **PDF Export**: The summarized text is available for download as a formatted PDF with justified text for easy reading.
- **Compression Ratio**: Displays a compression ratio to help users understand how much shorter the summary is compared to the original article.
- **Progress Tracking**: Real-time updates on the summarization process, with a progress bar and estimated time remaining.

## Tech Stack

- **Python**: The core language of the application.
- **Streamlit**: For building the web interface.
- **Transformers**: Hugging Face’s pre-trained BART model for abstractive summarization.
- **Requests & BeautifulSoup**: For scraping and processing article content.
- **ReportLab**: For generating and exporting the summary as a PDF.

## Installation

To run this project locally, you need Python installed on your system. Then, clone this repository and install the required dependencies:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

4. Install the required dependencies:
   
   ```bash
   pip install -r requirements.txt

6. Run the app:
   
   ```bash
   streamlit run app.py

Your app will be available at `http://localhost:8501`

## Usage

1. Enter the URL of an article you want to summarize in the input field.
2. The app will fetch the article, extract its text, and display it.
3. After processing, the summary will be shown on the page.
4. You can download the summarized text as a PDF using the "Download Summary as PDF" button.
5. The app will also display a compression ratio, indicating how much shorter the summary is compared to the original content.

## Example

For example, to summarize an article, you would simply paste the article's URL into the input field and click "Summarize." The app will fetch the content, process it, and display a concise summary with a download link for the PDF.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Hugging Face**: For the pre-trained BART model used for abstractive summarization.
- **Streamlit**: For providing an easy-to-use framework for creating web apps.
- **BeautifulSoup**: For scraping and processing HTML content.
