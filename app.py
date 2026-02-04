import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================================================================
# 🔴 DÁN LINK CSV MỚI CỦA BẠN VÀO 2 DÒNG DƯỚI ĐÂY
# (Link phải có đuôi output=csv)
# ==============================================================================
LINK_CSV_CONG_VIEC = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSRoKMQ8kMQ4WKjSvfUqwCi5MhX_NYM1r_C7mqmg8gKSWwVSt_FJPN81FClnnrkzUveirIBDKT9YACw/pub?gid=2034795073&single=true&output=csv"
LINK_CSV_LICH_TUAN = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSRoKMQ8kMQ4WKjSvfUqwCi5MhX_NYM1r_C7mqmg8gKSWwVSt_FJPN81FClnnrkzUveirIBDKT9YACw/pub?gid=959725079&single=true&output=csv"

# ==============================================================================
# CẤU HÌNH
# ==============================================================================
st.set_page_config(page_title="Hệ Thống Quản Lý", layout="wide", page_icon="🌐")
st.title("🌐 Hệ Thống Quản Lý & Điều Hành")

# NÚT LÀM MỚI DỮ LIỆU THỦ CÔNG
if st.button("🔄 BẤM VÀO ĐÂY ĐỂ CẬP NHẬT DỮ LIỆU MỚI NHẤT"):
    st.cache_data.clear()

# ==============================================================================
# HÀM ĐỌC DỮ LIỆU (ĐÃ TẮT CACHE ĐỂ SỬA LỖI)
# ==============================================================================
def load_data_force(link):
    try:
        # Thêm tham số ngẫu nhiên để lừa máy chủ Google trả về dữ liệu mới nhất
        if "?" in link:
            link_new = f"{link}&cache_buster={datetime.now().timestamp()}"
        else:
            link_new = f"{link}?cache_buster={datetime.now().timestamp()}"
            
        return pd.read_csv(link_new)
    except Exception as e:
        return None

# Tải dữ liệu
df_congviec = load_data_force(LINK_CSV_CONG_VIEC)
df_lich = load_data_force(LINK_CSV_LICH_TUAN)

# 🛑 KIỂM TRA NGAY LẬP TỨC
if df_congviec is None:
    st.error("⚠️ Lỗi: Link CSV không hoạt động. Vui lòng kiểm tra lại đường link.")
    st.stop()

# Hiển thị thông tin cột để Debug (Bạn sẽ thấy cái này trên Web)
st.info(f"ℹ️ Máy tính đang đọc được {len(df_congviec)} công việc. Các cột tìm thấy: {list(df_congviec.columns)}")

# ==============================================================================
# XỬ LÝ DỮ LIỆU
# ==============================================================================
# 1. Xóa khoảng trắng thừa
df_congviec.columns = df_congviec.columns.str.strip()

# 2. Đổi tên cột chuẩn xác
for col in df_congviec.columns:
    if "Chỉ" in col and "Đạo" in col:
        df_congviec.rename(columns={col: "Chỉ Đạo"}, inplace=True)
    if "Trạng" in col and "Thái" in col: # Xử lý cả Trạng Thải/Trạng Thái
        df_congviec.rename(columns={col: "Trạng Thái"}, inplace=True)

# ==============================================================================
# HIỂN THỊ DASHBOARD
# ==============================================================================
tab1, tab2 = st.tabs(["📊 Công Việc", "📅 Lịch Tuần"])

with tab1:
    df = df_congviec.copy()
    
    # Ép kiểu ngày
    if "Hạn Chót" in df.columns:
        df["Hạn Chót"] = pd.to_datetime(df["Hạn Chót"], dayfirst=True, errors='coerce')

    # Bộ lọc
    col_f1, col_f2 = st.columns(2)
    col_tro_ly = "Tên Trợ Lý" if "Tên Trợ Lý" in df.columns else df.columns[0]
    
    with col_f1:
        selected_tro_ly = st.multiselect("Nhân sự:", df[col_tro_ly].unique(), default=df[col_tro_ly].unique())
    
    if "Trạng Thái" in df.columns:
        with col_f2:
            selected_trang_thai = st.multiselect("Trạng thái:", df["Trạng Thái"].unique(), default=df["Trạng Thái"].unique())
        # Lọc
        df_display = df[df[col_tro_ly].isin(selected_tro_ly) & df["Trạng Thái"].isin(selected_trang_thai)].copy()
    else:
        df_display = df[df[col_tro_ly].isin(selected_tro_ly)].copy()

    # --- LOGIC XỬ LÝ (GIỮ NGUYÊN) ---
    st.subheader("📋 Danh sách công việc")

    if "Trạng Thái" in df_display.columns:
        def xu_ly_row(row):
            tt = str(row["Trạng Thái"])
            hc = row.get("Hạn Chót", pd.NaT)
            now = datetime.now()
            
            # Logic cũ của bạn
            sort = 2
            if 'Hoàn' in tt: sort = 1
            elif pd.notna(hc) and hc < now:
                tre = (now - hc).days
                if tre > 0: 
                    tt = f"{tt} (Trễ {tre} ngày)"
                    sort = 3
            elif 'Chậm' in tt: sort = 3
            return tt, sort

        df_display[['Trạng Thái Hiển Thị', 'Sort_Order']] = df_display.apply(lambda x: pd.Series(xu_ly_row(x)), axis=1)
        df_display["Trạng Thái"] = df_display["Trạng Thái Hiển Thị"]
        
        # Sắp xếp
        cols_sort = ["Sort_Order"]
        if "Hạn Chót" in df_display.columns: cols_sort.append("Hạn Chót")
        df_display = df_display.sort_values(by=cols_sort)

        # Cấu hình cột hiển thị (CỐ ĐỊNH CỘT CHỈ ĐẠO)
        cols_show = ["Tên Trợ Lý", "Nhiệm Vụ", "Chỉ Đạo", "Trạng Thái", "Tiến Độ (%)", "Hạn Chót"]
        # Chỉ lấy cột nào CÓ THẬT trong dữ liệu
        final_cols = [c for c in cols_show if c in df_display.columns]

        def to_mau(row):
            s = row.get("Sort_Order", 2)
            if s == 1: return ['background-color: #28a745; color: white'] * len(row)
            if s == 3: return ['background-color: #ff4b4b; color: white'] * len(row)
            return ['background-color: #ffa421; color: black'] * len(row)

        st.dataframe(
            df_display[final_cols].style.apply(to_mau, axis=1),
            use_container_width=True, height=600,
            column_config={
                "Hạn Chót": st.column_config.DateColumn("Hạn Chót", format="DD/MM/YYYY"),
                "Chỉ Đạo": st.column_config.TextColumn("👤 Chỉ Đạo", width="medium") # Cố định cột này
            }
        )
    else:
        st.error("Không tìm thấy cột 'Trạng Thái'. Vui lòng kiểm tra file Excel.")

with tab2:
    if df_lich is not None:
        st.dataframe(df_lich, use_container_width=True)
