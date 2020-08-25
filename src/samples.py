import altair as alt
import pandas as pd


df = pd.read_csv('./data/dnd_monsters.csv')

chart = alt.Chart(df, title='DnD Monsters 5e').mark_point().encode(
    alt.X('hp', scale=alt.Scale(zero=False)),
    alt.Y('ac', scale=alt.Scale(zero=False)),
    alt.Size('legendary'),
    alt.Color('type'),
    tooltip=[alt.Tooltip('name')]).interactive()

chart.save('./graphs/graph1.html')
