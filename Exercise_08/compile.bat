@echo off
call "C:\QGIS_3_40_5\bin\o4w_env.bat"
::call "C:\QGIS_3_40_5\bin\qt5_env.bat"
::call "C:\QGIS_3_40_5\bin\py3_env.bat"
@echo on
pyrcc5 -o resources.py resources.qrc