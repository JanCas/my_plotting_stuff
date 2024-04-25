import io

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from utils.plotly.data_manipulation import surface_plot_data

#pio.templates.default = "plotly"

delimiter = st.text_input('Delimiter', '\s+')

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter=delimiter)

    st.write(df)

    options = st.multiselect(
        'columns to plot',
        df.columns,
    )

    options_to_freeze = st.multiselect(
        'values to fix',
        set(list(df.columns)).difference(set(options)),
    )

    filter_v = {}
    for option in options_to_freeze:
        filter_v[option] = st.select_slider(
            option,
            options=np.sort(df[option].unique()))

    temp = df.loc[(df[list(filter_v)] == pd.Series(filter_v)).all(axis=1)]

    st.write(temp)

    print(filter_v)

    plot_options = st.selectbox(
        'plotting options',
        ["2D", "3D"],
        index=None
    )

    if plot_options == "2D":
        value_filter = st.selectbox(
            'value to filter',
            df.columns,
            index=None
        )

        if value_filter:

                reshaped = temp.pivot(index=options[0], columns=value_filter, values=options[1])
                reshaped.reset_index(inplace=True)

                reshaped.columns = ['Time'] + [f'{options[1]}_v_{col}' for col in reshaped.columns[1:]]

                cumu = st.toggle("cummulative")

                if cumu:
                    reshaped.iloc[:, 1:] = reshaped.iloc[:, 1:].cumsum(axis=0)

                st.write(reshaped)
                print(reshaped.columns[1:])

                fig = px.line(reshaped, x=reshaped.columns[0], y=reshaped.columns[1:])
                fig.update_layout(title=f"{options[0]} vs {options[1]}", xaxis_title=options[0], yaxis_title=options[1])

                st.plotly_chart(fig, use_container_width=True)

                buffer = io.StringIO()
                fig.write_html(buffer, include_plotlyjs='cdn')
                html_bytes = buffer.getvalue().encode()

                st.download_button(
                        label='Download HTML',
                        data=html_bytes,
                        file_name='stuff.html',
                        mime='text/html'
                )

    if plot_options == "3D":
        cumu = st.toggle("cummulative")

        if cumu:
            temp[options[2]] = temp[options[2]].cumsum(axis=0)

        x, y, z = surface_plot_data(temp, options[0], options[1], options[2])

        fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
        fig.update_layout(title=f'{options[0]} vs {options[1]} and {options[2]}', autosize=True,
                          width=1000, height=800,
                          scene=dict(
                              xaxis_title=options[0],
                              yaxis_title=options[1],
                              zaxis_title=options[2]),
                          margin=dict(l=65, r=50, b=65, t=90))

        st.plotly_chart(fig, use_container_width=True)

        buffer = io.StringIO()
        fig.write_html(buffer, include_plotlyjs='cdn')
        html_bytes = buffer.getvalue().encode()

        st.download_button(
            label='Download HTML',
            data=html_bytes,
            file_name='stuff.html',
            mime='text/html'
        )
