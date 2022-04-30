import folium
from folium import plugins
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    m = folium.Map(location=[51.656859, 39.205926],
                   tiles='openstreetmap',
                   zoom_start=12)
    draw = plugins.Draw(export=True)
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('CartoDB Positron').add_to(m)
    measure_control = plugins.MeasureControl(position='topleft',
                                             active_color='red',
                                             completed_color='red',
                                             primary_length_unit='miles')

    all_subgroups = folium.FeatureGroup(name='Хорошее место')
    m.add_child(all_subgroups)

    tooltip = 'ВГУ'
    tooltip_2 = 'Oscar beef'
    tooltip_3 = 'Biga'
    tooltip_4 = 'Chayhona'
    tooltip_5 = 'Сулико'

    folium.Marker([51.656859, 39.205926], popup=('<a href="http://www.vsu.ru/"> Link </a>'), tooltip=tooltip,
                  icon=folium.Icon(color="red")).add_to(m)
    folium.Marker([51.666888, 39.205913], popup=('<a href="https://oscarbeef.business.site/"> Link </a>'),
                  tooltip=tooltip_2, icon=folium.Icon(color="red")).add_to(m)
    folium.Marker([51.674031, 39.208084], popup=('<a href="https://bigapizza.ru/"> Link </a>'), tooltip=tooltip_3,
                  icon=folium.Icon(color="red")).add_to(m)
    folium.Marker([51.668914, 39.198823], popup=('<a href="https://chaihona.ru/vrg/> Link </a>'), tooltip=tooltip_4,
                  icon=folium.Icon(color="red")).add_to(m)
    folium.Marker([51.658568, 39.204931], popup=('<a href="https://suliko-belucci.ru/> Link </a>'), tooltip=tooltip_5,
                  icon=folium.Icon(color="red")).add_to(m)

    draw.add_to(m)
    folium.LayerControl().add_to(m)
    m.add_child(measure_control)
    #    m.add_child(folium.LatLngPopup()) Под вопросом, иногда мешается
    m.save('name.html')
    return m._repr_html_()


# 51.656859, 39.205926
# 51.666888, 39.205913 Oscar beef
# 51.674031, 39.208084 Biga
# 51.668914, 39.198823 Chayhona
# 51.658568, 39.204931 Сулико

if __name__ == "__main__":
    app.run(debug=True)
