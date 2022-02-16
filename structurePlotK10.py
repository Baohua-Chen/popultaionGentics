#!/home/bin/python3

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio

def readData(k):
    d = pd.read_csv('k'+str(k)+'/data_result.txt', header=None, sep=' +')
    d['inv'] = d[0] + '_' + d[1].map('{:02d}'.format)
    d = d[d[0]!='LP']
    cats = ['ZS','FD','DY','FF','PT','DS','ZJ','XW']
    d[0] = d[0].str.replace('LJ','PT')
    d[0] = d[0].astype('category').cat.set_categories(cats, ordered=True)
    d = d.sort_values([0])
    d['inv'] = d['inv'].str.replace('LJ','PT')
    d['pop'] = d['inv'].map(pd.read_csv('../pop.txt', header=None, sep='\t', index_col=0)[1].to_dict())
    d['pop'] = d['pop'].astype('category').cat.set_categories(clusters, ordered=True)
    d = d.dropna()

    vbounds = []
    s = 0
    for i in d.groupby('pop')[0].count().sort_index():
        e = s + i
        vbounds.append([s,e])
        s = e
    vbounds2 = []
    s = 0
    for i,v in d[0].value_counts().sort_index().iteritems():
        e = s + v
        vbounds2.append([i, s, e])
        s = e
#    vbounds2 = pd.DataFrame(vbounds2).rename(dict(zip(range(2), ['pop', 's', 'e'])), axis=1)
    vbounds2 = pd.DataFrame(vbounds2, columns=['pop', 's', 'e'])
    return d, vbounds, vbounds2

def plot():
    mk = 10
    fontStyle = 'Arial'
    fontBase = 7
    fontSize = dict(tick=2.5*fontBase,title=5*fontBase,legend=5*fontBase, scaleTick=4*fontBase, scaleTitle=5*fontBase, legendTitle=5*fontBase, legendText=4*fontBase)

    colors1 = ['#3686B7', '#C9BA83', '#7f1f17', '#3CB371'] #red, yellow, blue, green
    colors2 = px.colors.qualitative.Vivid
    print(len(colors2))
    fig = make_subplots(rows=mk, cols=1, row_heights=[0.05]+[(1-0.05-0.002*10)/(mk-1)]*(mk-1), vertical_spacing=0.002)
    for k in range(2, mk+1):
        d, vbounds, vbounds2 = readData(k)
#    d.to_csv('/dev/stdout', sep='\t', index=None)
        for i in range(d.shape[1]-5):
            color = colors2[i]
            fig.add_trace(go.Bar(x=d['inv'], y=d.iloc[:,3+i], showlegend=False, marker_color=color), row=k, col=1)

    fig.add_trace(go.Scatter(x=[10], y=[2], mode='text', text=['A'], textfont=dict(family=fontStyle, size=40, color='white'), showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=[(j[0]+j[1])/2 for j in vbounds], y=[1.5]*len(vbounds), mode='text', text=[ '<b>'+i+'</b>' for i in clusters ], textfont=dict(family=fontStyle, size=44, color='black'), showlegend=False), row=1, col=1)
    for i in range(len(vbounds)):
        color = colors1[i]
        fig.add_shape(x0=vbounds[i][0], x1=vbounds[i][1], y0=0.9, y1=1.05, fillcolor=color, line_color=color, opacity=1, layer="below", line_width=0, row=1, col=1)
    fig.add_trace(go.Scatter(x=[(j[0]+j[1])/2 for j in vbounds2.drop('pop', axis=1).to_numpy()], y=[0.4]*vbounds2.shape[0], mode='text', text=[ '<b>'+i+'</b>' for i in vbounds2['pop'].to_list()], textfont=dict(family=fontStyle, size=32, color='white'), showlegend=False), row=1, col=1)
    for i in vbounds2.drop('pop', axis=1).to_numpy():
        color = colors2.pop(0)
        fig.add_shape(x0=i[0], x1=i[1], y0=0, y1=0.8, fillcolor=color, line_color=color, opacity=1, layer="below", line_width=0, row=1, col=1)
    fig.update_layout(barmode='stack', template='plotly_white')
#    fig.update_xaxes(titlefont=None, tickfont=dict(family=fontStyle, size=fontSize['tick']-9), tickangle=90, row=1, col=1)
    fig.update_xaxes(titlefont=None, showticklabels=False, showgrid=False, zeroline=False, showline=False, row=1, col=1)
    fig.update_yaxes(titlefont=None, showticklabels=False, showgrid=False, zeroline=False, showline=False, row=1, col=1)
    for k in range(2, mk+1):
        fig.update_xaxes(titlefont=None, showticklabels=False, showgrid=False, showline=False, row=k, col=1)
        fig.update_yaxes(title='K='+str(k), titlefont=dict(family=fontStyle, size=fontSize['title']), showgrid=False, showticklabels=False, row=k, col=1)
    fig.update_xaxes(titlefont=None, showticklabels=True, tickfont=dict(family=fontStyle, size=fontSize['tick']), showgrid=False, showline=False, row=mk, col=1)
#    fig.update_xaxes(categoryorder='array', categoryarray=cats, titlefont=None, tickfont=dict(family=fontStyle, size=fontSize['tick']-9), tickangle=90, row=1, col=1)
#    fig.update_yaxes(title='K='+str(k), titlefont=dict(family=fontStyle, size=fontSize['title']), showgrid=False, tickwidth=0, showticklabels=False)
    pio.write_image(fig, 'frappe.k10.jpg', height=2600, width=2600)

clusters = ['DQ', 'MD', 'NH']
plot()
