import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="食品銷售趨勢", layout="wide")

st.title("📊 2018-2024 食品銷售趨勢")

# 讀取 CSV
df = pd.read_csv("cleaned_forpyqt.csv")

# 取得時間欄和資料欄
time_column = df.columns[0]
data_columns = df.columns[1:6].tolist()

# 側邊欄選擇要顯示的資料
st.sidebar.title("選擇資料")
selected_columns = st.sidebar.multiselect(
    "選擇要顯示的折線:",
    data_columns,
    default=data_columns  # 預設全選
)

# 建立圖表
if selected_columns:
    fig = go.Figure()
    
    # 添加選中的折線
    for col in selected_columns:
        fig.add_trace(go.Scatter(
            x=df[time_column],
            y=df[col],
            mode='lines+markers',
            name=col,
            hovertemplate='<b>%{fullData.name}</b><br>時間: %{x}<br>指數: %{y}<extra></extra>'
        ))
    
    # 設定圖表樣式
    fig.update_layout(
        title="波動最大的五項",
        xaxis_title="時間",
        yaxis_title="銷售指數",
        hovermode='x unified',
        template='plotly_white',
        height=600,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("請至少選擇一項資料")

# 顯示原始資料表
if st.checkbox("顯示原始資料"):
    st.dataframe(df, use_container_width=True)