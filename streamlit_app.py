import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd

def xml_to_dict(elem):
    """Đệ quy chuyển ElementTree element -> dict để hiển thị JSON"""
    children = list(elem)
    if not children:
        return elem.text.strip() if elem.text else None

    result = {}
    for child in children:
        tag = child.tag.split("}")[-1]  # bỏ namespace nếu có
        value = xml_to_dict(child)
        if tag in result:
            # Nếu đã tồn tại => chuyển sang list
            if isinstance(result[tag], list):
                result[tag].append(value)
            else:
                result[tag] = [result[tag], value]
        else:
            result[tag] = value
    return result

def find_repeating_elements(elem):
    """
    Tự động tìm phần tử lặp lại nhiều lần trong cùng cấp -> gợi ý chuyển thành DataFrame.
    Trả về list các DataFrame (mỗi DF cho một loại phần tử lặp).
    """
    dataframes = []
    tags_seen = {}
    for child in elem:
        tag = child.tag.split("}")[-1]
        if tag not in tags_seen:
            tags_seen[tag] = []
        tags_seen[tag].append(child)

    for tag, nodes in tags_seen.items():
        if len(nodes) > 1:  # có lặp => chuyển thành bảng
            rows = []
            for node in nodes:
                row = {c.tag.split("}")[-1]: (c.text.strip() if c.text else None) for c in node}
                rows.append(row)
            df = pd.DataFrame(rows)
            dataframes.append((tag, df))

        # Đệ quy tìm lặp trong các node con
        for node in nodes:
            dataframes.extend(find_repeating_elements(node))

    return dataframes

# ========== Streamlit UI ==========
st.set_page_config(page_title="XML Viewer", layout="wide")
st.title("📂 Trình đọc XML đa năng")

uploaded_files = st.file_uploader("Tải lên một hoặc nhiều file XML", type="xml", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📑 File: {file.name}")

        try:
            tree = ET.parse(file)
            root = tree.getroot()
        except Exception as e:
            st.error(f"Lỗi đọc file {file.name}: {e}")
            continue

        # Hiển thị toàn bộ XML dưới dạng JSON
        data_dict = xml_to_dict(root)
        st.markdown("### 🧾 Nội dung XML (dạng JSON)")
        st.json(data_dict)

        # Tìm các bảng lặp lại để hiển thị dạng bảng
        tables = find_repeating_elements(root)
        if tables:
            for tag, df in tables:
                st.markdown(f"### 📊 Bảng `{tag}` ({len(df)} dòng)")
                st.dataframe(df)

                csv = df.to_csv(index=False, encoding="utf-8-sig")
                st.download_button(
                    f"📥 Tải CSV cho {tag}",
                    data=csv,
                    file_name=f"{file.name}_{tag}.csv",
                    mime="text/csv"
                )
        else:
            st.info("Không tìm thấy phần tử lặp để tạo bảng.")
