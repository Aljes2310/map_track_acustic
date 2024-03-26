from flask import Flask, render_template_string, Blueprint, render_template
import folium
from datetime import datetime, timedelta
import pandas as pd

data=pd.read_excel("/home/ZEMMEP/programa_data_acustica_operacional/df_biomasa.xlsx", 0)
factor=(data["Biomasa_transecto"].max()/100)
data["Biomasa_fixed"]=data["Biomasa_transecto"]/factor

min_lon, max_lon = -80.5, -78
min_lat, max_lat = 8, 9.5

bp=Blueprint("pages", __name__)

@bp.route("/")
def fullscreen():
    """Simple example of a fullscreen map."""
    m = folium.Map(location=[8.5,-79.5], zoom_start=9)

    # Define una escala de color (aquí estoy usando una escala de color lineal para fines de demostración)
    color_scale = folium.LinearColormap(["darkblue",'blue', "cyan" ,'green', 'yellow', 'red', "darkred"],
                                        vmin=data['Biomasa_fixed'].min(), vmax=data['Biomasa_fixed'].max(),
                                        tick_labels=[0,20,40,60,80,100])

    # Itera sobre cada fila del DataFrame y agrega marcadores al mapa
    for index, row in data.iterrows(): #<b> = bold
        # Obtiene el color del marcador en función del valor de la variable
        color = color_scale(row['Biomasa_fixed'])

        tooltip_text = f"<b><font size='4'>Latitud:</font></b> <font size='4'> {row['latitude']} </font> <br> <b><font size='4'>Longitud:</font></b> <font size='4'>{row['longitude']} </font> <br>   <b><font size='4'>Fecha:</font></b> <font size='4'> {row['fecha']} </font> <br> <b><font size='4'>Abundancia:</font></b> <font size='4'> {round(row['Biomasa_fixed'],1)}t </font>"
        folium.CircleMarker(location=[row['latitude'], row['longitude']], fill=True, tooltip=tooltip_text,
                            weight=1, fill_opacity=0.7, radius=3, color=color).add_to(m)


    # Agrega la escala de color al mapa
    color_scale.caption = f"Abundancia"
    color_scale.add_to(m)

    return m.get_root().render()


@bp.route("/iframe")
def iframe():
    """Embed a map as an iframe on a page."""
    m = folium.Map(min_lat=min_lat, max_lat=max_lat,min_lon=min_lon,max_lon=max_lon)

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template("iframe.html", iframe=iframe)


@bp.route("/components")
def components():
    """Extract map components and put those on a page."""
    m = folium.Map(
        width=800,
        height=600,
    )

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    {{ header|safe }}
                </head>
                <body>
                    <h1>Using components</h1>
                    {{ body_html|safe }}
                    <script>
                        {{ script|safe }}
                    </script>
                </body>
            </html>
        """,
        header=header,
        body_html=body_html,
        script=script,
    )

