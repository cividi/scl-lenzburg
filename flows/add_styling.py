from dataflows import Flow, add_field, update_package

def flow(parameters, datapackage, resources, stats):

    legend = []
    for s in parameters["styles"]:
        l = {}
        l["label"] = s["label"]
        l["shape"] = s["shape"]
        l["primary"] = s["primary"]
        for attr, val in s["symbol"].items():
            l[attr] = val
        legend.append(l)
    
    r_ = []

    v_ = {"name": "mapview","specType": "gemeindescanSnapshot","spec": {"title": parameters["title"],"description": parameters["description"],"attribution": "","bounds": parameters["bounds"],"legend": legend},"resources": r_}

    def add_styling():
        def step(row):
            in_ = row["class"]
            for s in parameters["styles"]:
                if in_ == s["class"]:
                    for attr, val in s["symbol"].items():
                        row[attr] = val
        return step

    return Flow(
        add_field('fill', 'string', None, resources=parameters["resources"]),
        add_field('fill-opacity', 'number', None, resources=parameters["resources"]),
        add_field('stroke', 'string', None, resources=parameters["resources"]),
        add_field('stroke-opacity', 'number', None, resources=parameters["resources"]),
        add_field('stroke-width', 'number', None, resources=parameters["resources"]),
        add_field('title', 'string', None, resources=parameters["resources"]),
        add_styling(),
        update_package(views=[v_]),
    )