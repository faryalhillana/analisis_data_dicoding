import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import folium
from folium import Marker
from folium.plugins import HeatMap, MarkerCluster
import streamlit as st
from streamlit_folium import st_folium


sns.set(style='dark')

all_df = pd.read_csv("dashboard/dashboard_data.csv")

st.header("Olist's Brazilian E-Commerce Public Dataset Dashboard")
st.subheader("by Faryal Hillan")

sum_order_items_df = all_df.groupby("product_category_name").order_item_id.sum().sort_values(ascending=False).reset_index()
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Most Popular Product")
        max_order = sum_order_items_df["order_item_id"][0]
        st.metric(sum_order_items_df["product_category_name"][0]+" sales", value=max_order)

    with col2:
        st.subheader("Least Popular Product")
        min_order = sum_order_items_df["order_item_id"].iloc[-1]
        st.metric(sum_order_items_df["product_category_name"].iloc[-1]+" sales", value=min_order)

with st.container():
    st.subheader("Most and Least Popular Product by Number of Sales")

    fig1, ax1 = plt.subplots(figsize=(24, 24))

    sns.barplot(x="order_item_id", y="product_category_name", data=sum_order_items_df.head(10), palette="deep", ax=ax1, hue="product_category_name", legend=False)
    ax1.set_ylabel(None)
    ax1.set_xlabel(None)
    ax1.set_title("Most Popular Product", loc="center", fontsize=40)
    ax1.tick_params(axis="y", labelsize=36)
    ax1.tick_params(axis="x", labelsize=36)

    fig2, ax2 = plt.subplots(figsize=(24, 24))
    sns.barplot(x="order_item_id", y="product_category_name", data=sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(10), palette="deep", ax=ax2, hue="product_category_name", legend=False)
    ax2.set_ylabel(None)
    ax2.set_xlabel(None)
    ax2.invert_xaxis()
    ax2.yaxis.set_label_position("right")
    ax2.yaxis.tick_right()
    ax2.set_title("Least Popular Product", loc="center", fontsize=40)
    ax2.tick_params(axis="y", labelsize=36)
    ax2.tick_params(axis="x", labelsize=36)

    st.pyplot(fig1)
    st.pyplot(fig2)

sum_orders_city = all_df.groupby("customer_city").order_id.count().sort_values(ascending=False).reset_index()
sum_orders_state = all_df.groupby("customer_state").order_id.count().sort_values(ascending=False).reset_index()

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        city_sales = sum_orders_city["order_id"][0]
        st.metric("City with Most Sales: "+sum_orders_city["customer_city"][0], value=city_sales)

    with col2:
        state_sales = sum_orders_state["order_id"][0]
        st.metric("State with Most Sales: "+sum_orders_state["customer_state"][0], value=state_sales)

with st.container():
    heat_map = folium.Map(location=[-23.574809, -46.587471], tiles="cartodbpositron", zoom_start=12)
    HeatMap(data=all_df[["geolocation_lat", "geolocation_lng"]], radius=10).add_to(heat_map)

    cluster_map = folium.Map(location=[-23.574809, -46.587471], tiles="cartodbpositron", zoom_start=13)
    mc = MarkerCluster()
    for idx, row in all_df.iterrows():
        if not math.isnan(row["geolocation_lng"]) and not math.isnan(row["geolocation_lat"]):
            mc.add_child(Marker([row["geolocation_lat"], row["geolocation_lng"]]))
    cluster_map.add_child(mc)

    st.subheader("Order Distribution Heat Map")
    st_data = st_folium(heat_map, width=725)
    st.subheader("Order Distribution Cluster Map")
    st_data2 = st_folium(cluster_map, width=725)
