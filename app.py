import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang
st.set_page_config(page_title="BID Financial Dashboard", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    # Đọc file BCTC
    df = pd.read_excel('BID.xlsx')
    # Định dạng lại năm nếu có
    if 'Năm' in df.columns:
        df = df.sort_values(by='Năm')
    return df

col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image("sbv_logo.png", width=80)
with col_title:
    st.title("Báo cáo tài chính - BID")
st.markdown("Dashboard tổng quan phân tích các chỉ tiêu chính từ BCTC của Ngân hàng TMCP Đầu tư và Phát triển Việt Nam (BIDV).")

try:
    df = load_data()
    
    # Tạo Sidebar lọc dữ liệu
    st.sidebar.header("Lọc dữ liệu")
    if 'Năm' in df.columns:
        min_year = int(df['Năm'].min())
        max_year = int(df['Năm'].max())
        selected_years = st.sidebar.slider("Chọn giai đoạn (Năm)", 
                                           min_value=min_year, 
                                           max_value=max_year, 
                                           value=(min_year, max_year))
        filtered_df = df[(df['Năm'] >= selected_years[0]) & (df['Năm'] <= selected_years[1])]
    else:
        filtered_df = df

    st.subheader("Hiển thị dữ liệu dạng bảng")
    st.dataframe(filtered_df.style.format(precision=0))

    # Chia cột hiển thị biểu đồ
    col1, col2 = st.columns(2)

    # Biểu đồ 1: Tổng Tài sản vs Nợ Phải Trả vs Vốn Chủ Sở Hữu
    with col1:
        st.subheader("Cơ cấu Tài sản, Nợ và Vốn")
        columns_to_plot = ["TỔNG CỘNG TÀI SẢN (đồng)", "NỢ PHẢI TRẢ (đồng)", "VỐN CHỦ SỞ HỮU (đồng)"]
        valid_cols = [c for c in columns_to_plot if c in filtered_df.columns]
        if valid_cols and 'Năm' in filtered_df.columns:
            fig1 = px.line(filtered_df, x="Năm", y=valid_cols, markers=True, 
                           color_discrete_sequence=['#1f77b4', '#d62728', '#2ca02c'])
            fig1.update_layout(yaxis_title="Giá trị (VND)", xaxis_title="Năm", legend_title="Khoản mục",
                               hovermode="x unified")
            st.plotly_chart(fig1, use_container_width=True)

    # Biểu đồ 2: Tín dụng (Cho vay khách hàng vs Tiền gửi của khách hàng)
    with col2:
        st.subheader("Hoạt động Tín dụng & Huy động vốn")
        credit_cols = ["Cho vay khách hàng", "Tiền gửi của khách hàng"]
        valid_credit_cols = [c for c in credit_cols if c in filtered_df.columns]
        if valid_credit_cols and 'Năm' in filtered_df.columns:
            fig2 = px.bar(filtered_df, x="Năm", y=valid_credit_cols, barmode="group",
                          color_discrete_sequence=['#ff7f0e', '#9467bd'])
            fig2.update_layout(yaxis_title="Giá trị (VND)", xaxis_title="Năm", legend_title="Khoản mục",
                               hovermode="x unified")
            st.plotly_chart(fig2, use_container_width=True)

    # Biểu đồ mở rộng phía dưới: Các mục đầu tư và chứng khoán
    st.subheader("Hoạt động Đầu tư & Chứng khoán")
    invest_cols = ["Chứng khoán kinh doanh", "Chứng khoán đầu tư", "Đầu tư dài hạn (đồng)"]
    valid_invest = [c for c in invest_cols if c in filtered_df.columns]
    if valid_invest and 'Năm' in filtered_df.columns:
        fig3 = px.area(filtered_df, x="Năm", y=valid_invest)
        fig3.update_layout(yaxis_title="Giá trị (VND)", xaxis_title="Năm", legend_title="Khoản mục")
        st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"Đã xảy ra lỗi trong quá trình đọc và hiển thị dữ liệu: {e}")
