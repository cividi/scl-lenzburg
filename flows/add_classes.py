from dataflows import Flow, add_field

def flow(parameters, datapackage, resources, stats):

    def add_class():
        def step(row):
            in_ = row[parameters["in-col"]]
            for c in parameters["classes"]:
                if "from" in c and "to" in c:
                    if in_ >= c["from"] and in_ < c["to"]:
                        row["class"] = c["class"]
                elif "from" in c and "to" not in c:
                    if in_ >= c["from"]:
                        row["class"] = c["class"]
                elif "to" in c and not "from" not in c:
                    if in_ < c["to"]:
                        row["class"] = c["class"]
        return step

    return Flow(
        add_field('class', 'string', None, resources=parameters["resources"]),
        add_class(),
    )