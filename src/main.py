import supervisely as sly
from src.state import State

state = State()  # todo: temp
graph = sly.solution.GraphBuilder()
if sly.fs.file_exists("src/config.yaml"):
    graph.load_yaml("src/config.yaml")

app = sly.Application(layout=sly.app.widgets.Container([graph, *graph.modals]), static_dir="static")
app.call_before_shutdown(sly.solution.TasksScheduler().shutdown)
app.call_before_shutdown(sly.solution.PubSubAsync().shutdown)

# # * Restore data and state if available
sly.app.restore_data_state(sly.env.task_id())
