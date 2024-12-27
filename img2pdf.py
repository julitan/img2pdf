import streamlit as st
from PyPDF2 import PdfMerger
from PIL import Image
import io

def convert_images_to_pdf(images):
    # Pillow의 Image 객체를 이용해 PDF 변환
    pdf_buffer = io.BytesIO()
    images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
    pdf_buffer.seek(0)
    return pdf_buffer

def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merged_pdf = io.BytesIO()
    merger.write(merged_pdf)
    merger.close()
    merged_pdf.seek(0)
    return merged_pdf

def main():
    st.title("Image to PDF & PDF Merge App")
    st.write("JPG/PNG 이미지를 하나의 PDF로 만들고, 최대 3개의 PDF를 병합할 수 있다.")

    # 1) 이미지 → PDF 변환 섹션
    st.subheader("1. 이미지 → PDF 변환")
    img_files = st.file_uploader(
        "이미지를 업로드하세요 (JPG, PNG)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    if img_files:
        # PIL Image 객체 생성
        images = [Image.open(img).convert("RGB") for img in img_files]
        pdf_buffer = convert_images_to_pdf(images)
        
        st.download_button(
            label="다운로드 (이미지 → PDF)",
            data=pdf_buffer,
            file_name="converted_images.pdf",
            mime="application/pdf"
        )

    # 2) PDF 병합 섹션
    st.subheader("2. PDF 병합")
    pdf_files = st.file_uploader(
        "최대 3개의 PDF를 업로드하세요",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if pdf_files:
        if len(pdf_files) > 3:
            st.warning("3개 이하의 PDF만 업로드 해주세요.")
        else:
            pdf_buffers = [pdf.read() for pdf in pdf_files]
            merged_pdf = merge_pdfs(io.BytesIO(pdf) for pdf in pdf_buffers)
            
            st.download_button(
                label="다운로드 (병합 PDF)",
                data=merged_pdf,
                file_name="merged.pdf",
                mime="application/pdf"
            )

    # 리셋 버튼
    # 다운로드 후 새로운 작업을 쉽게 할 수 있도록 리셋
    if st.button("Reset"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
