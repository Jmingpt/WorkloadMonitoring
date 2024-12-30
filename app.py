import os
import streamlit as st
from datetime import datetime, timedelta
from workload import (
    extract_information,
    overall_transform,
    client_breakdown_transform,
    member_transform,
    task_transform
)
from workload import plotly_piechart, plotly_barchart


def run():
    st.set_page_config(
        page_title="Persuasion Resource",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="auto"
    )
    st.title("Resource Monitoring")
    st.logo(image="./src/logo.webp", size="large")

    today = datetime.today()
    week_num = today.isocalendar().week - 1

    with st.sidebar:
        st.header(f"Week: {week_num}")

    source_dir = f"data/week{week_num}"
    member_files = os.listdir(source_dir)

    if member_files:
        data = extract_information(member_files, source_dir)
        default_list = ["All"]
        with st.sidebar:
            selected_name = st.selectbox(
                label="Members",
                options=default_list + data["name"].unique().tolist()
            )
            selected_category = st.selectbox(
                label="Category",
                options=default_list + data["billable"].unique().tolist()
            )
            selected_client = st.selectbox(
                label="Client",
                options=default_list + data["client"].unique().tolist()
            )

        if selected_name != "All":
            data = data[data["name"] == selected_name]
        if selected_category != "All":
            data = data[data["billable"] == selected_category]
        if selected_client != "All":
            data = data[data["client"] == selected_client]

        num_client = data["client"].nunique()
        num_billale_taks = data[data["billable"] == "billable"][["client", "task"]].drop_duplicates().shape[0]
        num_nonbillale_taks = data[data["billable"] == "non-billable"][["client", "task"]].drop_duplicates().shape[0]
        total_hours = round(data["hours"].sum(), 2)
        avg_hours = round(total_hours / data["name"].nunique(), 2)
        score_card = st.columns((1, 1, 1.3, 1, 1))
        with score_card[0]:
            st.metric(
                label="Number of Clients",
                value=num_client,
            )
        with score_card[1]:
            st.metric(
                label="Number of Billable Tasks",
                value=num_billale_taks
            )
        with score_card[2]:
            st.metric(
                label="Number of Non-billable Tasks",
                value=num_nonbillale_taks
            )
        with score_card[3]:
            st.metric(
                label="Total Hours",
                value=total_hours
            )
        with score_card[4]:
            st.metric(
                label="Avg Hours",
                value=avg_hours
            )

        overall_hours = overall_transform(data)
        client_billable_hours = client_breakdown_transform(data)
        chart_columns_top = st.columns((1, 2))
        with chart_columns_top[0]:
            plotly_piechart(overall_hours, "billable", "hours", "Billable vs Non-billable Hours")
        with chart_columns_top[-1]:
            plotly_barchart(client_billable_hours, "client", "hours", "Client breakdown", orientation="h", category="billable")

        member_hours = member_transform(data)
        total_hours = member_hours.groupby("name").agg(
            total_hours=("hours", "sum")
        ).reset_index()
        member_hours = member_hours.merge(total_hours, on="name")
        member_hours["percentage"] = member_hours["hours"] / member_hours["total_hours"] * 100
        plotly_barchart(member_hours, "name", "percentage", "Employee Usage", orientation="v", barmode="stack", category="billable")

        task_hours = task_transform(data)
        st.markdown("**Task Details**")
        st.dataframe(
            data=task_hours,
            hide_index=True,
            use_container_width=True
        )


if __name__ == "__main__":
    run()
