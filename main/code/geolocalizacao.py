# Bibliotecas
import pandas as pd
import geopandas as gpd
import folium
from folium import GeoJson

# Lendo arquivo de ordens
df = pd.read_csv(r'C:\Users\leo-s\desktop\estudos\projeto_geopandas\main\data\ordens.csv')

# Renomeando as colunas
df = df.rename(columns={'ordem_id':'ordem', 'endereco':'endereco_ordem', 'cidade':'cidade_ordem', 'bairro':'bairro_ordem'})

# Transformando em um geodataframe
gdf_ordens = gpd.GeoDataFrame(
    df, 
    geometry=gpd.points_from_xy(df.longitude, df.latitude),
    crs='EPSG:4326'
    )

# Carregando a mancha de fibra
gdf_fibra = gpd.read_file(r'C:\Users\leo-s\desktop\estudos\projeto_geopandas\main\data\fibra.geojson')


# Garantir o crs
gdf_fibra = gdf_fibra.to_crs('EPSG:4326')


# Verificando se as ordens estão dentro da mancha
gdf_join = gpd.sjoin(gdf_ordens, gdf_fibra, how='left', predicate='within')


# Trocando so valores da coluna fibra
gdf_join['fibra'] = gdf_join['fibra'].astype(str)
gdf_join['fibra'] = gdf_join['fibra'].str.replace('1.0','Dentro_Mancha')
gdf_join['fibra'] = gdf_join['fibra'].str.replace('nan','Fora_Mancha')


# Criando visualização em mapa

## Centro aproximado do estado de SP
map_sp = folium.Map(location=[-22.5, -48.5], zoom_start=7)
map_sp


# Plotar os polígonos da mancha de fibra
## Adicionando os poligonos ao mapa
GeoJson(
    gdf_fibra.to_json(),
    name='Mancha de FIbra',
    style_function= lambda x: {
        'fillcolor': 'blue',
        'color': 'blue',
        'weight': 1,
        'fillopacity': 0.3,
    }
).add_to(map_sp)


# Adicionar pontos das ordens com cor diferente se tem fibra ou não
for _, row in gdf_join.iterrows():
    cor = 'green' if row['fibra'] == 'Dentro_Mancha' else 'red'

    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=5,
        color=cor,
        fill=True,
        fill_color=cor,
        popup=f"Ordem: {row['ordem']} <br> Fibra: {row['fibra']}"
    ).add_to(map_sp)


# Adicionar um controle de camadas
folium.LayerControl().add_to(map_sp)


# Mostrar o mapa
map_sp.save(r'C:\Users\leo-s\desktop\estudos\projeto_geopandas\main\data\mapa.html')
