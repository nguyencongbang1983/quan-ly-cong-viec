# ... (giữ nguyên logic CSS phía trên) ...

# ==============================================================================
# KHẨU HIỆU & LOGO [CẬP NHẬT MỚI]
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

# [MỚI BỔ SUNG] - Thuật toán đổi khẩu hiệu theo khung 2 tiếng (0-2h, 2-4h, ...)
gio_hien_tai = datetime.now().hour
# Dùng phép chia lấy nguyên (// 2) để nhóm 2 tiếng thành 1 mốc, sau đó lấy dư (%) cho tổng số câu
chi_so_kh = (gio_hien_tai // 2) % len(danh_sach_khau_hieu)
cau_hom_nay = danh_sach_khau_hieu[chi_so_kh]

st.markdown(f"""<div class="sticky-marquee"><marquee scrollamount="12">📢 THÔNG ĐIỆP: {cau_hom_nay} &nbsp;|&nbsp; 📢 HÃY CÙNG NHAU HOÀN THÀNH TỐT NHIỆM VỤ!</marquee></div>""", unsafe_allow_html=True)

# [MỚI BỔ SUNG] - Cấu trúc cột chèn Logo cạnh Tiêu đề
col_logo, col_title = st.columns([1, 11])
with col_logo:
    try:
        # Tải logo từ file ảnh.jpg (đảm bảo file nằm cùng cấp thư mục với app.py)
        st.image("ảnh.jpg", use_container_width=True)
    except Exception as e:
        st.error("⚠️ Thiếu logo") # Báo lỗi nhỏ nếu không tìm thấy file ảnh

with col_title:
    st.title("🌐 Hệ Thống Quản Lý & Điều Hành")

# ==============================================================================
# HÀM ĐỌC DỮ LIỆU
# ==============================================================================
# ... (giữ nguyên logic phía dưới) ...
