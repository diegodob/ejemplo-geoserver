#!/usr/bin/env python

from geoserver.catalog import Catalog
import sys
import geoserver.util
from gsreceta import GSReceta


if len(sys.argv) != 4:
  print("Modo de uso: goblocal-inicio.py GEOSERVER_URL GEOSERVER_USER GEOSERVER_PASSWORD")
  sys.exit(10001)

geoserverURL = sys.argv[1]  
geoserverUser = sys.argv[2]  
geoserverPassword = sys.argv[3]  

base_shape_dir = "/opt/goblocal-inicio/datos/" 

cat = Catalog(geoserverURL + "/rest",username=geoserverUser, password=geoserverPassword)

unaGSReceta = GSReceta(cat)
unaGSReceta.ejecutar("/opt/goblocal-inicio/datos/comandos.json")


## Capa de limites
# workspace_3df = cat.create_workspace("3df", "http://www.tresdefebrero.gov.ar/limites")
# limites_shape_dir = base_shape_dir + "3df_limites/3df_limites"
# limites_shp_y_otros_archivos = geoserver.util.shapefile_and_friends(limites_shape_dir)
# cat.create_featurestore("3df_limites", limites_shp_y_otros_archivos, workspace_3df)

## Capa de establecimientos educativos
# workspace_establecimientos_educativos = cat.create_workspace("hab_e_infra_social", "http://www.tresdefebrero.gov.ar/establecimientos_educativos")
# establecimientos_educativos_dir = base_shape_dir + "3df_establecimientos_educativos/3df_establecimientos_educativos"
# establecimientos_educativos_shp_y_otros_archivos = geoserver.util.shapefile_and_friends(establecimientos_educativos_dir)
# cat.create_featurestore("3df_establecimientos_educativos", establecimientos_educativos_shp_y_otros_archivos, workspace_establecimientos_educativos)

