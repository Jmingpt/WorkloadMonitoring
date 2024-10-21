import streamlit as st
import plotly.graph_objects as go

config = {'displayModeBar': False}
colors = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"]


def plotly_piechart(data, labels, values, title):
    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=data[labels].values,
            values=data[values].values,
            hole=0.3,
            texttemplate="%{percent:.2%}",
            hovertemplate="%{label}: %{value} hours <extra></extra>",
            marker=dict(colors=["2a9d8f", "264653"])
        )
    )

    fig.update_layout(
        title_text=title,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True, config=config)


def plotly_barchart(data, labels, values, title, orientation="v", barmode=None, category=None):
    fig = go.Figure()

    if category:
        categories = data[category].unique()
        for cat in categories:
            subset = data[data[category] == cat]
            x = subset[labels] if orientation == "v" else subset[values]
            y = subset[values] if orientation == "v" else subset[labels]
            text = y if orientation == "v" else x
            hovertemplate = "%{x}: %{y:.2f}" if orientation == "v" else "%{y}: %{x:.2f}"
            color = "#2a9d8f" if cat == "billable" else "#264653"

            fig.add_trace(go.Bar(
                name=cat,
                x=x,
                y=y,
                text=text,
                texttemplate="%{text:.2f}",
                orientation=orientation,
                hovertemplate=f"{cat} <br> " + hovertemplate + " <extra></extra>",
                marker=dict(color=color)
            ))
    else:
        x = data[labels] if orientation == "v" else data[values]
        y = data[values] if orientation == "v" else data[labels]
        text = y if orientation == "v" else x
        hovertemplate = "%{x}: %{y}" if orientation == "v" else "%{y}: %{x}"

        fig.add_trace(go.Bar(
            x=x,
            y=y,
            text=text,
            orientation=orientation,
            hovertemplate=hovertemplate + " <extra></extra>",
            marker=dict(color=colors)
        ))

    fig.update_layout(
        title_text=title,
        height=600,
        barmode=barmode
    )

    st.plotly_chart(fig, use_container_width=True, config=config)
