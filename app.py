import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ==============================================================================
# 🔴 CẤU HÌNH DỮ LIỆU
# ==============================================================================
LINK_CSV_CONG_VIEC = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSRoKMQ8kMQ4WKjSvfUqwCi5MhX_NYM1r_C7mqmg8gKSWwVSt_FJPN81FClnnrkzUveirIBDKT9YACw/pub?gid=2034795073&single=true&output=csv"
LINK_GOOGLE_CALENDAR = "https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=Asia%2FHo_Chi_Minh&mode=WEEK&src=YmFua2Vob2FjaHA1QGdtYWlsLmNvbQ&src=YTQzMjk4OGM4YzA0ZGVmYzRlNzU1MTAwYjFjOGNhNjdiMjU1YThjY2FiYzQ1Mzg1ZGEwYzIwMWU1MGVkYjRlZEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t&src=ZW4udmlldG5hbWVzZSNob2xpZGF5QGdyb3VwLnYuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&src=dmkudmlldG5hbWVzZSNob2xpZGF5QGdyb3VwLnYuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23039be5&color=%23ef6c00&color=%230b8043&color=%230b8043"

# ==============================================================================
# CẤU HÌNH GIAO DIỆN & CSS
# ==============================================================================
st.set_page_config(page_title="Hệ Thống Quản Lý", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    .block-container {
        padding-top: 5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    [data-testid="stDataFrame"] button[title="View fullscreen"] { display: none !important; }
    div[data-testid="stMetric"] { background-color: #262730; border: 1px solid #4f4f4f; padding: 10px; border-radius: 5px; }
    h1 { text-align: center; color: #4da6ff; margin-bottom: 0rem; padding-bottom: 0rem; }
    div[data-testid="stDataFrame"] { font-size: 16px !important; }
    thead tr th:first-child {display:none}
    tbody th {display:none}
    header, footer, .stDeployButton {visibility: hidden; display:none;}

    /* Cập nhật CSS để chạy chữ mượt mà bằng Animation */
    .sticky-marquee-container {
        position: fixed; top: 0; left: 0; width: 100vw;
        background-color: #fff3cd; color: #856404;
        z-index: 2147483647; border-bottom: 3px solid #ffcc00;
        padding: 10px 0; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        font-family: Arial, sans-serif; font-weight: bold; font-size: 20px;
        text-transform: uppercase;
        overflow: hidden;
        white-space: nowrap;
        display: block;
    }
    .scroll-text {
        display: inline-block;
        padding-left: 100%;
        animation: scroll-left 25s linear infinite; /* Chỉnh 25s để tốc độ vừa phải */
    }
    @keyframes scroll-left {
        0% { transform: translateX(0%); }
        100% { transform: translateX(-100%); }
    }
    
    /* CSS Căn chỉnh Lịch Trực Ban (Hàng Ngang) */
    .duty-box {
        background-color: #e6f4ea; padding: 10px; border-radius: 8px; margin-bottom: 10px; 
        border: 1px solid #34a853; font-family: Arial; color: #0d652d;
    }
    .duty-row {
        display: flex; flex-wrap: wrap; width: 100%; align-items: flex-start;
    }
    .duty-col-half {
        flex: 1; min-width: 300px; padding: 5px 10px;
    }
    .duty-col-left {
        flex: 3; min-width: 400px; padding: 5px 10px; border-right: 1px dashed #34a853;
    }
    .duty-col-right {
        flex: 1; min-width: 200px; padding: 5px 10px;
    }
    .duty-title { font-weight: bold; font-size: 16px; color: #137333; text-transform: uppercase; display: block; margin-bottom: 5px;}
    .highlight-today { color: #d93025; font-weight: 900; font-size: 16px; border: 1px solid #d93025; padding: 1px 5px; border-radius: 4px; background-color: #fff; }
    .normal-day { font-weight: bold; color: #333; }
    .separator { border-bottom: 1px dashed #34a853; margin: 5px 0; width: 100%; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# KHẨU HIỆU & LOGO
# ==============================================================================
danh_sach_khau_hieu = [
    "🚀 Việc hôm nay chớ để ngày mai - Hành động ngay!",
    "💪 Thái độ quyết định trình độ!",
    "🔥 Chủ động - Sáng tạo - Hiệu quả!",
    "⭐ Làm việc thông minh thay vì chỉ chăm chỉ!",
    "🤝 Đoàn kết là sức mạnh vô địch!",
    "🤝 Nhiệt liệt chào mừng kỷ niệm 70 năm Ngày truyền thống Phòng Đào tạo (11/4/1956 - 11/4/2026)!!!",
    "🤝 Mỗi cán bộ Phòng Đào tạo là một tấm gương sáng về tinh thần tận tụy, chuyên nghiệp và cống hiến!",
    "🤝 Dấu ấn 70 năm: Nâng cao chất lượng đào tạo là mục tiêu, là động lực để phát triển bền vững!",
    "🤝 Ra sức thi đua lập thành tích xuất sắc chào mừng 70 năm Ngày truyền thống Phòng Đào tạo!",
    "🤝 Kỷ cương, Trách nhiệm, Sáng tạo, Hiệu quả – Xứng danh bề dày 70 năm truyền thống Phòng Đào tạo!"
]

# Thuật toán đổi khẩu hiệu theo khung 2 tiếng
try:
    gio_hien_tai = datetime.now().hour
    chi_so_kh = (gio_hien_tai // 2) % len(danh_sach_khau_hieu)
    cau_hom_nay = danh_sach_khau_hieu[chi_so_kh]
except Exception as e:
    cau_hom_nay = "Chúc bạn một ngày làm việc hiệu quả!"

# Hiển thị chữ chạy bằng công nghệ mới
st.markdown(f"""
    <div class="sticky-marquee-container">
        <div class="scroll-text">
            📢 THÔNG ĐIỆP: {cau_hom_nay} &nbsp;&nbsp;|&nbsp;&nbsp; 📢 HÃY CÙNG NHAU HOÀN THÀNH TỐT NHIỆM VỤ!
        </div>
    </div>
""", unsafe_allow_html=True)

# Cấu trúc cột chèn Logo cạnh Tiêu đề
col_logo, col_title = st.columns([1, 11])
with col_logo:
    try:
        # Tải logo chuẩn từ file đã up
        st.image("logo.jpg", use_container_width=True)
    except Exception:
        st.error("⚠️ Không tìm thấy logo.jpg")

with col_title:
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
    if "Tiến Độ (%)" in df.columns: df["Tiến Độ (%)"] = df["Tiến Độ (%)"].fillna(0)

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

        # --- BẢNG TỶ TRỌNG & HIỆU SUẤT ---
        st.subheader("📊 Phân tích hiệu suất nhân sự")
        if tro_ly_col in df_loc.columns and "Trạng Thái" in df_loc.columns:
            analysis = df_loc.groupby(tro_ly_col).agg(
                Tong_Viec=("Trạng Thái", "count"),
                Viec_Da_Xong=("Trạng Thái", lambda x: x.str.contains("Hoàn", na=False).sum())
            )
            if "Tiến Độ (%)" in df_loc.columns:
                tien_do_tb = df_loc.groupby(tro_ly_col)["Tiến Độ (%)"].mean()
                analysis = analysis.join(tien_do_tb).rename(columns={"Tiến Độ (%)": "Tien_Do_TB"})
            else:
                analysis["Tien_Do_TB"] = 0
            
            analysis = analysis.reset_index()
            total_jobs = analysis["Tong_Viec"].sum()
            analysis["Ty_Trong"] = (analysis["Tong_Viec"] / total_jobs * 100) if total_jobs > 0 else 0
            analysis["Ty_Le_HT_That"] = (analysis["Viec_Da_Xong"] / analysis["Tong_Viec"] * 100)
            
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
# TAB 2: LỊCH GOOGLE CALENDAR & TRỰC BAN (GIAO DIỆN MỚI 2 HÀNG)
# ==============================================================================
with tab2:
    # 🟢🟢🟢 KHU VỰC CHỈNH SỬA HÀNG TUẦN (BẠN SỬA TÊN Ở ĐÂY) 🟢🟢🟢
    TRUC_CHI_HUY_HV = "Thiếu tướng Vũ Đức Long"
    TRUC_CHI_HUY_PHONG = "Đại tá Đỗ Huy Hà"
    TRUC_CHUYEN_MON_CUOI_TUAN = "Diện"

    # Lịch trực ban ngày thường (Thứ 2 đến Thứ 6)
    LICH_TRUC_NGAY_THUONG = {
        0: "Tuyển",   # Thứ 2
        1: "Diện",  # Thứ 3
        2: "Thiết",   # Thứ 4
        3: "Hà",     # Thứ 5
        4: "Đông"     # Thứ 6
    }
    # ============================================================

    # --- XỬ LÝ HIỂN THỊ TRỰC BAN (LAYOUT 2 HÀNG NGANG) ---
    thu_hom_nay = datetime.now().weekday()
    
    html_content = '<div class="duty-box">'
    
    # HÀNG 1: TRỰC CHỈ HUY (Chia đôi màn hình)
    html_content += '<div class="duty-row">'
    html_content += f'<div class="duty-col-half">🎖️ <b>TRỰC CHỈ HUY HV:</b> {TRUC_CHI_HUY_HV}</div>'
    html_content += f'<div class="duty-col-half">🎖️ <b>TRỰC CHỈ HUY PHÒNG:</b> {TRUC_CHI_HUY_PHONG}</div>'
    html_content += '</div>'
    
    html_content += '<div class="separator"></div>'
    
    # HÀNG 2: TRỰC BAN HL & TRỰC CM (Chia lệch 70-30)
    html_content += '<div class="duty-row">'
    
    # Cột Trái: Trực ban Huấn luyện (T2-T6)
    html_content += '<div class="duty-col-left">'
    html_content += '<span class="duty-title">👮 TRỰC BAN HUẤN LUYỆN:</span>'
    for i in range(5):
        ten_thu = f"Thứ {i+2}"
        nguoi_truc = LICH_TRUC_NGAY_THUONG[i]
        if i == thu_hom_nay:
            html_content += f'<span class="highlight-today">{ten_thu}: {nguoi_truc}</span> &nbsp; '
        else:
            html_content += f'<span class="normal-day">{ten_thu}: {nguoi_truc}</span> &nbsp;|&nbsp; '
    html_content += '</div>'
    
    # Cột Phải: Trực Chuyên Môn (T7-CN)
    html_content += '<div class="duty-col-right">'
    html_content += f'<span class="duty-title">🛠️ TRỰC CHUYÊN MÔN:</span>'
    
    # Kiểm tra xem hôm nay có phải là ngày trực CM không
    is_truc_cm_today = (thu_hom_nay >= 5)
    style_cm = 'class="highlight-today"' if is_truc_cm_today else 'class="normal-day"'
    
    html_content += f'<span {style_cm}>T7, CN: {TRUC_CHUYEN_MON_CUOI_TUAN}</span>'
    html_content += '</div>'
    
    html_content += '</div></div>' # Đóng duty-row và duty-box
    
    st.markdown(html_content, unsafe_allow_html=True)

    # --- PHẦN 2: LỊCH GOOGLE (PHÓNG TO) ---
    if "http" in LINK_GOOGLE_CALENDAR:
        link_final = LINK_GOOGLE_CALENDAR.replace("mode=AGENDA", "").replace("mode=MONTH", "")
        if "?" in link_final: link_final += "&mode=WEEK"
        else: link_final += "?mode=WEEK"
        
        # Dùng kỹ thuật CSS transform scale để phóng to iframe lên 1.2 lần
        st.markdown(f"""
            <div style="width: 100%; height: 1000px; overflow: hidden;">
                <iframe src="{link_final}" style="border: 0; width: 100%; height: 1200px; transform: scale(1.0); transform-origin: 0 0;" frameborder="0" scrolling="yes"></iframe>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("⚠️ Chưa có link Google Calendar.")
