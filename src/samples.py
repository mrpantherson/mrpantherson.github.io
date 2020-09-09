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
sns.set_style('darkgrid')
df = pd.read_csv('./data/dnd_monsters.csv')

class DnDashboard(param.Parameterized):
    
    sizes = param.ObjectSelector(default='Medium', objects=list(df.loc[:, 'size'].unique()))
    
    def get_data(self):
        class_df = df[(df.loc[:, 'size']==self.sizes)].copy()
        return class_df

    def ac_hist(self):
        # data = self.get_data() interactivity removed for now
        chart = alt.Chart(df).mark_boxplot().encode(
            y=alt.Y('size:O', title="size"),
            x=alt.X('ac:Q', title='armor class'),
            color=alt.Color('size:O', scale=alt.Scale(scheme='tableau10'), legend=None),
            )

        return chart
    
    def table_view(self):
        data = df.loc[df.loc[:, 'size']=='Tiny', :]
        data = data.sort_values(by='ac', ascending=False)
        return data.loc[:, ['name', 'ac', 'type', 'size']].head(n=10)

db_panel = DnDashboard()
dashboard_title = '# DnD 5e Monster'
dashboard_desc = "I didn't start playing role playing games until D&D 5E came out, but I have been hooked on RPGs ever since. I thought it would be interesting to examine\
     the composition of creatures and see what commonalities there might be with respect to size and armor class. The box plot clearly shows the median growing with the\
     size of the monster, however there seems to be some interesting 'tiny' creatures with very large ac, the table view lists these creatures. Also below are some interesting\
     KPI for the creature attribute modes."
kpi = pn.Row('# 762 Creatures - ', '# Medium Size - ', '# Humanoid - ', '# Chaotic Evil Alignment')

dashboard = pn.Column(dashboard_title, 
                      dashboard_desc,
                      kpi,
                      pn.Row(db_panel.ac_hist, pn.Spacer(width=125), db_panel.table_view),
                     )

dashboard.save('./graphs/graph3.html', embed=True, resources=INLINE)
