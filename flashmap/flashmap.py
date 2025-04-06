"""Main module."""

import ipyleaflet

class Map(ipyleaflet.Map):
    def __init__(self, center=(0, 20), zoom=2, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)
    
    def add_basemap(self, basemap="OpenTopoMap"):
            allowed_basemaps = {
                "OpenStreetMap": ipyleaflet.basemaps.OpenStreetMap.Mapnik,
                "OpenTopoMap": ipyleaflet.basemaps.OpenTopoMap,
                "EsriWorldImagery": ipyleaflet.basemaps.Esri.WorldImagery,
                "EsriWorldStreetMap": ipyleaflet.basemaps.Esri.WorldStreetMap,
                "EsriNatGeoWorldMap": ipyleaflet.basemaps.Esri.NatGeoWorldMap,
            }

            # Ensure the basemap exists in our safe list
            if basemap not in allowed_basemaps:
                print(f"Invalid basemap name: {basemap}. Choose from {list(allowed_basemaps.keys())}")
            else:
                # Get the basemap object safely
                basemap_obj = allowed_basemaps[basemap]
                layer = ipyleaflet.TileLayer(url=basemap_obj.url, name=basemap)
                self.add(layer)

    def add_layer_control(self):
        self.add_control(ipyleaflet.LayersControl(position='bottomleft'))

    def add_geojson(self, url, zoom_to_layer=True, hover_style=None, **kwargs):
        """
        Adds a GeoJSON layer to the map.

        Args:
            url (str): The file path or URL to the GeoJSON data.
            zoom_to_layer (bool, optional): Whether to zoom the map to fit the bounds of the layer. Defaults to True.
            hover_style (dict, optional): A dictionary defining the style to apply when hovering over features. 
                Defaults to {'fillColor': 'yellow', 'fillOpacity': 0.2}.
            **kwargs: Additional keyword arguments for customization.
        """
        import geopandas as gpd
        
        if hover_style is None:
            hover_style = {'fillColor': 'yellow', 'fillOpacity': 0.2}

        data = gpd.read_file(url)
        data_gj = ipyleaflet.GeoJSON(data = data.__geo_interface__, hover_style=hover_style) # converting GeoDataFrame to GeoJSON
        self.add_layer(data_gj)

    if zoom_to_layer:
        data_bounds = data.total_bounds # deriving bounding box of the layer
        self.fit_bounds([[data_bounds[1], data_bounds[0]], [data_bounds[3], data_bounds[2]]]) # fitting map layout to the bounding box
            
    def add_shp(self, data, **kwargs):
        """
        Adds a shapefile layer to the map.

        Args:
            data (str): The file path to the shapefile.
            **kwargs: Additional keyword arguments for customization.
        """
        import geopandas as gpd

        data_gdf = gpd.read_file(data)
        data_gdf = data_gdf.to_crs(epsg=4326) # Reprojecting to WGS84 (EPSG:4326)
        data_gj = ipyleaflet.GeoJSON(data = data_gdf.__geo_interface__) # converting GeoDataFrame to GeoJSON
        self.add_layer(data_gj)


import folium


class FoliumMap:
    def __init__(self, center=(0, 20), zoom=2):
        """
        Initializes a folium map.

        Args:
            center (tuple): Latitude and longitude of the map's center. Defaults to (0, 20).
            zoom (int): Initial zoom level. Defaults to 2.
        """
        self.map = folium.Map(location=center, zoom_start=zoom)

    def add_basemap(self, basemap="OpenStreetMap"):
        """
        Adds a basemap to the map.

        Args:
            basemap (str): Name of the basemap. Defaults to "OpenStreetMap".
        """
        basemaps = {
            "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "OpenTopoMap": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
            "EsriWorldImagery": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        }

        if basemap not in basemaps:
            print(f"Invalid basemap name: {basemap}. Choose from {list(basemaps.keys())}")
        else:
            folium.TileLayer(tiles=basemaps[basemap], name=basemap, attr=basemap).add_to(self.map)

    def add_geojson(self, url, zoom_to_layer=True, hover_style=None):
        """
        Adds a GeoJSON layer to the map.

        Args:
            url (str): The file path or URL to the GeoJSON data.
            zoom_to_layer (bool): Whether to zoom the map to fit the bounds of the layer. Defaults to True.
            hover_style (dict): Not applicable in folium, but kept for compatibility.
        """
        import geopandas as gpd

        data = gpd.read_file(url)
        geojson = folium.GeoJson(data, name="GeoJSON").add_to(self.map)

        if zoom_to_layer:
            bounds = data.total_bounds  # [minx, miny, maxx, maxy]
            self.map.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

    def add_shp(self, filepath):
        """
        Adds a shapefile layer to the map.

        Args:
            filepath (str): The file path to the shapefile.
        """
        import geopandas as gpd
        
        data = gpd.read_file(filepath)
        data = data.to_crs(epsg=4326)  # Reproject to WGS84
        geojson = folium.GeoJson(data, name="Shapefile").add_to(self.map)
