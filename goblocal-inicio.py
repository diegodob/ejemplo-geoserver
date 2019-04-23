#!/usr/bin/env python

from geoserver.catalog import Catalog
import sys
import geoserver.util

if len(sys.argv) != 4:
  print("Modo de uso: goblocal-inicio.py GEOSERVER_URL GEOSERVER_USER GEOSERVER_PASSWORD")
  sys.exit(10001)

geoserverURL = sys.argv[1]  
geoserverUser = sys.argv[2]  
geoserverPassword = sys.argv[3]  


cat = Catalog(geoserverURL + "/rest",username=geoserverUser, password=geoserverPassword)

workspace_3df = cat.create_workspace("3df", "http://www.tresdefebrero.gov.ar")

shape_dir = "/opt/goblocal-inicio/datos/3df_limites/3df_limites" 
shapefile_plus_sidecars = geoserver.util.shapefile_and_friends(shape_dir)
cat.create_featurestore("3df_limites", shapefile_plus_sidecars, workspace_3df)

