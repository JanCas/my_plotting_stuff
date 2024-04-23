def surface_plot_data(df, x_label, y_label, zlabel):
    x = df[x_label].unique()
    y = df[y_label].unique()
    z = df[zlabel].values.reshape(y.size,x.size)

    return x,y,z