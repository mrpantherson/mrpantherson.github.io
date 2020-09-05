import altair as alt
import pandas as pd
import panel as pn
import param
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.resources import INLINE


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
pn.extension()
df = pd.read_csv('./data/dnd_monsters.csv')

class DnDashboard(param.Parameterized):
    
    sizes = param.ObjectSelector(default='Medium', objects=list(df.loc[:, 'size'].unique()))
    
    def get_data(self):
        class_df = df[(df.loc[:, 'size']==self.sizes)].copy()
        return class_df
    
    def hp_hist(self):
        data = self.get_data() 

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        sns.distplot(data.loc[:, 'hp'], ax=ax, kde=False)
        sns.distplot(df.loc[:, 'hp'], ax=ax, kde=False)
        return fig

    def ac_hist(self):
        data = self.get_data() 

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        sns.distplot(data.loc[:, 'ac'], ax=ax, kde=False)
        sns.distplot(df.loc[:, 'ac'], ax=ax, kde=False)
        return fig
    
    def table_view(self):
        data = self.get_data()
        return data.loc[:, ['name', 'align', 'size', 'cr']].sample(n=10)

db_panel = DnDashboard()
dashboard_title = '# DnD 5e Monster'
dashboard_desc = 'Simple interactive dashboard that lets you pick a monster size and see how the distribution of health and ac changes.'

dashboard = pn.Column(dashboard_title, 
                      dashboard_desc,
                      db_panel.param,
                      pn.Row(db_panel.hp_hist, db_panel.ac_hist, db_panel.table_view),
                     )

dashboard.save('./graphs/graph3.html', embed=True, resources=INLINE)
