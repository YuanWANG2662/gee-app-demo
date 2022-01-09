from ee import collection
import streamlit as st
import ee
import os
import datetime
import geopandas as gpd
import folium
import geemap.colormaps as cm
# import geemap.foliumap as geemap
import geemap
from datetime import date, time
from rois import *

st.set_page_config(layout="wide")

st.title('EO4BEE')
st.markdown("This webapp provide a tool to visualize various earth observation data to support the decision-making process of beekeeping in Europe")

if st.session_state.get("zoom_level") is None:
	st.session_state["zoom_level"] = 4

st.session_state["ee_asset_id"] = None
st.session_state["bands"] = None
st.session_state["palette"] = None
st.session_state["vis_params"] = None

m = geemap.Map(
	basemap="ROADMAP", plugin_Draw=True, draw_export=True, locate_control=True
)

row1_col1, row1_col2 = st.columns([1, 1])

with row1_col1:
	keyword = st.text_input("Search for a location:", "")

with row1_col2:
	if keyword:
		locations = geemap.geocode(keyword)
		if locations is not None and len(locations) > 0:
			str_locations = [str(g)[1:-1] for g in locations]
			location = st.selectbox("Select a location:", str_locations)
			loc_index = str_locations.index(location)
			selected_loc = locations[loc_index]
			lat, lng = selected_loc.lat, selected_loc.lng
			folium.Marker(location=[lat, lng], popup=location).add_to(m)
			m.set_center(lng, lat, 12)
			st.session_state["zoom_level"] = 12

def mapTemperature():
	collection = ee.ImageCollection('ECMWF/ERA5/MONTHLY').select('mean_2m_air_temperature')
	vis_params = {
		'min': 250.0,
		'max': 320.0,
		'palette': [
			"#000080","#0000D9","#4000FF","#8000FF","#0080FF","#00FFFF",
			"#00FF80","#80FF00","#DAFF00","#FFFF00","#FFF500","#FFDA00",
			"#FFB000","#FFA400","#FF4F00","#FF2500","#FF0A00","#FF00FF",
		]
	}
	image = collection.first()
	m.addLayer(image,vis_params,"First Image")
	image_t = collection.toBands()
	m.addLayer(image_t, {}, "Time series", True)
	m.add_time_slider(collection, vis_params, '',"Time series", time_interval=1)

def mapPrecipitation():
	st.write('Precipitation coming')

datasets = {
	"temperature":mapTemperature,
	"precipitation":mapPrecipitation
}

row2_col1, row2_col2 = st.columns([2, 1])

with row2_col2:
	variable = st.selectbox("Select a variable:",datasets.keys(),index=0)

if variable:
	datasets[variable]()

with row2_col1:
	if not keyword:
		m.set_center(14, 52, 4)
	m.to_streamlit(height=500)




