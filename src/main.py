import supervisely as sly
from src.state import State

state = State() # todo: temp
graph = sly.solution.GraphBuilder.from_yaml("src/config.yaml")

app = sly.Application(layout=sly.app.widgets.Container([graph, *graph.modals]))
app.call_before_shutdown(sly.solution.TasksScheduler().shutdown)
app.call_before_shutdown(sly.solution.PubSubAsync().shutdown)
