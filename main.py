from dotenv import load_dotenv

import supervisely as sly

load_dotenv("local.env")

graph = sly.solution.SolutionGraphBuilder.from_yaml("src/config/config.yaml")

app = sly.Application(layout=sly.app.widgets.Container([graph, *graph.modals]))
