FROM continuumio/miniconda3

WORKDIR /app

RUN pip install pandas numpy shapely pyproj
