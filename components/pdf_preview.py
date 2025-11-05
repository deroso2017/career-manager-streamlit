import streamlit as st
import fitz  # PyMuPDF

def show_pdf_preview(uploaded_file, pages=1, width=None, show_button=True, show_page_label=True):
    """
    Show PDF preview in Streamlit using PyMuPDF.

    Parameters:
    - uploaded_file: file-like object (BytesIO or st.file_uploader)
    - pages: "all" or int, number of pages to show
    - width: optional, width for st.image
    - show_button: whether to require a click to show preview
    """
    if uploaded_file is None:
        return

    if show_button:
        if not st.button("Show PDF Preview"):
            return
    # Read file bytes once (before spinner)
    file_bytes = uploaded_file.read()

    # Show spinner while processing
    with st.spinner("Rendering PDF... ⏳"):
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        total_pages = pdf.page_count
        pages_to_show = total_pages if pages == "all" else min(pages, total_pages)

        for i in range(pages_to_show):
            page = pdf[i]
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            
            if show_page_label:
                st.subheader(f"Page {i + 1}")
            
            st.image(img_bytes, use_container_width=(width is None), width=width)
