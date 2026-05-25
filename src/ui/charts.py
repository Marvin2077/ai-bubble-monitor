import plotly.express as px

def line_chart(df, x, y, color=None, title=''):
    return px.line(df, x=x, y=y, color=color, title=title)
