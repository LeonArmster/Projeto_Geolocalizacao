# Projeto de cruzamento de Geolocalização

**Autor:** Leonardo Souza <br>
**Data Criação:** 02/12/25 <br>


## Objetivo

O objetivo deste projeto é cruzar a base de ordens com a mancha de fibra para identificar se cada ordem está dentro ou fora da área de cobertura da rede (mancha).
Além disso, o projeto gera uma visualização interativa em mapa, exibindo:

* Polígono da mancha de fibra

* Pontos das ordens

    * Verde: dentro da mancha

    * Vermelho: fora da mancha

Esse mapa é exportado como mapa.html, permitindo análise visual rápida.

## Bibliotecas Usadas

* Pandas
* Geopandas
* Folium

## Bases

Foram geradas automáticamente pelo chatgpt

Arquivo: **ordens.csv**

Base contendo as ordens de instalação/serviço.
Campos usados no projeto:

| Coluna    | Descrição              |
| --------- | ---------------------- |
| ordem_id  | Identificador da ordem |
| endereco  | Endereço textual       |
| cidade    | Cidade da ordem        |
| bairro    | Bairro da ordem        |
| latitude  | Coordenada Y           |
| longitude | Coordenada X           |
<br>

Arquivo: **fibra.geojson**

Arquivo geoespacial contendo o polígono da mancha de fibra.
O CRS deve estar em EPSG:4326 (latitude/longitude).


## Lógica do Processo

1. Carregar a base de ordens e renomear colunas.

1. Converter ordens em um GeoDataFrame, criando pontos pela latitude/longitude.

1. Carregar a mancha de fibra e garantir que esteja no mesmo CRS (EPSG:4326).

1. Executar um Spatial Join (sjoin) para verificar se cada ordem está dentro do polígono.

1. Padronizar o resultado, criando rótulos:

    * Dentro_Mancha

    * Fora_Mancha

1. Gerar um mapa interativo no Folium, adicionando:

    * Polígono da mancha

    * Pontos das ordens coloridos

1. Salvar o mapa como HTML