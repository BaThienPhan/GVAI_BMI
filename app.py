import streamlit as st
import pandas as pd
import numpy as np
import os
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Báo Cáo BMI & Ôn Tập",
                   page_icon="💪", layout="wide")

# --- BIẾN TOÀN CỤC VÀ TÊN FILE ---
DATA_FILE = "bmi_data.csv"
QUIZ_FILE = "quiz_results.csv"
# Tên file video khởi động (Thầy/cô đảm bảo file này nằm cùng thư mục với code)
INTRO_VIDEO = "Chỉ số BMI.mp4"

# Cấu hình cột
COLUMN_NAMES = [
    "Họ và tên", "Lớp", "Nhóm", "Chiều cao (m)",
    "Cân nặng (kg)", "Chỉ số BMI", "Kết luận", "Lời khuyên"
]
DISPLAY_COLUMNS = [
    "Họ và tên", "Lớp", "Nhóm", "Chiều cao (m)", "Cân nặng (kg)",
    "Chỉ số BMI", "BMI (Tự động tính)", "Kết luận", "Lời khuyên"
]
QUIZ_COLUMNS = ["Họ và tên", "Lớp", "Số câu đúng",
                "Tổng số câu", "Điểm số (Thang 10)", "Thời gian nộp"]

# --- DỮ LIỆU CÂU HỎI TRẮC NGHIỆM ---
QUIZ_DATA = [
    {
        "question": "BMI là viết tắt của thuật ngữ nào?",
        "options": ["Body Mass Index", "Body Muscle Index", "Basic Metabolic Indicator", "Bone Mass Indicator"],
        "answer": "Body Mass Index",
        "explanation": "BMI là chỉ số khối cơ thể (Body Mass Index)."
    },
    {
        "question": "Công thức tính BMI chuẩn là gì?",
        "options": ["Cân nặng / Chiều cao", "Cân nặng / (Chiều cao x 2)", "Cân nặng / (Chiều cao x Chiều cao)", "Chiều cao / Cân nặng"],
        "answer": "Cân nặng / (Chiều cao x Chiều cao)",
        "explanation": "Công thức: BMI = Cân nặng (kg) / [Chiều cao (m)]²"
    },
    {
        "question": "Theo thang đo WHO cho người châu Á, BMI từ 23 trở lên được xếp vào loại nào?",
        "options": ["Bình thường", "Thừa cân (Tiền béo phì)", "Thiếu cân", "Béo phì độ 2"],
        "answer": "Thừa cân (Tiền béo phì)",
        "explanation": "Với người châu Á, BMI >= 23 được coi là thừa cân."
    },
    {
        "question": "Chỉ số BMI KHÔNG phản ánh chính xác điều gì?",
        "options": ["Tình trạng dinh dưỡng chung", "Tỷ lệ mỡ và cơ trong cơ thể", "Mối liên quan với nguy cơ bệnh lý", "Sự cân đối giữa chiều cao và cân nặng"],
        "answer": "Tỷ lệ mỡ và cơ trong cơ thể",
        "explanation": "BMI không phân biệt được trọng lượng đó là mỡ hay cơ bắp (ví dụ vận động viên thể hình có BMI cao nhưng không béo)."
    },
    {
        "question": "Để duy trì BMI lý tưởng, biện pháp nào quan trọng nhất?",
        "options": ["Nhịn ăn hoàn toàn bữa tối", "Dinh dưỡng cân bằng và vận động hợp lý", "Chỉ uống nước ngọt thay nước lọc", "Ngủ 12 tiếng mỗi ngày"],
        "answer": "Dinh dưỡng cân bằng và vận động hợp lý",
        "explanation": "Sự cân bằng giữa năng lượng nạp vào và tiêu hao là chìa khóa."
    }
]

# --- HÀM KHỞI TẠO FILE ---


def initialize_files():
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=COLUMN_NAMES).to_csv(
            DATA_FILE, index=False, encoding='utf-8-sig')
    if not os.path.exists(QUIZ_FILE):
        pd.DataFrame(columns=QUIZ_COLUMNS).to_csv(
            QUIZ_FILE, index=False, encoding='utf-8-sig')


initialize_files()

# --- GIAO DIỆN CHÍNH ---
st.title("💪 Hệ Thống Học Tập & Đánh Giá BMI")
st.caption("Ứng dụng hỗ trợ thực hành tính toán và ôn tập kiến thức.")

st_autorefresh(interval=5000, key="data_refresh")

# TẠO 4 TAB (THÊM TAB KHỞI ĐỘNG)
tab_intro, tab1, tab2, tab3 = st.tabs(
    ["🎬 Khởi Động", "📝 Nhập Liệu Thực Hành", "📊 Bảng Báo Cáo Thực Hành", "📚 Ôn tập & Kiểm tra"])

# ==============================================================================
# TAB INTRO: KHỞI ĐỘNG BÀI HỌC
# ==============================================================================
with tab_intro:
    col_i1, col_i2 = st.columns([2, 1])
    with col_i1:
        st.header("🎬 Tình huống khởi động")
        st.info("Cùng xem thầy trò Đường Tăng gặp rắc rối gì về cân nặng nhé!")
        # Kiểm tra file video có tồn tại không
        st.video("https://youtu.be/0ICqUBIW3Rs")

    with col_i2:
        st.success("💡 Câu hỏi thảo luận:")
        st.write("""
        1. Trư Bát Giới đang lo lắng về điều gì?
        2. Đường Tăng đã nhắc đến chỉ số nào để đánh giá thể trạng?
        3. Vì sao chúng ta cần biết chỉ số BMI?
        """)
        st.write("---")
        st.markdown(
            "👉 **Hãy chuyển sang Tab 'Nhập Liệu Thực Hành' để bắt đầu tính toán nhé!**")

# ==============================================================================
# TAB 1: TRANG NHẬP LIỆU
# ==============================================================================
with tab1:
    st.header("📝 Biểu mẫu nhập thông tin thực hành")
    if "submitted_bmi" not in st.session_state:
        st.session_state.submitted_bmi = False

    if st.session_state.submitted_bmi:
        st.info("✅ Bạn đã gửi số liệu thực hành thành công.")
        if st.button("Nhập thêm người khác"):
            st.session_state.submitted_bmi = False
            st.rerun()
    else:
        with st.form(key="student_form"):
            col1, col2 = st.columns(2)
            with col1:
                ho_va_ten = st.text_input("Họ và tên")
            with col2:
                lop = st.text_input("Lớp")

            ten_nhom = st.selectbox("Chọn nhóm", [
                                    "Nhóm 1", "Nhóm 2", "Nhóm 3", "Nhóm 4", "Nhóm 5", "Nhóm 6 (Giáo viên)"], index=None)

            col3, col4 = st.columns(2)
            with col3:
                chieu_cao = st.number_input(
                    "Chiều cao (mét)", 0.0, 2.5, 0.0, format="%.2f", help="Nhập 0 nếu chưa đo")
            with col4:
                can_nang = st.number_input(
                    "Cân nặng (kg)", 0.0, 200.0, 0.0, format="%.1f")

            chi_so_bmi = st.number_input(
                "Nhập Chỉ số BMI (HS tự tính)", 0.0, 50.0, 0.0, format="%.2f")
            ket_luan = st.selectbox("Kết luận", ["BMI < 15: Gầy", "15 <= BMI < 22: Bình thường",
                                    "22 <= BMI < 25: Có nguy cơ béo phì", "BMI >= 25: Béo phì"], index=None)
            loi_khuyen = st.text_area("Nhập lời khuyên")

            submit_bmi = st.form_submit_button("Lưu kết quả thực hành")

        if submit_bmi:
            missing = []
            if not ho_va_ten.strip():
                missing.append("Họ và tên")
            if not lop.strip():
                missing.append("Lớp")
            if not ten_nhom:
                missing.append("Nhóm")
            if chieu_cao <= 0:
                missing.append("Chiều cao")
            if can_nang <= 0:
                missing.append("Cân nặng")
            if not ket_luan:
                missing.append("Kết luận")

            if missing:
                st.error(f"⚠️ Vui lòng bổ sung: {', '.join(missing)}")
            else:
                new_data = {
                    "Họ và tên": ho_va_ten, "Lớp": lop, "Nhóm": ten_nhom,
                    "Chiều cao (m)": chieu_cao, "Cân nặng (kg)": can_nang,
                    "Chỉ số BMI": chi_so_bmi, "Kết luận": ket_luan, "Lời khuyên": loi_khuyen
                }
                try:
                    df_old = pd.read_csv(DATA_FILE)
                    df_new = pd.concat(
                        [df_old, pd.DataFrame([new_data])], ignore_index=True)
                    df_new.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
                    st.session_state.submitted_bmi = True
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi: {e}")

    # Admin Area
    st.divider()
    with st.expander("🔐 Quản lý dữ liệu (Admin)"):
        pwd = st.text_input("Mật khẩu Admin", type="password")
        if st.button("🗑️ Xóa TOÀN BỘ dữ liệu"):
            if pwd == "admin123":
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                if os.path.exists(QUIZ_FILE):
                    os.remove(QUIZ_FILE)
                initialize_files()
                st.success("Đã reset toàn bộ hệ thống.")
                st.rerun()
            else:
                st.error("Sai mật khẩu.")

# ==============================================================================
# TAB 2: BẢNG BÁO CÁO
# ==============================================================================
with tab2:
    st.title("📊 BÁO CÁO THỰC HÀNH")
    try:
        df_bmi = pd.read_csv(DATA_FILE)
        if not df_bmi.empty:
            df_bmi["BMI (Tự động tính)"] = (pd.to_numeric(
                df_bmi["Cân nặng (kg)"]) / (pd.to_numeric(df_bmi["Chiều cao (m)"]) ** 2)).round(2)

            tabs_nhom = st.tabs(
                ["Nhóm 1", "Nhóm 2", "Nhóm 3", "Nhóm 4", "Nhóm 5", "Nhóm 6"])
            all_groups = ["Nhóm 1", "Nhóm 2", "Nhóm 3",
                          "Nhóm 4", "Nhóm 5", "Nhóm 6 (Giáo viên)"]

            for idx, t in enumerate(tabs_nhom):
                with t:
                    g_df = df_bmi[df_bmi["Nhóm"] == all_groups[idx]]
                    if not g_df.empty:
                        for col in DISPLAY_COLUMNS:
                            if col not in g_df.columns:
                                g_df[col] = np.nan
                        st.dataframe(g_df[DISPLAY_COLUMNS].reset_index(
                            drop=True), use_container_width=True)
                    else:
                        st.info("Chưa có dữ liệu.")

            csv = df_bmi.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 Tải dữ liệu thực hành (.csv)",
                               csv, "thuc_hanh_bmi.csv", "text/csv")
        else:
            st.info("Chưa có dữ liệu thực hành.")
    except Exception as e:
        st.error(f"Lỗi đọc file: {e}")

# ==============================================================================
# TAB 3: ÔN TẬP & KIỂM TRA
# ==============================================================================
with tab3:
    col_video, col_content = st.columns([1, 2])

    with col_video:
        st.header("📺 Tổng kết bài học")
        st.info("Video tóm tắt kiến thức.")
        # Chỗ này để video bài giảng tổng kết (khác video khởi động)
        # Nếu thầy cô muốn dùng lại file cũ hoặc file khác thì sửa tên ở đây
        st.video("Tính_Chỉ_số_Khối_Cơ_thể_(BMI).mp4")
        st.caption("Hãy xem kỹ video trước khi làm bài!")

    with col_content:
        quiz_tab_do, quiz_tab_view = st.tabs(
            ["✍️ Làm bài thi", "🏆 Bảng vàng thành tích"])

        # >>> LÀM BÀI THI <<<
        with quiz_tab_do:
            st.subheader("Kiểm tra kiến thức")

            if "quiz_submitted" not in st.session_state:
                st.session_state.quiz_submitted = False
                st.session_state.score = 0
                st.session_state.quiz_answers = {}

            if st.session_state.quiz_submitted:
                score = st.session_state.score
                total = len(QUIZ_DATA)
                diem_so = (score / total) * 10

                if diem_so >= 8:
                    st.balloons()
                st.metric("Điểm số của bạn", f"{diem_so:.1f} / 10")

                with st.expander("🔍 Xem chi tiết đáp án"):
                    for idx, q in enumerate(QUIZ_DATA):
                        user_ans = st.session_state.quiz_answers.get(idx)
                        st.markdown(f"**Câu {idx+1}: {q['question']}**")
                        if user_ans == q['answer']:
                            st.success(f"✅ Chọn: {user_ans}")
                        else:
                            st.error(f"❌ Chọn: {user_ans}")
                            st.info(f"👉 Đáp án đúng: {q['answer']}")
                        st.caption(f"💡 {q['explanation']}")
                        st.divider()

                if st.button("🔄 Làm lại bài thi"):
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_answers = {}
                    st.rerun()

            else:
                with st.form("quiz_form"):
                    st.write("Điền thông tin để bắt đầu:")
                    q_name = st.text_input(
                        "Họ và tên học sinh", placeholder="Nguyễn Văn A")
                    q_class = st.text_input("Lớp", placeholder="10A1")
                    st.divider()

                    user_choices = {}
                    for idx, q in enumerate(QUIZ_DATA):
                        st.markdown(f"**Câu {idx+1}:** {q['question']}")
                        user_choices[idx] = st.radio(
                            "Chọn đáp án:", q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed")
                        st.write("")

                    submit_quiz = st.form_submit_button("Nộp bài")

                if submit_quiz:
                    error_msg = []
                    if not q_name.strip():
                        error_msg.append("Họ và tên")
                    if not q_class.strip():
                        error_msg.append("Lớp")

                    if error_msg:
                        st.error(f"⚠️ Bạn chưa điền: {', '.join(error_msg)}")
                    else:
                        missing_questions = []
                        score = 0
                        for idx, q in enumerate(QUIZ_DATA):
                            if user_choices[idx] is None:
                                missing_questions.append(str(idx + 1))
                            elif user_choices[idx] == q['answer']:
                                score += 1

                        if missing_questions:
                            st.error(
                                f"⚠️ Bạn chưa trả lời câu: {', '.join(missing_questions)}")
                        else:
                            st.session_state.score = score
                            st.session_state.quiz_answers = user_choices
                            st.session_state.quiz_submitted = True

                            quiz_entry = {
                                "Họ và tên": q_name, "Lớp": q_class,
                                "Số câu đúng": score, "Tổng số câu": len(QUIZ_DATA),
                                "Điểm số (Thang 10)": (score / len(QUIZ_DATA)) * 10,
                                "Thời gian nộp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            try:
                                df_old_q = pd.read_csv(QUIZ_FILE)
                                df_new_q = pd.concat(
                                    [df_old_q, pd.DataFrame([quiz_entry])], ignore_index=True)
                                df_new_q.to_csv(
                                    QUIZ_FILE, index=False, encoding='utf-8-sig')
                                st.rerun()
                            except Exception as e:
                                st.error(f"Lỗi lưu điểm: {e}")

        # >>> XEM BẢNG ĐIỂM <<<
        with quiz_tab_view:
            st.subheader("🏆 Bảng Xếp Hạng Lớp Học")
            try:
                df_quiz = pd.read_csv(QUIZ_FILE)
                if not df_quiz.empty:
                    df_quiz = df_quiz.sort_values(
                        by=["Điểm số (Thang 10)", "Thời gian nộp"], ascending=[False, False])

                    search_name = st.text_input(
                        "🔍 Tìm kiếm tên:", placeholder="Nhập tên...")
                    if search_name:
                        df_quiz = df_quiz[df_quiz["Họ và tên"].str.contains(
                            search_name, case=False, na=False)]

                    st.dataframe(df_quiz.style.highlight_max(axis=0, color='lightgreen', subset=[
                                 "Điểm số (Thang 10)"]), use_container_width=True, hide_index=True)
                    st.download_button("📥 Tải bảng điểm", df_quiz.to_csv(
                        index=False).encode('utf-8-sig'), "bang_diem.csv", "text/csv")
                else:
                    st.info("Chưa có dữ liệu điểm thi.")
            except Exception:
                st.info("Chưa có file dữ liệu.")


