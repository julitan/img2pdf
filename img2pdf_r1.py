# 올린 이미지들은 하나의 PDF로 합친 뒤,
# 올린 PDF들과 함께 최종적으로 병합하여
# 다운로드할 수 있게 해준다.

import streamlit as st
from PIL import Image
from PyPDF2 import PdfMerger
import io

def main():
    st.title("이미지 & PDF 단일 업로드 → 자동 PDF 변환/병합")

    # 하나의 드래그 앤 드롭 영역에 이미지와 PDF를 동시에 업로드
    uploaded_files = st.file_uploader(
        "이미지(JPG, PNG)와 PDF를 한 번에 올려주세요",
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        # 이미지와 PDF 분류
        image_files = []
        pdf_files = []
        for f in uploaded_files:
            if f.type in ["image/jpeg", "image/png"]:
                image_files.append(f)
            elif f.type == "application/pdf":
                pdf_files.append(f)

        # 1) 이미지들을 하나의 PDF로 변환
        merged_images_pdf = None
        if image_files:
            pil_images = [Image.open(img).convert("RGB") for img in image_files]
            merged_images_pdf = io.BytesIO()
            # 첫 번째 이미지 저장 후 나머지 이미지를 append
            pil_images[0].save(
                merged_images_pdf, format="PDF", save_all=True, append_images=pil_images[1:]
            )
            merged_images_pdf.seek(0)

        # 2) 이미지 PDF와 기존 PDF들 병합
        merger = PdfMerger()
        
        # 이미지 PDF가 있다면 병합에 포함
        if merged_images_pdf is not None:
            merger.append(merged_images_pdf)

        # 업로드된 PDF 파일 병합
        for pdf in pdf_files:
            pdf_data = pdf.read()
            merger.append(io.BytesIO(pdf_data))
        
        # 최종 병합본 작성
        final_merged_pdf = io.BytesIO()
        merger.write(final_merged_pdf)
        merger.close()
        final_merged_pdf.seek(0)

        # 3) 최종 병합된 PDF 다운로드
        st.download_button(
            label="최종 PDF 다운로드",
            data=final_merged_pdf,
            file_name="final_merged.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
