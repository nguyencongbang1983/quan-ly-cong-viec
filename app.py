import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================================================================
# 🔴 CẤU HÌNH LINK DỮ LIỆU (BẠN DÁN LINK CSV CỦA BẠN VÀO ĐÂY)
# ==============================================================================
LINK_CSV_CONG_VIEC = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSRoKMQ8kMQ4WKjSvfUqwCi5MhX_NYM1r_C7mqmg8gKSWwVSt_FJPN81FClnnrkzUveirIBDKT9YACw/pub?gid=2034795073&single=true&output=csv"
LINK_CSV_LICH_TUAN = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSRoKMQ8kMQ4WKjSvfUqwCi5MhX_NYM1r_C7mqmg8gKSWwVSt_FJPN81FClnnrkzUveirIBDKT9YACw/pub?gid=959725079&single=true&output=csv"

# ==============================================================================
# CẤU HÌNH GIAO DIỆN
# ==============================================================================
st.set_page_config(page_title="Hệ Thống Quản Lý", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    div[data-testid="stMetric"] { background-color: #262730; border: 1px solid #4f4f4f; padding: 10px; border-radius: 5px; }
    h1 { text-align: center; color: #4da6ff; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    div[data-testid="stDataFrame"] { font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.title("🌐 Hệ Thống Quản Lý & Điều Hành")

# Nút cập nhật thủ công
if st.button("🔄 Cập nhật dữ liệu mới nhất"):
    st.cache_data.clear()

# ==============================================================================
# HÀM ĐỌC DỮ LIỆU
# ==============================================================================
def load_data_force(link):
    try:
        if "?" in link: link_new = f"{link}&t={datetime.now().timestamp()}"
        else: link_new = f"{link}?t={datetime.now().timestamp()}"
        return pd.read_csv(link_new)
    except: return None

df_congviec = load_data_force(LINK_CSV_CONG_VIEC)
df_lich = load_data_force(LINK_CSV_LICH_TUAN)

if df_congviec is None:
    st.error("⚠️ Chưa đọc được dữ liệu. Kiểm tra Link CSV.")
    st.stop()

# --- XỬ LÝ TÊN CỘT ---
df_congviec.columns = df_congviec.columns.str.strip()
for col in df_congviec.columns:
    if "Chỉ" in col and "Đạo" in col: df_congviec.rename(columns={col: "Chỉ Đạo"}, inplace=True)
    if "Trạng" in col and "Thái" in col: df_congviec.rename(columns={col: "Trạng Thái"}, inplace=True)

# ==============================================================================
# TAB 1: DASHBOARD
# ==============================================================================
tab1, tab2 = st.tabs(["📊 Dashboard Quản Lý", "📅 Lịch Công Tác Tuần"])

with tab1:
    df = df_congviec.copy()
    if "Hạn Chót" in df.columns:
        df["Hạn Chót"] = pd.to_datetime(df["Hạn Chót"], dayfirst=True, errors='coerce')
    df["Tiến Độ (%)"] = df["Tiến Độ (%)"].fillna(0)

    # --- BỘ LỌC ---
    col_f1, col_f2 = st.columns(2)
    col_tro_ly = "Tên Trợ Lý" if "Tên Trợ Lý" in df.columns else df.columns[0]
    
    with col_f1:
        ds_tro_ly = df[col_tro_ly].unique()
        selected_tro_ly = st.multiselect("Nhân sự:", ds_tro_ly, default=ds_tro_ly)
    
    with col_f2:
        if "Trạng Thái" in df.columns:
            ds_trang_thai = df["Trạng Thái"].unique()
            selected_trang_thai = st.multiselect("Trạng thái:", ds_trang_thai, default=ds_trang_thai)
            df_loc = df[df[col_tro_ly].isin(selected_tro_ly) & df["Trạng Thái"].isin(selected_trang_thai)].copy()
        else:
            df_loc = df[df[col_tro_ly].isin(selected_tro_ly)].copy()

    # --- KPI ---
    if not df_loc.empty:
        c1, c2, c3, c4 = st.columns(4)
        now = datetime.now()
        tong = len(df_loc)
        xong = len(df_loc[df_loc["Trạng Thái"].str.contains("Hoàn", na=False)]) if "Trạng Thái" in df_loc.columns else 0
        tre = len(df_loc[(~df_loc["Trạng Thái"].str.contains("Hoàn", na=False)) & (df_loc["Hạn Chót"] < now)]) if "Hạn Chót" in df_loc.columns else 0
        
        c1.metric("Tổng việc", tong)
        c2.metric("Đã xong", xong)
        c3.metric("🚨 Quá hạn", tre)
        c4.metric("Ngày báo cáo", now.strftime("%d/%m/%Y"))
        st.markdown("---")
        
        # --- BẢNG TỶ TRỌNG ---
        if col_tro_ly in df_loc.columns and "Trạng Thái" in df_loc.columns:
            analysis = df_loc.groupby(col_tro_ly).agg(
                Tong_Viec=("Trạng Thái", "count"),
                Viec_Da_Xong=("Trạng Thái", lambda x: x.str.contains("Hoàn", na=False).sum()),
                Tien_Do_TB=("Tiến Độ (%)", "mean")
            ).reset_index()
            total_jobs = analysis["Tong_Viec"].sum()
            analysis["Ty_Trong"] = (analysis["Tong_Viec"] / total_jobs * 100) if total_jobs > 0 else 0
            analysis["Ty_Le_HT_That"] = (analysis["Viec_Da_Xong"] / analysis["Tong_Viec"] * 100)
            
            st.dataframe(
                analysis.style.background_gradient(subset=["Ty_Trong", "Ty_Le_HT_That"], cmap="Blues"),
                use_container_width=True,
                column_config={
                    "Ty_Trong": st.column_config.ProgressColumn("Tỷ Trọng", format="%.1f%%", min_value=0, max_value=100),
                    "Ty_Le_HT_That": st.column_config.ProgressColumn("Tỷ Lệ HT", format="%.1f%%", min_value=0, max_value=100),
                }
            )

        # --- DANH SÁCH CHI TIẾT (ĐÃ SỬA LỖI MÀU SẮC) ---
        st.subheader("📋 Danh sách công việc chi tiết")
        
        if "Trạng Thái" in df_loc.columns:
            # 1. TÍNH TOÁN
            def xu_ly_row(row):
                tt = str(row["Trạng Thái"])
                hc = row.get("Hạn Chót", pd.NaT)
                
                sort = 2 # Mặc định: Vàng (Đang làm)
                
                # Ưu tiên 1: Hoàn thành (Xanh)
                if 'Hoàn' in tt: 
                    sort = 1 
                
                # Ưu tiên 3: Quá hạn / Chậm (Đỏ)
                elif pd.notna(hc) and hc < now:
                    tre = (now - hc).days
                    if tre > 0: 
                        tt = f"{tt} (Trễ {tre} ngày)"
                        sort = 3 
                elif 'Chậm' in tt or 'Trễ' in tt: 
                    sort = 3
                
                return tt, sort

            df_loc[['Trạng Thái Hiển Thị', 'Sort_Order']] = df_loc.apply(lambda x: pd.Series(xu_ly_row(x)), axis=1)
            df_loc["Trạng Thái"] = df_loc["Trạng Thái Hiển Thị"]
            
            # 2. SẮP XẾP
            cols_sort = ["Sort_Order"]
            if "Hạn Chót" in df_loc.columns: cols_sort.append("Hạn Chót")
            df_display = df_loc.sort_values(by=cols_sort)

            # 3. CHUẨN BỊ CỘT ĐỂ HIỂN THỊ
            # Lưu ý: PHẢI đưa cột Sort_Order vào đây thì hàm tô màu mới đọc được
            cols_show = ["Tên Trợ Lý", "Nhiệm Vụ", "Chỉ Đạo", "Trạng Thái", "Tiến Độ (%)", "Hạn Chót", "Sort_Order"]
            final_cols = [c for c in cols_show if c in df_display.columns]

            # 4. HÀM TÔ MÀU (Đã test kỹ)
            def to_mau(row):
                # Lấy giá trị Sort_Order của dòng hiện tại
                s = row.get("Sort_Order", 2)
                
                if s == 1: return ['background-color: #28a745; color: white'] * len(row) # Xanh lá
                if s == 3: return ['background-color: #ff4b4b; color: white'] * len(row) # Đỏ
                return ['background-color: #ffa421; color: black'] * len(row) # Vàng cam

            # 5. HIỂN THỊ VÀ ẨN CỘT SORT_ORDER
            st.dataframe(
                df_display[final_cols].style.apply(to_mau, axis=1),
                use_container_width=True, height=600,
                column_config={
                    "Hạn Chót": st.column_config.DateColumn("Hạn Chót", format="DD/MM/YYYY"),
                    "Chỉ Đạo": st.column_config.TextColumn("👤 Chỉ Đạo", width="medium"),
                    "Tiến Độ (%)": st.column_config.NumberColumn("Tiến Độ", format="%.0f%%"),
                    "Sort_Order": None, # <--- BÍ KÍP: Ẩn cột này đi để bảng đẹp
                }
            )

# ==============================================================================
# TAB 2: LỊCH TUẦN
# ==============================================================================
with tab2:
    if df_lich is not None:
        tong_so_viec = len(df_lich)
        if tong_so_viec <= 10: font_size = "16px"; padding = "1rem"
        elif tong_so_viec <= 20: font_size = "14px"; padding = "0.5rem"
        else: font_size = "12px"; padding = "0.2rem"

        st.markdown(f"""<style>div[data-testid="stDataFrame"] {{ font-size: {font_size} !important; }} td {{ padding-top: {padding} !important; padding-bottom: {padding} !important; line-height: 1.2 !important; }}</style>""", unsafe_allow_html=True)
        
        def sua_gio(val): return str(val).replace("nan","")
        if "Thời Gian" in df_lich.columns: df_lich["Thời Gian"] = df_lich["Thời Gian"].apply(sua_gio)
        df_lich = df_lich.fillna("")

        cac_ngay = df_lich["Thứ Ngày"].unique()
        for ngay in cac_ngay:
            cong_viec_ngay = df_lich[df_lich["Thứ Ngày"] == ngay]
            with st.container():
                st.markdown(f"<div style='background-color: #ff9f1c; padding: 2px 10px; font-weight: bold; margin-top: 5px; color: black; font-size: {font_size};'>📅 {ngay}</div>", unsafe_allow_html=True)
                st.dataframe(
                    cong_viec_ngay, use_container_width=True, hide_index=True,
                    column_config={"Nội Dung": st.column_config.TextColumn("Nội Dung", width="large")}
                )
    else:
        st.info("Chưa có dữ liệu lịch tuần.")
