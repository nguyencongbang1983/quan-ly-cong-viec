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
        animation: scroll-left 25s linear infinite;
    }
    @keyframes scroll-left {
        0% { transform: translateX(0%); }
        100% { transform: translateX(-100%); }
    }

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

try:
    gio_hien_tai = datetime.now().hour
    chi_so_kh = (gio_hien_tai // 2) % len(danh_sach_khau_hieu)
    cau_hom_nay = danh_sach_khau_hieu[chi_so_kh]
except:
    cau_hom_nay = "Chúc bạn một ngày làm việc hiệu quả!"

st.markdown(f"""
    <div class="sticky-marquee-container">
        <div class="scroll-text">
            📢 THÔNG ĐIỆP: {cau_hom_nay} &nbsp;&nbsp;|&nbsp;&nbsp; 📢 HÃY CÙNG NHAU HOÀN THÀNH TỐT NHIỆM VỤ!
        </div>
    </div>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 11])
with col_logo:
    try:
        st.image("logo.jpg", use_container_width=True)
    except:
        st.error("⚠️ Không tìm thấy logo.jpg")

with col_title:
    st.title("🌐 Hệ Thống Quản Lý & Điều Hành")

# ==============================================================================
# HÀM ĐỌC DỮ LIỆU
# ==============================================================================
if st.button("🔄 Cập nhật dữ liệu"):
    st.cache_data.clear()

def load_data(link):
    try:
        sep = "&" if "?" in link else "?"
        link = f"{link}{sep}t={datetime.now().timestamp()}"
        return pd.read_csv(link)
    except:
        return None

df_congviec = load_data(LINK_CSV_CONG_VIEC)

if df_congviec is None:
    st.error("⚠️ Chưa đọc được dữ liệu. Vui lòng kiểm tra kết nối.")
    st.stop()

df_congviec.columns = df_congviec.columns.str.strip()
for col in df_congviec.columns:
    if "Chỉ" in col and "Đạo" in col:
        df_congviec.rename(columns={col: "Chỉ Đạo"}, inplace=True)
    if "Trạng" in col and "Thái" in col:
        df_congviec.rename(columns={col: "Trạng Thái"}, inplace=True)

# ==============================================================================
# 🔑 HÀM TÍNH NGÀY CÒN LẠI (dùng chung toàn app)
# ==============================================================================
def tinh_ngay_con_lai(han_chot, now):
    """
    Trả về (số nguyên ngày, chuỗi hiển thị)
    - Dương: còn X ngày
    - 0    : hôm nay
    - Âm   : đã trễ
    - None : không có hạn chót
    """
    if pd.isna(han_chot):
        return None, ""
    
    han = pd.Timestamp(han_chot).normalize()
    hom_nay = pd.Timestamp(now).normalize()
    so_ngay = (han - hom_nay).days

    if so_ngay > 1:
        chu = f"{so_ngay} ngày"
    elif so_ngay == 1:
        chu = "⚠️ Còn 1 ngày!"
    elif so_ngay == 0:
        chu = "⚠️ Hôm nay!"
    else:
        chu = f"🔴 Trễ {abs(so_ngay)} ngày"

    return so_ngay, chu

# ==============================================================================
# TAB 1: DASHBOARD QUẢN LÝ
# ==============================================================================
tab1, tab2 = st.tabs(["📊 Dashboard Quản Lý", "📅 Lịch & Trực Ban"])

with tab1:
    df = df_congviec.copy()
    now = datetime.now()

    if "Hạn Chót" in df.columns:
        df["Hạn Chót"] = pd.to_datetime(df["Hạn Chót"], dayfirst=True, errors='coerce')

    # ✅ Tính cột "Ngày Còn Lại" realtime thay thế "Tiến Độ (%)"
    if "Hạn Chót" in df.columns:
        df[["_so_ngay", "Ngày Còn Lại"]] = df["Hạn Chót"].apply(
            lambda x: pd.Series(tinh_ngay_con_lai(x, now))
        )
    else:
        df["_so_ngay"] = None
        df["Ngày Còn Lại"] = ""

    # --- BỘ LỌC ---
    c1, c2 = st.columns(2)
    tro_ly_col = "Tên Trợ Lý" if "Tên Trợ Lý" in df.columns else df.columns[0]
    with c1:
        selected_user = st.multiselect("Nhân sự:", df[tro_ly_col].unique(), default=df[tro_ly_col].unique())
    with c2:
        status_list = df["Trạng Thái"].unique() if "Trạng Thái" in df.columns else []
        selected_status = st.multiselect("Trạng thái:", status_list, default=status_list)

    df_loc = df[df[tro_ly_col].isin(selected_user)].copy()
    if selected_status:
        df_loc = df_loc[df_loc["Trạng Thái"].isin(selected_status)]

    # --- KPI TỔNG QUAN ---
    if not df_loc.empty:
        k1, k2, k3, k4 = st.columns(4)
        tong = len(df_loc)
        xong = len(df_loc[df_loc["Trạng Thái"].str.contains("Hoàn", na=False)])
        tre  = len(df_loc[
            (~df_loc["Trạng Thái"].str.contains("Hoàn", na=False)) &
            (df_loc["Hạn Chót"] < now)
        ]) if "Hạn Chót" in df_loc.columns else 0

        k1.metric("Tổng việc", tong)
        k2.metric("Đã xong", xong)
        k3.metric("🚨 Quá hạn", tre)
        k4.metric("Hôm nay", now.strftime("%d/%m/%Y"))
        st.markdown("---")

        # --- BẢNG PHÂN TÍCH HIỆU SUẤT NHÂN SỰ ---
        st.subheader("📊 Phân tích hiệu suất nhân sự")
        if tro_ly_col in df_loc.columns and "Trạng Thái" in df_loc.columns:

            def phan_tich_nhom(grp):
                tong_viec  = len(grp)
                da_xong    = grp["Trạng Thái"].str.contains("Hoàn", na=False).sum()
                viec_con    = grp[~grp["Trạng Thái"].str.contains("Hoàn", na=False)]
                # Ngày còn lại trung bình (chỉ tính việc chưa xong, có hạn chót)
                so_ngay_hd = viec_con["_so_ngay"].dropna()
                ncl_tb = so_ngay_hd.mean() if len(so_ngay_hd) > 0 else None
                return pd.Series({
                    "Tong_Viec"  : tong_viec,
                    "Viec_Da_Xong": da_xong,
                    "NCL_TB"     : ncl_tb          # Ngày còn lại trung bình
                })

            analysis = df_loc.groupby(tro_ly_col).apply(phan_tich_nhom).reset_index()
            total_jobs = analysis["Tong_Viec"].sum()
            analysis["Ty_Trong"] = (analysis["Tong_Viec"] / total_jobs * 100) if total_jobs > 0 else 0
            analysis["Ty_Le_HT"] = (analysis["Viec_Da_Xong"] / analysis["Tong_Viec"] * 100)

            # Nhãn NCL_TB dễ đọc
            def nhan_ncl(val):
                if pd.isna(val): return "—"
                val = int(round(val))
                if val > 0:   return f"{val} ngày"
                elif val == 0: return "⚠️ Hôm nay"
                else:          return f"🔴 Trễ {abs(val)} ngày"

            analysis["NCL_TB_Label"] = analysis["NCL_TB"].apply(nhan_ncl)

            st.dataframe(
                analysis,
                use_container_width=True,
                column_config={
                    tro_ly_col       : st.column_config.TextColumn("Nhân Sự"),
                    "Tong_Viec"      : st.column_config.NumberColumn("Tổng Việc"),
                    "Viec_Da_Xong"   : st.column_config.NumberColumn("Đã Xong"),
                    "Ty_Trong"       : st.column_config.ProgressColumn("Tỷ Trọng (%)", format="%.1f%%", min_value=0, max_value=100),
                    "Ty_Le_HT"       : st.column_config.ProgressColumn("Tỷ Lệ HT (%)", format="%.1f%%", min_value=0, max_value=100),
                    "NCL_TB"         : None,                                            # Ẩn cột số thô
                    "NCL_TB_Label"   : st.column_config.TextColumn("⏳ Ngày CL Trung Bình"),
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
            tt   = str(row["Trạng Thái"])
            hc   = row.get("Hạn Chót", pd.NaT)
            sort = 2
            if "Hoàn" in tt:
                sort = 1
            elif pd.notna(hc):
                so_ngay = (pd.Timestamp(hc).normalize() - pd.Timestamp(now).normalize()).days
                if so_ngay < 0:
                    tt   = f"{tt} (Trễ {abs(so_ngay)} ngày)"
                    sort = 4
                elif so_ngay <= 3:
                    tt   = f"{tt} (🔥 Gấp: Còn {so_ngay} ngày)"
                    sort = 3
            elif "Chậm" in tt:
                sort = 4
            return tt, sort

        df_display[["Trạng Thái Hiển Thị", "Sort_Order"]] = df_display.apply(
            lambda x: pd.Series(xu_ly_row(x)), axis=1
        )
        df_display["Trạng Thái"] = df_display["Trạng Thái Hiển Thị"]

        if not hien_thi_xong:
            df_display = df_display[df_display["Sort_Order"] != 1]

        cols_sort = ["Sort_Order", "Hạn Chót"] if "Hạn Chót" in df_display.columns else ["Sort_Order"]
        df_display = df_display.sort_values(by=cols_sort, ascending=[False, True])

        # ✅ Cột hiển thị: thay "Tiến Độ (%)" bằng "Ngày Còn Lại"
        cols_show = ["Tên Trợ Lý", "Nhiệm Vụ", "Chỉ Đạo", "Trạng Thái", "Ngày Còn Lại", "Hạn Chót", "Sort_Order"]
        final_cols = [c for c in cols_show if c in df_display.columns]

        def to_mau(row):
            s = row.get("Sort_Order", 2)
            if s == 1: return ["background-color: #28a745; color: white"] * len(row)
            if s == 4: return ["background-color: #ff4b4b; color: white; font-weight: bold"] * len(row)
            if s == 3: return ["background-color: #ff8c00; color: white; font-weight: bold"] * len(row)
            return ["background-color: #ffd700; color: black"] * len(row)

        h_table = (len(df_display) + 1) * 35 + 3 if len(df_display) > 0 else 150
        st.dataframe(
            df_display[final_cols].style.apply(to_mau, axis=1),
            use_container_width=True,
            height=max(h_table, 150),
            column_config={
                "Hạn Chót"     : st.column_config.DateColumn("Hạn Chót", format="DD/MM/YYYY"),
                "Ngày Còn Lại" : st.column_config.TextColumn("⏳ Ngày Còn Lại"),
                "Sort_Order"   : None
            }
        )

# ==============================================================================
# TAB 2: LỊCH GOOGLE CALENDAR & TRỰC BAN
# ==============================================================================
with tab2:
    TRUC_CHI_HUY_HV       = "Thiếu tướng Hoàng Văn Phai"
    TRUC_CHI_HUY_PHONG    = "Đại tá Đỗ Huy Hà"
    TRUC_CHUYEN_MON_CUOI_TUAN = "Đại"

    LICH_TRUC_NGAY_THUONG = {
        0: "Thiết",
        1: "Diện",
        2: "Đông",
        3: "Hà",
        4: "Đại"
    }

    thu_hom_nay  = datetime.now().weekday()
    html_content = '<div class="duty-box">'

    html_content += '<div class="duty-row">'
    html_content += f'<div class="duty-col-half">🎖️ <b>TRỰC CHỈ HUY HV:</b> {TRUC_CHI_HUY_HV}</div>'
    html_content += f'<div class="duty-col-half">🎖️ <b>TRỰC CHỈ HUY PHÒNG:</b> {TRUC_CHI_HUY_PHONG}</div>'
    html_content += '</div>'
    html_content += '<div class="separator"></div>'

    html_content += '<div class="duty-row">'
    html_content += '<div class="duty-col-left">'
    html_content += '<span class="duty-title">👮 TRỰC BAN HUẤN LUYỆN:</span>'
    for i in range(5):
        ten_thu     = f"Thứ {i+2}"
        nguoi_truc  = LICH_TRUC_NGAY_THUONG[i]
        if i == thu_hom_nay:
            html_content += f'<span class="highlight-today">{ten_thu}: {nguoi_truc}</span> &nbsp; '
        else:
            html_content += f'<span class="normal-day">{ten_thu}: {nguoi_truc}</span> &nbsp;|&nbsp; '
    html_content += '</div>'

    html_content += '<div class="duty-col-right">'
    html_content += '<span class="duty-title">🛠️ TRỰC CHUYÊN MÔN:</span>'
    is_truc_cm_today = (thu_hom_nay >= 5)
    style_cm = 'class="highlight-today"' if is_truc_cm_today else 'class="normal-day"'
    html_content += f'<span {style_cm}>T7, CN: {TRUC_CHUYEN_MON_CUOI_TUAN}</span>'
    html_content += '</div>'

    html_content += '</div></div>'
    st.markdown(html_content, unsafe_allow_html=True)

    if "http" in LINK_GOOGLE_CALENDAR:
        link_final = LINK_GOOGLE_CALENDAR.replace("mode=AGENDA", "").replace("mode=MONTH", "")
        sep = "&" if "?" in link_final else "?"
        link_final += f"{sep}mode=WEEK"
        st.markdown(f"""
            <div style="width: 100%; height: 1000px; overflow: hidden;">
                <iframe src="{link_final}" style="border: 0; width: 100%; height: 1200px; transform: scale(1.0); transform-origin: 0 0;" frameborder="0" scrolling="yes"></iframe>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("⚠️ Chưa có link Google Calendar.")
