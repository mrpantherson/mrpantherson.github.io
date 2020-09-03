import altair as alt
import pandas as pd
import panel as pn


# dnd scatter
df = pd.read_csv('./data/dnd_monsters.csv')

chart = alt.Chart(df).mark_point().encode(
    alt.X('hp', scale=alt.Scale(zero=False)),
    alt.Y('ac', scale=alt.Scale(zero=False)),
    alt.Color('legendary'),
    alt.Size('cr'),
    tooltip=[alt.Tooltip('name')]).interactive()

chart = chart.properties(title='DnD Monsters 5e',
    width=1000,
    height=600, )

chart.save('./graphs/graph1.html')

# dnd align heatmap
df = pd.read_csv('./data/dnd_monsters.csv')
df = df.loc[:, ['align', 'cr']]

chart = alt.Chart(df).mark_rect().encode(
    x=alt.X('cr:O', title="challenge rating"),
    y=alt.Y('align:O', title=''),
    color=alt.Color('count():Q')
    )

chart = chart.properties(title='DnD Monsters 5e - Count of Alignment Per Challenge Rating',
    width=1000,
    height=600, )

chart.save('./graphs/graph2.html')


# panel dashboard

import param
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import panel as pn
from bokeh.resources import INLINE

pn.extension()

df = pd.read_csv('./data/dnd_monsters.csv')

class TestDashboard(param.Parameterized):
    
    types = param.ObjectSelector(default='humanoid', objects=list(df.type.unique()))
    
    def get_data(self):
        class_df = df[(df.type==self.types)].copy()
        return class_df
    
    def box_view(self):
        data = self.get_data() 
        ax = sns.boxplot(data['hp'])
        plt.close()
        return ax.figure
    
    def table_view(self):
        data = self.get_data()
        return data.loc[:, ['name', 'align', 'size', 'cr']].sample(n=10)


rd = TestDashboard(name='')
dashboard_title = '# Test Dashboard'
dashboard_desc = 'Here I go again on my own'

dashboard = pn.Column(dashboard_title, 
                      dashboard_desc,   
                      rd.param,
                      pn.Row(rd.box_view, rd.table_view),
                     )

dashboard.save('./graphs/graph3.html', embed=True, resources=INLINE)
