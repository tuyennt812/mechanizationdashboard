import streamlit as st
import pandas as pd
from plotnine import ggplot
from plotnine import ggplot # needed for st.pyplot compatibility
from plotnine import *
import matplotlib.pyplot as plt
import base64
from pathlib import Path
import os
st.set_page_config(
    page_title="Thực trạng cơ giới hóa trong canh tác lúa",
    page_icon="🌾",
    layout="wide"
)

# Roboto font for entire app
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

/* Apply to entire app */
html, body, [class*="css"]  {
    font-family: 'Roboto', sans-serif !important;
}

/* Sidebar also inherits */
[data-testid="stSidebar"] {
    font-family: 'Roboto', sans-serif !important;
}

/* Headers override to Roboto */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Roboto', sans-serif !important;
}

/* Plot titles (plotnine HTML wrappers) */
.plot-container {
    font-family: 'Roboto', sans-serif !important;
}

</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>

.toggle-row {
    display: flex;
    gap: 6px;
    margin-bottom: 15px;
}

.toggle-btn {
    flex: 1;
    padding: 10px 0;
    text-align: center;
    border-radius: 6px;
    border: 1px solid #2B8A3E;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    background-color: white;
    color: #2B8A3E;
}

.toggle-btn.active {
    background-color: #2B8A3E;
    color: white;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="
        background-color: #f1f8f3; 
        padding: 30px 40px; 
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: left;
    ">
        <h1 style="
            color: #2B8A3E; 
            margin: 0; 
            font-size: 28px; 
            letter-spacing: 1px;
            line-height: 1.2;
            font-weight: 600;
            letter-spacing: 4px;
            text-transform: uppercase;
        ">
            Thực Trạng Cơ Giới Hóa Trong Canh Tác Lúa
        </h1>
    </div>
""", unsafe_allow_html=True)
# ==========================
# IRRI logo
# ==========================
current_dir = os.path.dirname(os.path.abspath(__file__))
st.sidebar.image(os.path.join(current_dir, "icon", "IRRI.png"), width=160)

# ✅ SHOW MAP IF SELECTED
# ==========================
# Initialize session state to keep track of which view is active
if 'view_choice' not in st.session_state:
    st.session_state.view_choice = "Dashboard"

with st.sidebar:
    st.markdown(
        '<p style="color: #2B8A3E; font-size: 22px;font-weight:600; margin-bottom: 5px;">Chọn chế độ hiển thị</p>', 
        unsafe_allow_html=True
    )
    # Create two equal-sized columns
    col1, col2 = st.columns(2)
    
    with col1:
        # If 'Dashboard' is active, use the 'primary' (colored) button type
        if st.button(
            "Dashboard", 
            use_container_width=True, 
            type="primary" if st.session_state.view_choice == "Dashboard" else "secondary"
        ):
            st.session_state.view_choice = "Dashboard"
            st.rerun()

    with col2:
        # If 'Bản đồ' is active, use the 'primary' (colored) button type
        if st.button(
            "Bản đồ", 
            use_container_width=True, 
            type="primary" if st.session_state.view_choice == "Bản đồ" else "secondary"
        ):
            st.session_state.view_choice = "Bản đồ"
            st.rerun()

# Use the variable to control your app logic
view_choice = st.session_state.view_choice

if view_choice == "Bản đồ":

  st.markdown(
      f"""
      <div style="margin-top: 0px;">
          <a href="https://rmituniversity.maps.arcgis.com/apps/mapviewer/index.html?configurableview=true&webmap=1d1cac3f2b1f4f7f85784c2210eb182f&theme=light&center=105.62538600000002,9.736617999999991&scale=577790.554289" 
            target="_blank" 
            style="display:inline-block; padding:8px 16px; background-color:#2B8A3E; 
                    color:white; border-radius:8px; text-decoration:none; 
                    font-weight:600; font-size:14px; margin-bottom: 12px;">
              🔎 Click mở bản đồ toàn màn hình
          </a>
          <iframe src="https://rmituniversity.maps.arcgis.com/apps/mapviewer/index.html?configurableview=true&webmap=1d1cac3f2b1f4f7f85784c2210eb182f&theme=light&center=105.62538600000002,9.736617999999991&scale=577790.554289" 
                  width="100%" height="600" 
                  style="border:1px solid #eee; border-radius:10px;" 
                  allowfullscreen>
          </iframe>
      </div>
      """, 
      unsafe_allow_html=True
  )
  st.stop()
# ==========================
# ✅ EXCEL UPLOAD SECTION
# ==========================
uploaded_file = st.sidebar.file_uploader(
    "Tải lên template Excel dữ liệu (tùy chọn)",
    type=["xlsx"]
)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    st.sidebar.success("Đã tải dữ liệu từ template!")
else:
    df = pd.read_excel("data/df_app.xlsx", engine="openpyxl")
    st.sidebar.info("Đang dùng dữ liệu mặc định")

st.sidebar.markdown(
    """
    <p style="color:#2B8A3E; font-size:22px; font-weight:600; margin-bottom:0px;">
        Bộ lọc dữ liệu
    </p>
    """,
    unsafe_allow_html=True
)


left, right = st.columns([1, 3])
province_choice = st.sidebar.selectbox("Chọn tỉnh/thành phố:", ['Cần Thơ'])
#stage_choice = st.sidebar.selectbox("Chọn giai đoạn canh tác lúa:", df["stage"].unique())
stage_choice = st.sidebar.selectbox("Chọn giai đoạn canh tác lúa:", ['Bơm nước','Làm đất', 'Xuống giống','Chăm sóc lúa','Drone', 'Thu hoạch', 'Quản lý rơm rạ', 'Sau thu hoạch'])

filtered = df[df["stage"] == stage_choice]

from plotnine import (
    ggplot, aes, geom_col, geom_errorbar, geom_violin, geom_boxplot, geom_jitter, theme_minimal, labs
)

# Bar plots

def plot_bar_se_py(df, x_var, y_var, plot_title=""):
    # Xác định nhãn trục Y theo param_choice
    if y_var == "Công suất":
        ylab = df["unit_power"].iloc[0]   # ví dụ: hp, kW
    elif y_var == "Năng suất":
        ylab = df["unit_productivity"].iloc[0]  # thường: ha/giờ
    else:
        ylab = y_var


    df = df[[x_var, y_var]].dropna()  # loại bỏ hàng có giá trị thiếu ở cột x_var hoặc y_var


    summary = (
        df.groupby(x_var)[y_var]
          .agg(['mean', 'std', 'count'])
          .reset_index()
    )
    summary["se"] = summary["std"] / summary["count"]**0.5
    summary["lower"] = summary["mean"] - summary["se"]
    summary["upper"] = summary["mean"] + summary["se"]

    p = (
        ggplot(summary, aes(x=x_var, y="mean", fill=x_var))
        + geom_col(alpha=0.7, width=0.5)                # no black border
        + geom_errorbar(aes(ymin="lower", ymax="upper"), width=0.2)
        + theme_minimal()
        + theme(
            # Remove vertical gridlines
            panel_grid_major_x=element_blank(),
            panel_grid_minor_x=element_blank(),
            # Remove plot border
            #panel_border=element_blank(),
            # Remove axis lines (optional)
            axis_line=element_blank(),
            # Hide legend
            legend_position="none",
            # Increase font sizes
            axis_text_x=element_text(size=14),      # x‑axis category labels
            axis_text_y=element_text(size=14),      # y‑axis numeric labels
            axis_title_y=element_text(size=14),     # y‑axis title
            plot_background=element_rect(fill="#F5F5F5",color="none"),
            panel_background=element_rect(fill="#F5F5F5",color="none"),
            panel_border=element_blank()
    )
        + labs(
            title=plot_title,
            x="",
            y=ylab,
        )
    )
    return p

# Violin plots
from plotnine import (
    ggplot, aes, geom_violin, geom_boxplot, 
    theme_minimal, theme, labs
)

def plot_violin_simple(df, x_var, y_var,
                       plot_title="Violin Plot",
                       add_boxplot=True,
                       fill_label=None,
                       show_legend=False):
    # Xác định nhãn trục Y theo param_choice
    if y_var == "Công suất":
        ylab = df["unit_power"].iloc[0]   # ví dụ: hp, kW
    elif y_var == "Năng suất":
        ylab = df["unit_productivity"].iloc[0]  # thường: ha/giờ
    else:
        ylab = y_var  # giữ nguyên mặc định

    fill_lab_final = fill_label if fill_label else x_var

    df = df[[x_var, y_var]].dropna()  # loại bỏ hàng có giá trị thiếu ở cột x_var hoặc y_var
    p = (
        ggplot(df, aes(x=x_var, y=y_var, fill=x_var))
        + geom_violin(alpha=0.7,color=None)
        + theme_minimal()
        + theme(
            # Remove vertical gridlines
            panel_grid_major_x=element_blank(),
            panel_grid_minor_x=element_blank(),
            # Remove plot border
            panel_border=element_blank(),
            # Remove axis lines (optional)
            axis_line=element_blank(),
            # Hide legend
            legend_position="none",
            # Increase font sizes
            axis_text_x=element_text(size=14),      # x‑axis category labels
            axis_text_y=element_text(size=14),      # y‑axis numeric labels
            axis_title_y=element_text(size=14),     # y‑axis title
            plot_background=element_rect(fill="#F5F5F5",color="none"),
            panel_background=element_rect(fill="#F5F5F5",color="none")
        )
        
    )

    if add_boxplot:
        p += geom_boxplot(width=0.12, alpha=1, color="#00BFC4")

    p += labs(
            title=plot_title,
            x='',
            y=ylab,
            fill=fill_lab_final
        )
  

    # ✅ Plotnine: ẩn legend đúng cách
    if not show_legend:
        p += theme(legend_position='none')

    return p

def plot_pie_chart(data, category_var, plot_title="Pie Chart"):
    data = data[[category_var]].dropna()  # loại bỏ hàng có giá trị thiếu ở cột category_var
    counts = data[category_var].value_counts()
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#F5F5F5')   # ✅ whole figure grey
    ax.set_facecolor('#F5F5F5')          # ✅ plot area grey
  
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.75,      # moves percentage labels outward (0=center, 1=edge)
        labeldistance=1.04,      # moves category labels outward,
        textprops={'color': 'black'},  # set category label color\
        wedgeprops={'edgecolor': 'white', 'linewidth': 2,'alpha': 0.8},  # white borders between slices
        colors = ["#F8766D", "#00BFC4"]
    )
        # Set percentage labels to white and bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
    
    # Draw a white circle in the center to create the donut hole
    centre_circle = plt.Circle((0, 0), 0.50, fc='white', linewidth=0)
    ax.add_artist(centre_circle)
    
    ax.set_title(plot_title)
    ax.axis('equal')
    
    return fig                                    

def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()



# ===== Title for plot section =====
# ====== CREATE 4 PLOT BOXES ======
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# ==========================
# ✅ 1. ROW 1 — COL 1 → CÔNG SUẤT
# ==========================

with row1_col1:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-bottom:5px;">
            <img src="data:image/png;base64,{get_base64_bin_file(os.path.join(current_dir, "icon", "power.png"))}"
                style="width: 30px; height: 30px; margin-right: 12px; vertical-align: middle;">
            <h3 style="font-size: 22px; font-weight: 200; margin: 0;">
                Công suất máy - {stage_choice}
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- NO DATA ----
    if filtered.empty:
        st.warning("Không có dữ liệu phù hợp.")

    else:
        # -------- MAIN LOGIC --------
        num_groups = filtered["machine_type"].nunique()

        # ✅ CASE 1: Non-Drone + 1 category → Violin
        if num_groups == 1 and stage_choice != "Drone":
            fig = plot_violin_simple(
                filtered,
                x_var="machine_type",
                y_var="Công suất",
                plot_title=""
            )
            st.pyplot(fig.draw())

        # ✅ CASE 2: Non-Drone + multiple categories → Bar
        elif num_groups != 1 and stage_choice != "Drone":
            fig = plot_bar_se_py(
                filtered,
                "machine_type",
                "Công suất",
                ""
            )
            st.pyplot(fig.draw())

        # ✅ CASE 3: Drone → always group by main_function
        elif stage_choice == "Drone":
            fig = plot_bar_se_py(
                filtered,
                "main_function",
                "Công suất",
                ""
            )
            st.pyplot(fig.draw())

# ==========================
# ✅ 2. ROW 1 — COL 2 → NĂNG SUẤT
# ==========================
with row1_col2:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-bottom:5px;">
            <img src="data:image/png;base64,{get_base64_bin_file(os.path.join(current_dir, "icon", "productivity.png"))}"
                style="width: 30px; height: 30px; margin-right: 12px; vertical-align: middle;">
            <h3 style="font-size: 22px; font-weight: 200; margin: 0;">
                Năng suất máy - {stage_choice}
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- NO DATA ----
    if filtered.empty:
        st.warning("Không có dữ liệu phù hợp.")

    else:
        # -------- MAIN LOGIC --------
        num_groups = filtered["machine_type"].nunique()

        # ✅ CASE 1: Non-Drone + 1 category → Violin
        if num_groups == 1 and stage_choice != "Drone":
            fig = plot_violin_simple(
                filtered,
                x_var="machine_type",
                y_var="Năng suất",
                plot_title=""
            )
            st.pyplot(fig.draw())

        # ✅ CASE 2: Non-Drone + multiple categories → Bar
        elif num_groups != 1 and stage_choice != "Drone":
            fig = plot_bar_se_py(
                filtered,
                "machine_type",
                "Năng suất",
                ""
            )
            st.pyplot(fig.draw())

        # ✅ CASE 3: Drone → always group by main_function
        elif stage_choice == "Drone":
            fig = plot_bar_se_py(
                filtered,
                "main_function",
                "Năng suất",
                ""
            )
            st.pyplot(fig.draw())

# ==========================
# ✅ 3. ROW 2 — COL 1 → XUẤT XỨ (Pie Chart)
# ==========================
with row2_col1:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-bottom:5px;">
            <img src="data:image/png;base64,{get_base64_bin_file(os.path.join(current_dir, "icon", "sourcing.png"))}" 
                style="width: 30px; height: 30px; margin-right: 12px; vertical-align: middle;">
            <h3 style="font-size: 22px; font-weight: 200; margin: 0">
                Xuất xứ máy - {stage_choice}
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    if filtered.empty:
        st.warning("Không có dữ liệu phù hợp.")
    else:
        fig = plot_pie_chart(
            filtered,
            category_var="Xuất xứ",
            plot_title=""
        )
        st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================
# ✅ 4. ROW 2 — COL 2 → BIỂU ĐỒ PHỤ THUỘC GIAI ĐOẠN
# ==========================
with row2_col2:

    if filtered.empty:
        st.warning("Không có dữ liệu phù hợp.")

    else:
        # -----------------------------
        # ✅ DRONE → Tải trọng (kg/lần)
        # -----------------------------
        if stage_choice == "Drone":
            target_col = "Tải trọng (kg/lần)"
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom:5px;">
                    <img src="data:image/png;base64,{get_base64_bin_file(os.path.join(current_dir, "icon", "battery.png"))}" 
                        style="width: 30px; height: 30px; margin-right: 12px; vertical-align: middle;">
                    <h3 style="font-size: 22px; font-weight: 200; margin: 0">
                        Tải trọng - Drone
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            fig = None
            num_groups = filtered["machine_type"].nunique()

            if num_groups == 1:
                fig = plot_violin_simple(
                    filtered,
                    x_var="machine_type",
                    y_var=target_col,
                    plot_title=f"kg vật tư nông nghiệp tải được trong một lần bay"
                )
                st.pyplot(fig.draw())
            else:
                fig = plot_bar_se_py(
                    filtered,
                    "machine_type",
                    target_col,
                    ""
                )
                st.pyplot(fig.draw())


        # ------------------------------------------------------
        # ✅ THU HOẠCH → Tỉ lệ chiều dài rơm trên chiều dài lúa (%)
        # ------------------------------------------------------
        elif stage_choice == "Thu hoạch":
            target_col = "Tỉ lệ chiều dài rơm trên chiều dài lúa (%)"
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom:5px;">
                    <img src="data:image/png;base64,{get_base64_bin_file(os.path.join(current_dir, "icon", "ratio.png"))}" 
                        style="width: 30px; height: 30px; margin-right: 12px; vertical-align: middle;">
                    <h3 style="font-size: 22px; font-weight: 200; margin: 0">
                        Tỉ lệ chiều dài rơm trên chiều dài lúa (%)
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            fig = None
            fig = plot_violin_simple(
                    filtered,
                    x_var="machine_type",
                    y_var=target_col,
                    plot_title=""
                )
            st.pyplot(fig.draw())



        # -----------------------------------------------
        # ✅ QUẢN LÝ NƯỚC → Lưu lượng bơm (mét khối/giờ)
        # -----------------------------------------------
        elif stage_choice == "Bơm nước":
            target_col = "Lưu lượng bơm (mét khối/giờ)"
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom:5px;">
                    <img src="data:image/png;base64,{get_base64_bin_file(os.path.join(current_dir, "icon", "water.png"))}" 
                        style="width: 30px; height: 30px; margin-right: 12px; vertical-align: middle;">
                    <h3 style="font-size: 22px; font-weight: 200; margin: 0">
                        Lưu lượng bơm (mét khối/giờ)
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            fig = None
            num_groups = filtered["machine_type"].nunique()

            if num_groups == 1:
                fig = plot_violin_simple(
                    filtered,
                    x_var="machine_type",
                    y_var=target_col,
                    plot_title=f"Lưu lượng bơm - {stage_choice}"
                )
                st.pyplot(fig.draw())
            else:
                fig = plot_bar_se_py(
                    filtered,
                    "machine_type",
                    target_col,
                    ""
                )
                st.pyplot(fig.draw())


        # ✅ mặc định cho các stage khác (không có chỉ tiêu)
        else:
            st.write("")

    st.markdown('</div>', unsafe_allow_html=True)

    
st.markdown(
    """
    <p style='font-size:16px; font-style:italic; color:#555; margin-top: 0px; text-align:right;'>
        Nguồn: Khảo sát của IRRI về cơ giới hóa trong sản xuất lúa vào 01/2026 tại 3 xã Thạnh Quới, Long Hưng, Thuận Hòa
        thuộc thành phố Cần Thơ.
    </p>
    """,
    unsafe_allow_html=True
)
