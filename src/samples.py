import altair as alt
import pandas as pd


df = pd.read_csv('./data/dnd_monsters.csv')

# dnd scatter

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
