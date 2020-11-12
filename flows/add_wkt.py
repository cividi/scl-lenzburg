from dataflows import Flow, add_field, delete_fields
from shapely.geometry import Point, LineString
import numpy as np

def flow(parameters, datapackage, resources, stats):

    def addWKT():
        def step(row):
            if parameters["type"] == 'Point':
                row[parameters["out-col"]] = Point(row[parameters["coord-cols"][0]],row[parameters["coord-cols"][1]]).wkt
            elif parameters["type"] == 'LineString':
                line = []
                for coords_pair in parameters["coord-cols"]:
                    pair = []
                    for coord_col in coords_pair:
                        pair.append(float(row[coord_col]))
                    line.append(pair)
                row[parameters["out-col"]] = LineString(line).wkt
            else:
                pass
        return step

    return Flow(
        add_field(parameters["out-col"], 'string', None, resources=parameters["resources"]),
        addWKT(),
        delete_fields(np.hstack(parameters["coord-cols"]), resources=parameters["resources"]),
    )