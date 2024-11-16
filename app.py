from transformers import pipeline
import streamlit as st
import requests
from bs4 import BeautifulSoup
import html
import time
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.enums import TA_JUSTIFY

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Set page layout to wide
st.set_page_config(layout="wide")


# Function to create PDF with justified text
def create_pdf(text):
    # Create a BytesIO buffer to avoid saving the PDF to disk
    pdf_buffer = BytesIO()

    # Define the PDF document layout and page size
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)

    # Define a style for justified text
    styles = getSampleStyleSheet()
    justified_style = ParagraphStyle(
        name="JustifiedStyle",
        parent=styles["BodyText"],
        alignment=TA_JUSTIFY,
        fontSize=12,
        leading=15  # Adjust line spacing as needed
    )

    # Create a Paragraph object with justified text
    paragraph = Paragraph(text, justified_style)

    # Build the PDF in the buffer
    elements = [paragraph]
    doc.build(elements)

    # Move the buffer to the beginning so Streamlit can read it
    pdf_buffer.seek(0)
    return pdf_buffer


# Main application
def main():
    st.title("Article Extractor and Summarizer")

    # Get URL from the user
    url = st.text_input("Share an article URL:", key="url")

    # Define max chunk size to split article into manageable parts
    max_chunk = 300

    if url:
        try:
            # Fetch and parse the article
            response = requests.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all(['h1', 'p'])

            # Clean and concatenate text
            text = [html.unescape(result.get_text()) for result in results]
            article = ' '.join(text)

            # Display the extracted article text in a scrollable window
            st.subheader("Extracted Article Content")
            st.text_area("Article", article, height=300)
            st.markdown(f"**Article Length:** {len(article)} characters")

            # Preprocess text for chunking
            article = article.replace('.', '.<eos>').replace('?', '?<eos>').replace('!', '!<eos>')
            sentences = article.split('<eos>')
            current_chunk = 0
            chunks = [[]]

            # Split text into manageable chunks
            for sentence in sentences:
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))

            # Join words back to form full sentences for each chunk
            for chunk_id in range(len(chunks)):
                chunks[chunk_id] = ' '.join(chunks[chunk_id])

            # Streamlit progress bar, dynamic status display, and summaries list
            progress_bar = st.progress(0)
            status_text = st.empty()  # Placeholder for dynamic status updates
            summaries = []
            start_time = time.time()

            # Summarize each chunk and update progress
            for i, chunk in enumerate(chunks):
                summary = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
                summaries.append(summary[0]['summary_text'])

                # Calculate and display percentage completed and estimated time
                percent_complete = (i + 1) / len(chunks)
                elapsed_time = time.time() - start_time
                estimated_total_time = elapsed_time / percent_complete
                estimated_time_remaining = estimated_total_time - elapsed_time

                # Update progress bar and status text
                progress_bar.progress(percent_complete)
                status_text.markdown(f"**Progress:** {percent_complete * 100:.2f}% - "
                                     f"**Estimated time remaining:** {estimated_time_remaining:.2f} seconds")

            # Combine summaries into a single text output
            summary_text = ' '.join(summaries)

            # Display the summarized text
            st.subheader("Summarized Article Content")
            st.text_area("Summary", summary_text, height=300)
            st.markdown(f"**Summary Length:** {len(summary_text)} characters")

            # Create the PDF from the summary text with justified alignment and wrapping
            pdf_buffer = create_pdf(summary_text)

            # Display the download button for the PDF
            st.download_button(
                label="Download Summary as PDF",
                data=pdf_buffer,
                file_name="summarized_article.pdf",
                mime="application/pdf"
            )

            # Display the compression ratio
            original_length = len(article.split())
            summary_length = len(summary_text.split())
            compression_ratio = (summary_length / original_length) * 100

            # Evaluate if the compression ratio is good or bad
            if compression_ratio < 20:
                st.success(
                    f"{round(compression_ratio)}% Great Compression!\nThe summary is succinct and effectively "
                    f"highlights key points.")
            elif 20 <= compression_ratio <= 40:
                st.info(
                    f"{round(compression_ratio)}% Well-balanced Summary.\nIt maintains essential details while being "
                    f"brief.")
            else:
                st.warning(
                    f"{round(compression_ratio)}% Compression may be excessive.\nThe summary could be too brief and "
                    f"miss important details.")

        except Exception as e:
            st.warning(f"Error: {e}")


# Run the app
if __name__ == '__main__':
    main()
