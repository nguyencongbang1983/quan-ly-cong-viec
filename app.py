import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================================================================
# 🔴 CẤU HÌNH LINK DỮ LIỆU (BẠN HÃY DÁN LẠI LINK CỦA BẠN VÀO ĐÂY)
# ==============================================================================

# 1. Dán Link CSV của Sheet "CongViec" vào đây:
LINK_CSV_CONG_VIEC = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQGBFEMqSqVkBhaym0YZilrmjtYlyN-F4qv5ypElMQyf-YPFxcXmAE_pBpWY4gg7y43H7HT9FT0JgpM/pub?gid=0&single=true&output=csv"

# 2. Dán Link CSV của Sheet "LichTuan" vào đây:
LINK_CSV_LICH_TUAN = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQGBFEMqSqVkBhaym0YZilrmjtYlyN-F4qv5ypElMQyf-YPFxcXmAE_pBpWY4gg7y43H7HT9FT0JgpM/pub?gid=689380875&single=true&output=csv"

# ==============================================================================
# CẤU HÌNH GIAO DIỆN & HÀM ĐỌC
# ==============================================================================
st.set_page_config(page_title="Hệ Thống Quản Lý Online", layout="wide", page_icon="🌐")

# CSS Tùy chỉnh
st.markdown("""
<style>
    div[data-testid="stMetric"] { background-color: #262730; border: 1px solid #4f4f4f; padding: 10px; border-radius: 5px; }
    h1 { text-align: center; color: #4da6ff; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    div[data-testid="stDataFrame"] { font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.title("🌐 Hệ Thống Quản Lý & Điều Hành (Online)")

# Hàm đọc dữ liệu trực tiếp từ Link CSV
@st.cache_data(ttl=60)
def load_data_direct(link):
    try:
        if "google.com" not in link: return None
        return pd.read_csv(link)
    except: return None

# Tải dữ liệu
df_congviec = load_data_direct(LINK_CSV_CONG_VIEC)
df_lich = load_data_direct(LINK_CSV_LICH_TUAN)

# Kiểm tra lỗi
if df_congviec is None or df_lich is None:
    st.error("⚠️ Chưa đọc được dữ liệu! Hãy chắc chắn bạn đã dán đúng Link CSV từ bước 'Publish to web' vào code.")
    st.stop()

# TẠO 2 TAB
tab1, tab2 = st.tabs(["📊 Dashboard Quản Lý", "📅 Lịch Công Tác Tuần"])

# ==============================================================================
# TAB 1: DASHBOARD
# ==============================================================================
with tab1:
    df = df_congviec.copy()
    df.columns = df.columns.str.strip().str.title()
    if "Trạng Thải" in df.columns: df.rename(columns={"Trạng Thải": "Trạng Thái"}, inplace=True)
    
    df["Hạn Chót"] = pd.to_datetime(df["Hạn Chót"], dayfirst=True, errors='coerce')
    df["Tiến Độ (%)"] = df["Tiến Độ (%)"].fillna(0)

    # Bộ lọc
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        ds_tro_ly = df["Tên Trợ Lý"].unique() if "Tên Trợ Lý" in df.columns else []
        selected_tro_ly = st.multiselect("Nhân sự:", ds_tro_ly, default=ds_tro_ly)
    with col_f2:
        ds_trang_thai = df["Trạng Thái"].unique() if "Trạng Thái" in df.columns else []
        selected_trang_thai = st.multiselect("Trạng thái:", ds_trang_thai, default=ds_trang_thai)

    if not df.empty:
        df_selection = df.query("`Tên Trợ Lý` == @selected_tro_ly & `Trạng Thái` == @selected_trang_thai").copy()

        # KPI
        c1, c2, c3, c4 = st.columns(4)
        now = datetime.now()
        viec_qua_han = len(df_selection[(~df_selection["Trạng Thái"].str.contains("Hoàn", na=False)) & (df_selection["Hạn Chót"] < now)])
        c1.metric("Tổng việc", len(df_selection))
        c2.metric("Đã xong", len(df_selection[df_selection["Trạng Thái"].str.contains("Hoàn", na=False)]))
        c3.metric("🚨 Quá hạn", viec_qua_han)
        c4.metric("Ngày báo cáo", now.strftime("%d/%m/%Y"))

        st.markdown("---")
        
        # Bảng phân tích
        if "Tên Trợ Lý" in df_selection.columns:
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

        # --------------------------------------------------------------------------
        # DANH SÁCH CHI TIẾT (LOGIC MỚI: XỬ LÝ NGÀY TRỄ + SẮP XẾP)
        # --------------------------------------------------------------------------
        st.subheader("📋 Danh sách công việc")
        
        # 1. Hàm XỬ LÝ DỮ LIỆU: Tính ngày trễ và gán số thứ tự
        # Sort Order: 1 = Hoàn thành, 2 = Đang làm, 3 = Quá hạn (Theo ý bạn)
        def xu_ly_trang_thai_va_sap_xep(row):
            trang_thai = str(row["Trạng Thái"])
            han_chot = row["Hạn Chót"]
            
            # --- TRƯỜNG HỢP 1: HOÀN THÀNH (LÊN ĐẦU) ---
            if 'Hoàn' in trang_thai:
                return trang_thai, 1 # Sort = 1
            
            # --- TRƯỜNG HỢP 2: QUÁ HẠN (XUỐNG CUỐI + TÍNH NGÀY) ---
            # Kiểm tra nếu có ngày hạn và ngày hạn nhỏ hơn hôm nay
            if pd.notna(han_chot) and han_chot < now:
                so_ngay_tre = (now - han_chot).days
                if so_ngay_tre > 0:
                    # Thêm dòng chữ cảnh báo vào trạng thái
                    new_status = f"{trang_thai} ⚠️ (Trễ {so_ngay_tre} ngày)"
                    return new_status, 3 # Sort = 3 (Xuống đáy)
            
            # Nếu đã có chữ "Chậm" trong file Excel sẵn rồi thì cũng đẩy xuống
            if 'Chậm' in trang_thai or 'Trễ' in trang_thai:
                 return trang_thai, 3

            # --- TRƯỜNG HỢP 3: ĐANG LÀM (Ở GIỮA) ---
            return trang_thai, 2 # Sort = 2

        # 2. Áp dụng hàm vào dữ liệu
        # Tạo 2 cột tạm: 'Trạng Thái Hiển Thị' và 'Sort_Order'
        df_selection[['Trạng Thái Hiển Thị', 'Sort_Order']] = df_selection.apply(
            lambda row: pd.Series(xu_ly_trang_thai_va_sap_xep(row)), axis=1
        )
        
        # 3. Sắp xếp: Theo Sort_Order (1->2->3) rồi đến Ngày hạn
        df_display = df_selection.sort_values(by=["Sort_Order", "Hạn Chót"], ascending=[True, True])

        # 4. HÀM TÔ MÀU (Dựa trên cột Sort_Order đã tính)
        def style_rows(row):
            uu_tien = row["Sort_Order"]
            
            if uu_tien == 1: # Hoàn thành
                return ['background-color: #28a745; color: white'] * len(row) # Xanh lá
            elif uu_tien == 2: # Đang làm
                return ['background-color: #ffa421; color: black'] * len(row) # Vàng cam
            else: # Quá hạn (uu_tien == 3)
                return ['background-color: #ff4b4b; color: white; font-weight: bold'] * len(row) # Đỏ rực

        # 5. Hiển thị
        if "Hạn Chót" in df_display.columns:
            # Thay cột Trạng thái gốc bằng cột đã thêm chữ "Trễ X ngày"
            df_final = df_display.drop(columns=["Trạng Thái", "Sort_Order"]).rename(columns={"Trạng Thái Hiển Thị": "Trạng Thái"})
            
            # Đưa cột Trạng Thái về vị trí cũ (hoặc để cuối tùy pandas, ở đây ta hiển thị theo column_config)
            cols = ["Tên Trợ Lý", "Nhiệm Vụ", "Trạng Thái", "Tiến Độ (%)", "Chất Lượng (1-10)", "Hạn Chót"]
            # Chỉ lấy các cột có trong dữ liệu thực tế
            cols = [c for c in cols if c in df_final.columns]
            
            st.dataframe(
                df_final[cols].style.apply(style_rows, axis=1),
                use_container_width=True, height=600,
                column_config={
                    "Hạn Chót": st.column_config.DateColumn("Hạn Chót", format="DD/MM/YYYY"),
                    "Trạng Thái": st.column_config.TextColumn("Trạng Thái", width="large"), # Cột này sẽ dài hơn vì có thêm chữ "Trễ X ngày"
                }
            )

# ==============================================================================
# TAB 2: LỊCH CÔNG TÁC TUẦN
# ==============================================================================
with tab2:
    tong_so_viec = len(df_lich)
    if tong_so_viec <= 10: font_size = "16px"; padding = "1rem"
    elif tong_so_viec <= 20: font_size = "14px"; padding = "0.5rem"
    else: font_size = "12px"; padding = "0.2rem"

    st.markdown(f"""<style>div[data-testid="stDataFrame"] {{ font-size: {font_size} !important; }} td {{ padding-top: {padding} !important; padding-bottom: {padding} !important; line-height: 1.2 !important; }}</style>""", unsafe_allow_html=True)

    def chinh_sua_gio(val): return str(val).replace("nan","")
    if "Thời Gian" in df_lich.columns: df_lich["Thời Gian"] = df_lich["Thời Gian"].apply(chinh_sua_gio)
    df_lich = df_lich.fillna("")

    st.info("💡 Lưu ý: Cập nhật Trực chỉ huy trong Google Sheet.")
    
    if not df_lich.empty:
        cac_ngay = df_lich["Thứ Ngày"].unique()
        for ngay in cac_ngay:
            cong_viec_ngay = df_lich[df_lich["Thứ Ngày"] == ngay]
            with st.container():
                st.markdown(f"<div style='background-color: #ff9f1c; padding: 2px 10px; font-weight: bold; margin-top: 5px; font-size: {font_size};'>📅 {ngay}</div>", unsafe_allow_html=True)
                st.dataframe(
                    cong_viec_ngay,
                    use_container_width=True, hide_index=True,
                    column_config={
                        "Trực Ban": st.column_config.TextColumn("Trực Ban", width="small"),
                        "Thời Gian": st.column_config.TextColumn("Giờ", width="small"),
                        "Nội Dung": st.column_config.TextColumn("Nội Dung", width="medium"),
                        "TTHV": st.column_config.TextColumn("TTHV", width="small"),
                        "TT Phòng": st.column_config.TextColumn("TT Phòng", width="small"),
                        "Chỉ huy Ban": st.column_config.TextColumn("CH Ban", width="small"),
                        "Lực lượng tham gia": st.column_config.TextColumn("LL Tham Gia", width="small"),
                        "Lực lượng phối hợp": st.column_config.TextColumn("LL Phối Hợp", width="small"),
                        "Địa Điểm": st.column_config.TextColumn("Đ.Điểm", width="small"),
                    }
                )
    else:
        st.info("Chưa có dữ liệu lịch tuần.")
