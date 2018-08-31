from osgeo import gdal

gdal.Warp("/home_local/obayona/rasters/PRECT2018-05-21-21-39-21-reproj.tif","/home_local/obayona/rasters/PRECT2018-05-21-21-39-21.tif",dstSRS="EPSG:3857")