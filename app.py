import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ==============================================================================
# 🔴 CẤU HÌNH DỮ LIỆU (ĐÃ ĐIỀN CHUẨN)
# ==============================================================================
LINK_CSV_CONG_VIEC = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSRoKMQ8kMQ4WKjSvfUqwCi5MhX_NYM1r_C7mqmg8gKSWwVSt_FJPN81FClnnrkzUveirIBDKT9YACw/pub?gid=2034795073&single=true&output=csv"
LINK_GOOGLE_CALENDAR = "https://calendar.google.com/calendar/embed?src=a432988c8c04defc4e755100b1c8ca67b255a8ccabc45385da0c201e50edb4ed%40group.calendar.google.com&ctz=Asia%2FHo_Chi_Minh"

# ==============================================================================
# CẤU HÌNH GIAO DIỆN & CSS
# ==============================================================================
st.set_page_config(page_title="Hệ Thống Quản Lý", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    .block-container {
        padding-top: 5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    [data-testid="stDataFrame"] button[title="View fullscreen"] { display: none !important; }
    div[data-testid="stMetric"] { background-color: #262730; border: 1px solid #4f4f4f; padding: 10px; border-radius: 5px; }
    h1 { text-align: center; color: #4da6ff; }
    div[data-testid="stDataFrame"] { font-size: 14px; }
    thead tr th:first-child {display:none}
    tbody th {display:none}
    header, footer, .stDeployButton {visibility: hidden; display:none;}

    .sticky-marquee {
        position: fixed; top: 0; left: 0; width: 100vw;
        background-color: #fff3cd; color: #856404;
        z-index: 2147483647; border-bottom: 3px solid #ffcc00;
        padding: 10px 0; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        font-family: Arial, sans-serif; font-weight: bold; font-size: 20px;
        text-transform: uppercase; display: flex; align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# KHẨU HIỆU
# ==============================================================================
danh_sach_khau_hieu = [
    "🚀 Việc hôm nay chớ để ngày mai - Hành động ngay!",
    "💪 Thái độ quyết định trình độ!",
    "🔥 Chủ động - Sáng tạo - Hiệu quả!",
    "⭐ Làm việc thông minh thay vì chỉ chăm chỉ!",
    "🤝 Đoàn kết là sức mạnh vô địch!",
]
try: cau_hom_nay = random.choice(danh_sach_khau_hieu)
except: cau_hom_nay = "Chúc bạn một ngày làm việc hiệu quả!"

st.markdown(f"""<div class="sticky-marquee"><marquee scrollamount="12">📢 THÔNG ĐIỆP: {cau_hom_nay} &nbsp;|&nbsp; 📢 HÃY CÙNG NHAU HOÀN THÀNH TỐT NHIỆM VỤ!</marquee></div>""", unsafe_allow_html=True)
st.title("🌐 Hệ Thống Quản Lý & Điều Hành")

# ==============================================================================
# HÀM ĐỌC DỮ LIỆU
# ==============================================================================
if st.button("🔄 Cập nhật dữ liệu"): st.cache_data.clear()

def load_data(link):
    try:
        if "?" in link: link = f"{link}&t={datetime.now().timestamp()}"
        else: link = f"{link}?t={datetime.now().timestamp()}"
        return pd.read_csv(link)
    except: return None

df_congviec = load_data(LINK_CSV_CONG_VIEC)

if df_congviec is None:
    st.error("⚠️ Chưa đọc được dữ liệu. Vui lòng kiểm tra kết nối.")
    st.stop()

# Chuẩn hóa cột
df_congviec.columns = df_congviec.columns.str.strip()
for col in df_congviec.columns:
    if "Chỉ" in col and "Đạo" in col: df_congviec.rename(columns={col: "Chỉ Đạo"}, inplace=True)
    if "Trạng" in col and "Thái" in col: df_congviec.rename(columns={col: "Trạng Thái"}, inplace=True)

# ==============================================================================
# TAB 1: DASHBOARD QUẢN LÝ
# ==============================================================================
tab1, tab2 = st.tabs(["📊 Dashboard Quản Lý", "📅 Lịch & Trực Ban"])

with tab1:
    df = df_congviec.copy()
    if "Hạn Chót" in df.columns: df["Hạn Chót"] = pd.to_datetime(df["Hạn Chót"], dayfirst=True, errors='coerce')
    df["Tiến Độ (%)"] = df["Tiến Độ (%)"].fillna(0)

    # --- BỘ LỌC ---
    c1, c2 = st.columns(2)
    tro_ly_col = "Tên Trợ Lý" if "Tên Trợ Lý" in df.columns else df.columns[0]
    with c1: selected_user = st.multiselect("Nhân sự:", df[tro_ly_col].unique(), default=df[tro_ly_col].unique())
    with c2: 
        status_list = df["Trạng Thái"].unique() if "Trạng Thái" in df.columns else []
        selected_status = st.multiselect("Trạng thái:", status_list, default=status_list)

    df_loc = df[df[tro_ly_col].isin(selected_user)].copy()
    if selected_status: df_loc = df_loc[df_loc["Trạng Thái"].isin(selected_status)]

    # --- KPI TỔNG QUAN ---
    if not df_loc.empty:
        k1, k2, k3, k4 = st.columns(4)
        now = datetime.now()
        tong = len(df_loc)
        xong = len(df_loc[df_loc["Trạng Thái"].str.contains("Hoàn", na=False)])
        tre = len(df_loc[(~df_loc["Trạng Thái"].str.contains("Hoàn", na=False)) & (df_loc["Hạn Chót"] < now)])
        
        k1.metric("Tổng việc", tong)
        k2.metric("Đã xong", xong)
        k3.metric("🚨 Quá hạn", tre)
        k4.metric("Hôm nay", now.strftime("%d/%m/%Y"))
        st.markdown("---")

        # --- 🟢 PHẦN ĐÃ KHÔI PHỤC: BẢNG TỶ TRỌNG & HIỆU SUẤT ---
        st.subheader("📊 Phân tích hiệu suất nhân sự")
        if tro_ly_col in df_loc.columns and "Trạng Thái" in df_loc.columns:
            # Tính toán thống kê
            analysis = df_loc.groupby(tro_ly_col).agg(
                Tong_Viec=("Trạng Thái", "count"),
                Viec_Da_Xong=("Trạng Thái", lambda x: x.str.contains("Hoàn", na=False).sum()),
                Tien_Do_TB=("Tiến Độ (%)", "mean")
            ).reset_index()
            
            # Tính phần trăm
            total_jobs = analysis["Tong_Viec"].sum()
            analysis["Ty_Trong"] = (analysis["Tong_Viec"] / total_jobs * 100) if total_jobs > 0 else 0
            analysis["Ty_Le_HT_That"] = (analysis["Viec_Da_Xong"] / analysis["Tong_Viec"] * 100)
            
            # Hiển thị bảng có biểu đồ thanh
            st.dataframe(
                analysis,
                use_container_width=True,
                column_config={
                    tro_ly_col: st.column_config.TextColumn("Nhân Sự"),
                    "Tong_Viec": st.column_config.NumberColumn("Tổng Việc"),
                    "Viec_Da_Xong": st.column_config.NumberColumn("Đã Xong"),
                    "Ty_Trong": st.column_config.ProgressColumn("Tỷ Trọng (%)", format="%.1f%%", min_value=0, max_value=100),
                    "Ty_Le_HT_That": st.column_config.ProgressColumn("Tỷ Lệ HT (%)", format="%.1f%%", min_value=0, max_value=100),
                    "Tien_Do_TB": st.column_config.NumberColumn("Tiến Độ TB", format="%.1f%%")
                },
                hide_index=True
            )
        st.markdown("---")

    # --- DANH SÁCH CHI TIẾT ---
    st.subheader("📋 Danh sách công việc chi tiết")
    hien_thi_xong = st.checkbox("✅ Hiển thị việc đã xong", value=False)
    
    if "Trạng Thái" in df_loc.columns:
        df_display = df_loc.copy()
        def xu_ly_row(row):
            tt = str(row["Trạng Thái"])
            hc = row.get("Hạn Chót", pd.NaT)
            sort = 2
            if 'Hoàn' in tt: sort = 1 
            elif pd.notna(hc):
                ngay_con = (hc - now).days
                if hc < now: tt = f"{tt} (Trễ {(now-hc).days} ngày)"; sort = 4
                elif 0 <= ngay_con <= 3: tt = f"{tt} (🔥 Gấp: Còn {ngay_con} ngày)"; sort = 3
            elif 'Chậm' in tt: sort = 4
            return tt, sort

        df_display[['Trạng Thái Hiển Thị', 'Sort_Order']] = df_display.apply(lambda x: pd.Series(xu_ly_row(x)), axis=1)
        df_display["Trạng Thái"] = df_display["Trạng Thái Hiển Thị"]
        
        if not hien_thi_xong: df_display = df_display[df_display['Sort_Order'] != 1]
        
        cols_sort = ["Sort_Order", "Hạn Chót"] if "Hạn Chót" in df_display.columns else ["Sort_Order"]
        df_display = df_display.sort_values(by=cols_sort, ascending=[False, True])

        cols_show = ["Tên Trợ Lý", "Nhiệm Vụ", "Chỉ Đạo", "Trạng Thái", "Tiến Độ (%)", "Hạn Chót", "Sort_Order"]
        final_cols = [c for c in cols_show if c in df_display.columns]

        def to_mau(row):
            s = row.get("Sort_Order", 2)
            if s == 1: return ['background-color: #28a745; color: white'] * len(row)
            if s == 4: return ['background-color: #ff4b4b; color: white; font-weight: bold'] * len(row)
            if s == 3: return ['background-color: #ff8c00; color: white; font-weight: bold'] * len(row)
            return ['background-color: #ffd700; color: black'] * len(row)

        h_table = (len(df_display) + 1) * 35 + 3 if len(df_display) > 0 else 150
        st.dataframe(
            df_display[final_cols].style.apply(to_mau, axis=1),
            use_container_width=True, height=h_table if h_table > 150 else 150,
            column_config={
                "Hạn Chót": st.column_config.DateColumn("Hạn Chót", format="DD/MM/YYYY"),
                "Tiến Độ (%)": st.column_config.NumberColumn("Tiến Độ", format="%.0f%%"),
                "Sort_Order": None
            }
        )

# ==============================================================================
# TAB 2: LỊCH GOOGLE CALENDAR & TRỰC BAN
# ==============================================================================
with tab2:
    # --- PHẦN 1: THANH HIỂN THỊ TRỰC BAN ---
    lich_truc = {0: "TUYỂN", 1: "THIẾT", 2: "ĐẠI", 3: "ĐÔNG", 4: "DIỆN", 5: "NGHỈ", 6: "NGHỈ"}
    thu_hom_nay = datetime.now().weekday()
    
    html_truc_ban = """
    <div style="background-color: #e6f4ea; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #34a853; text-align: center; color: #0d652d; font-family: Arial;">
        <span style="font-weight: bold; font-size: 18px;">👮 LỊCH TRỰC BAN HUẤN LUYỆN:</span><br><br>
    """
    for i in range(5):
        ten_thu = f"Thứ {i+2}"
        nguoi_truc = lich_truc[i]
        if i == thu_hom_nay:
            html_truc_ban += f"<span style='color: #d93025; font-weight: 900; font-size: 18px; border: 2px solid #d93025; padding: 3px 8px; border-radius: 5px;'>{ten_thu}: {nguoi_truc} (Hôm nay)</span> &nbsp;&nbsp;|&nbsp;&nbsp; "
        else:
            html_truc_ban += f"<span>{ten_thu}: <b>{nguoi_truc}</b></span> &nbsp;&nbsp;|&nbsp;&nbsp; "
    html_truc_ban += "</div>"
    st.markdown(html_truc_ban, unsafe_allow_html=True)

    # --- PHẦN 2: LỊCH GOOGLE ---
    if "http" in LINK_GOOGLE_CALENDAR:
        link_final = LINK_GOOGLE_CALENDAR.replace("mode=WEEK", "").replace("mode=MONTH", "")
        if "?" in link_final: link_final += "&mode=AGENDA"
        else: link_final += "?mode=AGENDA"
        st.markdown(f'<iframe src="{link_final}" style="border: 0" width="100%" height="800" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)
    else:
        st.info("⚠️ Chưa có link Google Calendar.")
