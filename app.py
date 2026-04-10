import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang
st.set_page_config(page_title="BID Financial Dashboard", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    # 1. Bảng cân đối kế toán (BID.xlsx)
    df = pd.read_excel('BID.xlsx')
    if 'Năm' in df.columns:
        df = df.sort_values(by='Năm')
        
    # 2. Hiệu quả kinh doanh (BID1.xlsx)
    df1 = pd.read_excel('BID1.xlsx')
    if 'Năm' in df1.columns:
        df1 = df1.sort_values(by='Năm')
        
    # 3. Chỉ số tài chính & Lưu chuyển tiền tệ (BID2.xlsx)
    # File BID2 có cấu trúc tiêu đề (Header) ở dòng 2 (index=1)
    df2 = pd.read_excel('BID2.xlsx', header=1)
    df2 = df2.dropna(subset=['Năm'])  # Loại bỏ các dòng trống không có năm
    if 'Năm' in df2.columns:
        df2 = df2.sort_values(by='Năm')
        
    return df, df1, df2

# Header
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image("sbv_logo.png", width=80)
with col_title:
    st.title("Báo cáo tài chính - BID")
st.markdown("Dashboard tổng quan phân tích các chỉ tiêu định giá, báo cáo lưu chuyển tiền tệ và kết quả hoạt động kinh doanh (Ngân hàng BIDV).")

try:
    df, df1, df2 = load_data()
    
    # Gộp tất cả các năm để làm thanh trượt Sidebar
    all_years = list(df['Năm'].dropna()) + list(df1['Năm'].dropna()) + list(df2['Năm'].dropna())
    min_year = int(min(all_years))
    max_year = int(max(all_years))
    
    # Tạo Sidebar lọc dữ liệu
    st.sidebar.header("Lọc dữ liệu")
    selected_years = st.sidebar.slider("Chọn giai đoạn (Năm)", 
                                       min_value=min_year, 
                                       max_value=max_year, 
                                       value=(min_year, max_year))
    
    # Lọc các dataframe theo năm được chọn
    f_df = df[(df['Năm'] >= selected_years[0]) & (df['Năm'] <= selected_years[1])]
    f_df1 = df1[(df1['Năm'] >= selected_years[0]) & (df1['Năm'] <= selected_years[1])]
    f_df2 = df2[(df2['Năm'] >= selected_years[0]) & (df2['Năm'] <= selected_years[1])]

    # Giao diện chia thành 3 thẻ (Tabs)
    tab1, tab2, tab3 = st.tabs(["Cân đối Kế toán", "Hiệu quả Kinh doanh", "Chỉ số Tài chính & LCTT"])

    # ---------------- TAB 1: BẢNG CÂN ĐỐI KẾ TOÁN ----------------
    with tab1:
        st.subheader("Cân đối Kế toán (Nguồn: BID.xlsx)")
        st.dataframe(f_df.style.format(precision=0))
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Biến động Tài sản, Nợ và Vốn**")
            cols_cdkt = ["TỔNG CỘNG TÀI SẢN (đồng)", "NỢ PHẢI TRẢ (đồng)", "VỐN CHỦ SỞ HỮU (đồng)"]
            vc1 = [c for c in cols_cdkt if c in f_df.columns]
            if vc1:
                fig1 = px.line(f_df, x="Năm", y=vc1, markers=True, color_discrete_sequence=['#1f77b4', '#d62728', '#2ca02c'])
                fig1.update_layout(yaxis_title="Giá trị", xaxis_title="Năm", hovermode="x unified")
                st.plotly_chart(fig1, use_container_width=True)
                
        with c2:
            st.write("**Hoạt động Tín dụng & Huy động vốn**")
            cols_cred = ["Cho vay khách hàng", "Tiền gửi của khách hàng"]
            vc2 = [c for c in cols_cred if c in f_df.columns]
            if vc2:
                fig2 = px.bar(f_df, x="Năm", y=vc2, barmode="group", color_discrete_sequence=['#ff7f0e', '#9467bd'])
                fig2.update_layout(yaxis_title="Giá trị", xaxis_title="Năm", hovermode="x unified")
                st.plotly_chart(fig2, use_container_width=True)

    # ---------------- TAB 2: HIỆU QUẢ KINH DOANH ----------------
    with tab2:
        st.subheader("Kết quả Hoạt động Kinh doanh (Nguồn: BID1.xlsx)")
        st.dataframe(f_df1.style.format(precision=0))
        
        c3, c4 = st.columns(2)
        with c3:
            st.write("**Cơ cấu Doanh thu & Thu nhập**")
            cols_rev = ["Doanh thu (đồng)", "Thu nhập lãi thuần", "Lãi thuần từ hoạt động dịch vụ"]
            v_rev = [c for c in cols_rev if c in f_df1.columns]
            if v_rev:
                fig3 = px.bar(f_df1, x="Năm", y=v_rev, barmode="group")
                fig3.update_layout(yaxis_title="Giá trị", xaxis_title="Năm", hovermode="x unified")
                st.plotly_chart(fig3, use_container_width=True)
                
        with c4:
            st.write("**Biến động Lợi nhuận**")
            cols_prof = ["Lợi nhuận sau thuế của Cổ đông công ty mẹ (đồng)", "LN trước thuế"]
            v_prof = [c for c in cols_prof if c in f_df1.columns]
            if v_prof:
                fig4 = px.line(f_df1, x="Năm", y=v_prof, markers=True, color_discrete_sequence=['#00cc96', '#ab63fa'])
                fig4.update_layout(yaxis_title="Giá trị", xaxis_title="Năm", hovermode="x unified")
                st.plotly_chart(fig4, use_container_width=True)

    # ---------------- TAB 3: LƯU CHUYỂN TIỀN TỆ & TÀI CHÍNH ----------------
    with tab3:
        st.subheader("Chỉ số Phân tích & Lưu chuyển Tài chính (Nguồn: BID2.xlsx)")
        st.dataframe(f_df2.style.format(precision=2, na_rep='-'))
        
        c5, c6 = st.columns(2)
        with c5:
            st.write("**Hiệu quả Sinh lời (%)**")
            cols_profitability = ["Biên lợi nhuận ròng (%)", "ROE (%)", "ROA (%)"]
            v_prof_r = [c for c in cols_profitability if c in f_df2.columns]
            if v_prof_r:
                fig5 = px.line(f_df2, x="Năm", y=v_prof_r, markers=True)
                fig5.update_layout(yaxis_title="Tỷ lệ (%)", xaxis_title="Năm", hovermode="x unified")
                st.plotly_chart(fig5, use_container_width=True)
                
        with c6:
            st.write("**Định giá & Tỷ lệ**")
            cols_val = ["P/E", "P/B", "Đòn bẩy tài chính"]
            v_val = [c for c in cols_val if c in f_df2.columns]
            if v_val:
                fig6 = px.bar(f_df2, x="Năm", y=v_val, barmode="group")
                fig6.update_layout(yaxis_title="Chỉ số", xaxis_title="Năm", hovermode="x unified")
                st.plotly_chart(fig6, use_container_width=True)

except Exception as e:
    st.error(f"Đã xảy ra lỗi trong quá trình đọc và hiển thị dữ liệu: {e}")
