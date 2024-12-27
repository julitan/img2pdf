# img, pdf 목록 순서 재배치 보완 

import streamlit as st
from PIL import Image
from PyPDF2 import PdfMerger
import io
from streamlit_sortables import sort_items

def main():
    st.title("파일 업로드 후 순서 재배열 - 단일 컨테이너 예시")

    uploaded_files = st.file_uploader(
        "여러 이미지를 JPG/PNG/PDF로 업로드 (드래그 앤 드롭)",
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        # 업로드된 파일 정보 정리
        file_info = [{"name": f.name, "data": f} for f in uploaded_files]
        file_names = [item["name"] for item in file_info]

        st.write("현재 순서:", file_names)

        # sort_items: 단일 컨테이너 모드 (multi_containers=False)
        # - 첫 번째 인수: list[str]
        # - 반환값도 list[str] 형태로, 재배열된 순서를 반환
        reordered_names = sort_items(
            file_names, 
            key="sort_files_list"  # 각 sort_items 호출마다 유일한 key 설정
        )

        st.write("재배열된 순서:", reordered_names)

        # 재배열된 순서대로 파일 가져오기
        if st.button("PDF 병합하기"):
            name_to_file = {item["name"]: item["data"] for item in file_info}
            ordered_files = [name_to_file[name] for name in reordered_names]

            final_pdf = merge_files_in_order(ordered_files)

            st.download_button(
                label="다운로드 (병합 PDF)",
                data=final_pdf,
                file_name="merged.pdf",
                mime="application/pdf"
            )

def merge_files_in_order(ordered_files):
    """이미지를 PDF로 변환한 뒤, 업로드된 PDF들과 이어서 병합해 최종 PDF를 반환."""
    images = []
    pdfs = []

    for f in ordered_files:
        if f.type in ["image/jpeg", "image/png"]:
            images.append(f)
        else:
            pdfs.append(f)

    merged_images_pdf = None
    if images:
        pil_images = [Image.open(img).convert("RGB") for img in images]
        merged_images_pdf = io.BytesIO()
        pil_images[0].save(
            merged_images_pdf,
            format="PDF",
            save_all=True,
            append_images=pil_images[1:]
        )
        merged_images_pdf.seek(0)

    merger = PdfMerger()

    # 먼저 이미지로 만든 PDF 병합
    if merged_images_pdf:
        merger.append(merged_images_pdf)

    # 그 뒤 업로드한 PDF 병합
    for pdf in pdfs:
        pdf_data = pdf.read()
        merger.append(io.BytesIO(pdf_data))

    final_pdf = io.BytesIO()
    merger.write(final_pdf)
    merger.close()
    final_pdf.seek(0)
    return final_pdf

if __name__ == "__main__":
    main()
