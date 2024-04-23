import io

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.plotly.data_manipulation import surface_plot_data

delimiter = st.text_input('Delimiter', '\s')

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter="\s+")

        st.write(df)

        options = st.multiselect(
                'columns to plot',
                df.columns,
                )

        options_to_freeze = st.multiselect(
                'columns to plot',
                set(list(df.columns)).difference(set(options)),
                )

        filter_v = {}
        for option in options_to_freeze:
                filter_v[option] = st.select_slider(
                        option,
                        options=df[option].unique())

        temp = df.loc[(df[list(filter_v)] == pd.Series(filter_v)).all(axis=1)]

        st.write(temp)

        print(filter_v)

        plot_options = st.selectbox(
                'plotting options',
                ["2D", "3D"],
                index=None
        )

        if plot_options == "2D":
                fig = px.line(df, x=options[0], y=options[1])
                st.plotly_chart(fig, use_container_width=True)

        if plot_options == "3D":
                x,y,z = surface_plot_data(temp, options[0], options[1], options[2])

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