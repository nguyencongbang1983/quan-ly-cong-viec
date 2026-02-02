import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime

# ==============================================================================
# CẤU HÌNH DỮ LIỆU (BẠN CHỈ CẦN THAY LINK CỦA BẠN VÀO ĐÂY)
# ==============================================================================
# Dán link Google Sheets của bạn vào giữa 2 dấu ngoặc kép bên dưới
LINK_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/edit?usp=sharing"

# Hàm hỗ trợ đọc dữ liệu từ Google Sheet
@st.cache_data(ttl=60) # Tự động làm mới dữ liệu mỗi 60 giây
def load_data(sheet_name):
    try:
        # Chuyển link view sang link export csv để máy đọc
        csv_url = LINK_GOOGLE_SHEET.replace('/edit?usp=sharing', f'/gviz/tq?tqx=out:csv&sheet={sheet_name}')
        csv_url = csv_url.replace('/edit#gid=', f'/gviz/tq?tqx=out:csv&sheet={sheet_name}')
        return pd.read_csv(csv_url)
    except Exception as e:
        return None

# ==============================================================================
# CẤU HÌNH GIAO DIỆN
# ==============================================================================
st.set_page_config(page_title="Hệ Thống Quản Lý Online", layout="wide", page_icon="🌐")

# CSS Tùy chỉnh (Giữ nguyên giao diện đẹp)
st.markdown("""
<style>
    div[data-testid="stMetric"] { background-color: #262730; border: 1px solid #4f4f4f; padding: 10px; border-radius: 5px; }
    h1 { text-align: center; color: #4da6ff; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    div[data-testid="stDataFrame"] { font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.title("🌐 Hệ Thống Quản Lý & Điều Hành (Online)")

# Tải dữ liệu
df_congviec = load_data("CongViec") # Tên sheet 1 trên Google Sheet phải là CongViec
df_lich = load_data("LichTuan")     # Tên sheet 2 trên Google Sheet phải là LichTuan

if df_congviec is None or df_lich is None:
    st.error("⚠️ Không đọc được dữ liệu! Vui lòng kiểm tra lại đường Link Google Sheets và tên Sheet (CongViec, LichTuan).")
    st.stop()

# TẠO 2 TAB
tab1, tab2 = st.tabs(["📊 Dashboard Quản Lý", "📅 Lịch Công Tác Tuần"])

# ==============================================================================
# TAB 1: DASHBOARD
# ==============================================================================
with tab1:
    # Xử lý dữ liệu công việc
    df = df_congviec.copy()
    df.columns = df.columns.str.strip().str.title()
    if "Trạng Thải" in df.columns: df.rename(columns={"Trạng Thải": "Trạng Thái"}, inplace=True)
    
    # Ép kiểu ngày tháng (Xử lý định dạng ngày trên Google Sheet)
    df["Hạn Chót"] = pd.to_datetime(df["Hạn Chót"], dayfirst=True, errors='coerce')
    df["Tiến Độ (%)"] = df["Tiến Độ (%)"].fillna(0)

    # Bộ lọc
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_tro_ly = st.multiselect("Nhân sự:", df["Tên Trợ Lý"].unique(), default=df["Tên Trợ Lý"].unique())
    with col_f2:
        selected_trang_thai = st.multiselect("Trạng thái:", df["Trạng Thái"].unique(), default=df["Trạng Thái"].unique())

    df_selection = df.query("`Tên Trợ Lý` == @selected_tro_ly & `Trạng Thái` == @selected_trang_thai").copy()

    # KPI & Biểu đồ (Giữ nguyên logic cũ)
    if not df_selection.empty:
        c1, c2, c3, c4 = st.columns(4)
        now = datetime.now()
        viec_qua_han = len(df_selection[(~df_selection["Trạng Thái"].str.contains("Hoàn", na=False)) & (df_selection["Hạn Chót"] < now)])
        c1.metric("Tổng việc", len(df_selection))
        c2.metric("Đã xong", len(df_selection[df_selection["Trạng Thái"].str.contains("Hoàn", na=False)]))
        c3.metric("🚨 Quá hạn", viec_qua_han)
        c4.metric("Ngày báo cáo", now.strftime("%d/%m/%Y"))

        st.markdown("---")
        
        # Bảng phân tích
        analysis_df = df_selection.groupby("Tên Trợ Lý").agg(
            Tong_Viec=("Trạng Thái", "count"),
            Viec_Da_Xong=("Trạng Thái", lambda x: x.str.contains("Hoàn", na=False).sum()),
            Ty_Le_HT=("Tiến Độ (%)", "mean")
        ).reset_index()
        analysis_df["Ty_Le_HT_That"] = (analysis_df["Viec_Da_Xong"] / analysis_df["Tong_Viec"] * 100)
        total = analysis_df["Tong_Viec"].sum()
        analysis_df["Ty_Trong"] = (analysis_df["Tong_Viec"] / total * 100) if total > 0 else 0
        
        st.dataframe(
            analysis_df.style.background_gradient(subset=["Ty_Trong", "Ty_Le_HT_That"], cmap="Blues"),
            use_container_width=True,
            column_config={
                "Ty_Trong": st.column_config.ProgressColumn("Tỷ Trọng", format="%.1f%%", min_value=0, max_value=100),
                "Ty_Le_HT_That": st.column_config.ProgressColumn("Tỷ Lệ Hoàn Thành", format="%.1f%%", min_value=0, max_value=100),
            }
        )

        # Danh sách chi tiết
        st.subheader("📋 Danh sách công việc")
        def to_mau_theo_han(row):
            tt = str(row["Trạng Thái"]).lower()
            if 'hoàn' in tt: return ['background-color: #28a745; color: white'] * len(row)
            if pd.isna(row["Hạn Chót"]): return [''] * len(row)
            days = (row["Hạn Chót"] - now).days
            if days < 0: return ['background-color: #d9534f; color: white'] * len(row)
            return [''] * len(row)

        st.dataframe(
            df_selection.sort_values("Hạn Chót").style.apply(to_mau_theo_han, axis=1),
            use_container_width=True, height=500,
            column_config={"Hạn Chót": st.column_config.DateColumn("Hạn Chót", format="DD/MM/YYYY")}
        )

# ==============================================================================
# TAB 2: LỊCH CÔNG TÁC TUẦN (CO GIÃN THÔNG MINH)
# ==============================================================================
with tab2:
    tong_so_viec = len(df_lich)
    
    # Logic co giãn
    if tong_so_viec <= 10:
        font_size = "16px"; padding = "1rem"; header_size = "20px"
    elif tong_so_viec <= 20:
        font_size = "14px"; padding = "0.5rem"; header_size = "18px"
    else:
        font_size = "12px"; padding = "0.2rem"; header_size = "14px"

    st.markdown(f"""
    <style>
        div[data-testid="stDataFrame"] {{ font-size: {font_size} !important; }}
        td {{ padding-top: {padding} !important; padding-bottom: {padding} !important; line-height: 1.2 !important; }}
    </style>
    """, unsafe_allow_html=True)

    # Hàm sửa giờ
    def chinh_sua_gio(val):
        return str(val).replace("nan","")

    if "Thời Gian" in df_lich.columns:
        df_lich["Thời Gian"] = df_lich["Thời Gian"].apply(chinh_sua_gio)
    
    # Điền dữ liệu trống
    df_lich = df_lich.fillna("")

    # Nhập chỉ huy (Phần này khi lên online sẽ reset mỗi khi load lại, 
    # nếu muốn cố định thì phải nhập thẳng vào Google Sheet)
    st.info("💡 Lưu ý: Trên bản Online, thông tin Trực chỉ huy nên nhập trực tiếp vào file Google Sheet để lưu cố định.")
    
    # Hiển thị lịch
    if not df_lich.empty:
        cac_ngay = df_lich["Thứ Ngày"].unique()
        for ngay in cac_ngay:
            cong_viec_ngay = df_lich[df_lich["Thứ Ngày"] == ngay]
            with st.container():
                st.markdown(f"<div style='background-color: #ff9f1c; padding: 2px 10px; font-weight: bold; margin-top: 5px; font-size: {font_size};'>📅 {ngay}</div>", unsafe_allow_html=True)
                st.dataframe(cong_viec_ngay, use_container_width=True, hide_index=True)
    else:
        st.info("Chưa có dữ liệu.")
