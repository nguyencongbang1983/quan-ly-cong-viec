import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ==============================================================================
# 🔴 CẤU HÌNH DỮ LIỆU (QUAN TRỌNG NHẤT)
# ==============================================================================

# 1. Dán Link CSV Công Việc của bạn vào đây (Link cũ của bạn)
LINK_CSV_CONG_VIEC = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSRoKMQ8kMQ4WkjSvfUqwCi5MhX_NYM1r_C7mqmg8gKSwwVSt_FJPN81FClnnrkzUveirIBDKT9YACw/pub?gid=2034795073&single=true&output=csv"

# 2. Dán Link Google Calendar "sạch" vào đây
# (Ví dụ mẫu bên dưới là lịch nghỉ lễ, hãy thay bằng link lịch cơ quan của bạn)
LINK_GOOGLE_CALENDAR = "https://calendar.google.com/calendar/embed?src=a432988c8c04defc4e755100b1c8ca67b255a8ccabc45385da0c201e50edb4ed%40group.calendar.google.com&ctz=Asia%2FHo_Chi_Minh" 

# ==============================================================================
# CẤU HÌNH GIAO DIỆN & CSS (TRÀN VIỀN + GHIM KHẨU HIỆU)
# ==============================================================================
st.set_page_config(page_title="Hệ Thống Quản Lý", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    /* 1. Mở rộng giao diện ra sát lề (Full Width 100%) */
    .block-container {
        padding-top: 5rem !important; /* Chừa chỗ cho khẩu hiệu */
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* 2. ẨN NÚT TOÀN MÀN HÌNH CỦA BẢNG (Để giữ khẩu hiệu luôn hiện) */
    [data-testid="stDataFrame"] button[title="View fullscreen"] {
        display: none !important;
    }
    
    /* 3. Tùy chỉnh giao diện bảng và metric */
    div[data-testid="stMetric"] { background-color: #262730; border: 1px solid #4f4f4f; padding: 10px; border-radius: 5px; }
    h1 { text-align: center; color: #4da6ff; margin-bottom: 20px; }
    div[data-testid="stDataFrame"] { font-size: 14px; }
    thead tr th:first-child {display:none} /* Ẩn cột index */
    tbody th {display:none}

    /* 4. Ẩn Header/Footer mặc định của Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 5. KHẨU HIỆU "BẤT TỬ" (LUÔN GHIM TRÊN ĐẦU) */
    .sticky-marquee {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        background-color: #fff3cd;
        color: #856404;
        z-index: 2147483647;
        border-bottom: 3px solid #ffcc00;
        padding: 10px 0;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        font-family: Arial, sans-serif;
        font-weight: bold;
        font-size: 20px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# ✨ KHẨU HIỆU CỔ ĐỘNG
# ==============================================================================
danh_sach_khau_hieu = [
    "🚀 Việc hôm nay chớ để ngày mai - Hành động ngay!",
    "💪 Thái độ quyết định trình độ - Hãy làm việc bằng cả trái tim!",
    "🔥 Chủ động - Sáng tạo - Hiệu quả - Kỷ luật là sức mạnh!",
    "⭐ Đừng làm việc chăm chỉ, hãy làm việc thông minh!",
    "🤝 Đoàn kết là sức mạnh vô địch - Cùng nhau chúng ta sẽ thành công!",
    "🎯 Tập trung vào giải pháp, đừng tập trung vào vấn đề!",
    "⏰ Thời gian là vàng bạc - Hãy trân trọng từng phút giây!",
    "✨ Mỗi ngày làm tốt một việc nhỏ sẽ tạo nên thành công lớn!",
    "🏆 Kỷ luật là cầu nối giữa mục tiêu và thành tựu!"
]

try:
    cau_hom_nay = random.choice(danh_sach_khau_hieu)
except:
    cau_hom_nay = "Chúc bạn một ngày làm việc hiệu quả!"

st.markdown(f"""
<div class="sticky-marquee">
    <marquee scrollamount="12">
        📢 THÔNG ĐIỆP HÔM NAY: {cau_hom_nay} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 📢 HÃY CÙNG NHAU HOÀN THÀNH TỐT NHIỆM VỤ!
    </marquee>
</div>
""", unsafe_allow_html=True)

st.title("🌐 Hệ Thống Quản Lý & Điều Hành")

# ==============================================================================
# HÀM ĐỌC DỮ LIỆU
# ==============================================================================
if st.button("🔄 Cập nhật dữ liệu mới nhất"):
    st.cache_data.clear()

def load_data_force(link):
    try:
        if "?" in link: link_new = f"{link}&t={datetime.now().timestamp()}"
        else: link_new = f"{link}?t={datetime.now().timestamp()}"
        return pd.read_csv(link_new)
    except: return None

df_congviec = load_data_force(LINK_CSV_CONG_VIEC)

if df_congviec is None:
    st.error("⚠️ Chưa đọc được dữ liệu Công Việc. Vui lòng kiểm tra lại Link CSV.")
    st.stop()

# --- XỬ LÝ TÊN CỘT ---
df_congviec.columns = df_congviec.columns.str.strip()
for col in df_congviec.columns:
    if "Chỉ" in col and "Đạo" in col: df_congviec.rename(columns={col: "Chỉ Đạo"}, inplace=True)
    if "Trạng" in col and "Thái" in col: df_congviec.rename(columns={col: "Trạng Thái"}, inplace=True)

# ==============================================================================
# TAB 1: DASHBOARD QUẢN LÝ
# ==============================================================================
tab1, tab2 = st.tabs(["📊 Dashboard Quản Lý", "📅 Lịch Google Calendar"])

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

        # --- DANH SÁCH CHI TIẾT ---
        st.subheader("📋 Danh sách công việc chi tiết")
        hien_thi_xong = st.checkbox("✅ Hiển thị cả công việc đã Hoàn thành", value=False)
        
        if "Trạng Thái" in df_loc.columns:
            df_display = df_loc.copy()
            def xu_ly_row(row):
                tt = str(row["Trạng Thái"])
                hc = row.get("Hạn Chót", pd.NaT)
                sort = 2
                if 'Hoàn' in tt: sort = 1 
                elif pd.notna(hc):
                    so_ngay_con_lai = (hc - now).days
                    if hc < now:
                        tre = (now - hc).days
                        tt = f"{tt} (Trễ {tre} ngày)"
                        sort = 4
                    elif 0 <= so_ngay_con_lai <= 3:
                        tt = f"{tt} (🔥 Gấp: Còn {so_ngay_con_lai} ngày)"
                        sort = 3
                elif 'Chậm' in tt: sort = 4
                return tt, sort

            df_display[['Trạng Thái Hiển Thị', 'Sort_Order']] = df_display.apply(lambda x: pd.Series(xu_ly_row(x)), axis=1)
            df_display["Trạng Thái"] = df_display["Trạng Thái Hiển Thị"]
            
            if not hien_thi_xong:
                df_display = df_display[df_display['Sort_Order'] != 1]

            cols_sort = ["Sort_Order"]
            if "Hạn Chót" in df_display.columns: cols_sort.append("Hạn Chót")
            df_display = df_display.sort_values(by=cols_sort, ascending=[False, True])

            cols_show = ["Tên Trợ Lý", "Nhiệm Vụ", "Chỉ Đạo", "Trạng Thái", "Tiến Độ (%)", "Hạn Chót", "Sort_Order"]
            final_cols = [c for c in cols_show if c in df_display.columns]

            def to_mau(row):
                s = row.get("Sort_Order", 2)
                if s == 1: return ['background-color: #28a745; color: white'] * len(row)
                if s == 4: return ['background-color: #ff4b4b; color: white; font-weight: bold'] * len(row)
                if s == 3: return ['background-color: #ff8c00; color: white; font-weight: bold'] * len(row)
                return ['background-color: #ffd700; color: black'] * len(row)

            # TÍNH CHIỀU CAO TỰ ĐỘNG
            so_dong = len(df_display)
            if so_dong > 0:
                chieu_cao_tu_dong = (so_dong + 1) * 35 + 3
                if chieu_cao_tu_dong < 150: chieu_cao_tu_dong = 150
            else:
                chieu_cao_tu_dong = 150

            st.dataframe(
                df_display[final_cols].style.apply(to_mau, axis=1),
                use_container_width=True,
                height=chieu_cao_tu_dong,
                column_config={
                    "Hạn Chót": st.column_config.DateColumn("Hạn Chót", format="DD/MM/YYYY"),
                    "Chỉ Đạo": st.column_config.TextColumn("👤 Chỉ Đạo", width="medium"),
                    "Tiến Độ (%)": st.column_config.NumberColumn("Tiến Độ", format="%.0f%%"),
                    "Sort_Order": None,
                }
            )

# ==============================================================================
# TAB 2: LỊCH GOOGLE CALENDAR
# ==============================================================================
with tab2:
    if "http" in LINK_GOOGLE_CALENDAR:
        # Nhúng lịch với chiều cao lớn 850px cho thoải mái
        st.markdown(f'<iframe src="{LINK_GOOGLE_CALENDAR}" style="border: 0" width="100%" height="850" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)
    else:
        st.info("⚠️ Chưa có link Google Calendar.")
