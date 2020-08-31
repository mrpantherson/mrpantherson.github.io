import altair as alt
import pandas as pd


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
