import supervisely as sly
import supervisely.solution as sly_solution
from src.state import State

state = State()  # todo: temp
graph = sly_solution.GraphBuilder()
if sly.fs.file_exists("src/config.yaml"):
    graph.load_yaml("src/config.yaml")

static_dir = "static"
if not sly.fs.dir_exists(static_dir):
    sly.fs.mkdir(static_dir, True)

app = sly.Application(
    layout=sly.app.widgets.Container([graph, *graph.modals], gap=0),
    static_dir="static",
    show_header=False,
)
app.call_before_shutdown(sly_solution.TasksScheduler().shutdown)
app.call_before_shutdown(sly_solution.PubSubAsync().shutdown)

# # * Restore data and state if available
sly.app.restore_data_state(sly.env.task_id())

graph._prepare_ui_static(static_dir)
