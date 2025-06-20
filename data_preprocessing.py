# data_preprocessing.py

import streamlit as st
import pandas as pd

@st.cache_data(show_spinner="📦 Loading and preprocessing data... (may take 1–5 mins)", max_entries=1)
def load_data():
    df = pd.read_parquet("//Ds1821/기획실/홍은정/Power BI/데이터연결/sales_data.parquet")
    df['주문/물류일자'] = pd.to_datetime(df['주문/물류일자'], errors='coerce')
    df['매출'] = (df['실판매금액(반품반영)'] / 1.1).round(0)
    df['사전원가'] = (df['사전원가금액(반품반영)'] / 1.1).round(0)
    df['판매량'] = df['주문수량(반품반영)'].round(0)
    df['주문월'] = df['주문/물류일자'].dt.to_period('M').astype(str)
    return df.dropna(subset=['주문/물류일자'])

@st.cache_data
def get_unique_sorted(series):
    return sorted(series.dropna().unique())
