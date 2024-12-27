import streamlit as st
from PIL import Image
from PyPDF2 import PdfMerger
import io
from streamlit_sortables import sort_items

def main():
    st.title("파일 업로드 후 순서 재배열")

    # 세션 상태 초기화
    if 'show_reorder' not in st.session_state:
        st.session_state.show_reorder = False
    if 'file_info' not in st.session_state:
        st.session_state.file_info = []
    if 'reordered_names' not in st.session_state:
        st.session_state.reordered_names = []

    uploaded_files = st.file_uploader(
        "이미지(JPG, PNG) & PDF 업로드 (여러 개)",
        type=["jpg","jpeg","png","pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        # 파일 정보 업데이트
        file_info = [{"name": f.name, "data": f} for f in uploaded_files]
        st.session_state.file_info = file_info
        file_names = [item["name"] for item in file_info]
        st.session_state.reordered_names = file_names

        # 현재 파일 목록 표시
        st.write("업로드된 파일:", file_names)

        # 병합 순서 버튼
        if st.button("병합 순서 설정"):
            st.session_state.show_reorder = not st.session_state.show_reorder

        # 순서 재배열 인터페이스
        if st.session_state.show_reorder:
            st.write("👇 아래 항목들을 드래그하여 순서를 변경하세요")
            st.session_state.reordered_names = sort_items(file_names, key="sortable_list")
            st.write("재배열된 순서:", st.session_state.reordered_names)

        # PDF 병합하기 버튼
        if st.button("PDF 병합하기"):
            name_to_file = {item["name"]: item["data"] for item in st.session_state.file_info}
            ordered_files = [name_to_file[name] for name in st.session_state.reordered_names]

            final_pdf = merge_files_in_order(ordered_files)

            st.download_button(
                label="다운로드 (병합 PDF)",
                data=final_pdf,
                file_name="merged.pdf",
                mime="application/pdf"
            )

def merge_files_in_order(ordered_files):
    """재배열된 순서 그대로 PDF로 병합"""
    merger = PdfMerger()
    
    for f in ordered_files:
        # 파일 포인터 위치 초기화
        f.seek(0)
        
        if f.type in ["image/jpeg", "image/png"]:
            # 이미지를 PDF로 변환
            img = Image.open(f).convert("RGB")
            img_pdf = io.BytesIO()
            img.save(img_pdf, format="PDF")
            img_pdf.seek(0)
            merger.append(img_pdf)
        else:
            # PDF 파일 처리
            pdf_data = io.BytesIO(f.read())
            merger.append(pdf_data)

    # 결과 PDF 반환
    final_pdf = io.BytesIO()
    merger.write(final_pdf)
    merger.close()
    final_pdf.seek(0)
    return final_pdf

if __name__ == "__main__":
    main()