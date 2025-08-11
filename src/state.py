import os

from dotenv import load_dotenv

import supervisely as sly


class State:
    PROJECT_ID = "PROJECT_ID"
    LABELING_PROJECT_ID = "LABELING_PROJECT_ID"
    LABELING_QUEUE_ID = "LABELING_QUEUE_ID"
    LABELING_COLLECTION_ID = "LABELING_COLLECTION_ID"
    TRAINING_PROJECT_ID = "TRAINING_PROJECT_ID"

    def __init__(self) -> None:
        self.load_env()
        self.api = sly.Api.from_env()
        self.project_id = sly.env.project_id()
        self.project = self.api.project.get_info_by_id(self.project_id)
        if not self.project:
            raise ValueError(f"Project with ID {self.project_id} not found.")
        self.custom_data = self.project.custom_data
        self.update_project = False
        self._initialize_custom_data()
        self._set_environment_variables()

    def load_env(self):
        if sly.is_development():
            load_dotenv("local.env")
            load_dotenv(os.path.expanduser("~/supervisely.env"))

    def _initialize_custom_data(self):
        if State.LABELING_PROJECT_ID not in self.custom_data:
            self._create_labeling_project()

        if State.TRAINING_PROJECT_ID not in self.custom_data:
            self._create_trainig_project()

        # Additional collections and queues can be initialized here as needed
        if State.LABELING_COLLECTION_ID not in self.custom_data:
            self._create_labeling_collection()

        if State.LABELING_QUEUE_ID not in self.custom_data:
            self._create_labeling_queue()

        if self.update_project:
            self.api.project.update_custom_data(self.project.id, self.custom_data)

    def _set_environment_variables(self):
        os.environ[State.PROJECT_ID] = str(self.project.id)
        os.environ[State.LABELING_PROJECT_ID] = str(self.custom_data[State.LABELING_PROJECT_ID])
        os.environ[State.LABELING_QUEUE_ID] = str(self.custom_data[State.LABELING_QUEUE_ID])
        os.environ[State.LABELING_COLLECTION_ID] = str(self.custom_data[State.LABELING_COLLECTION_ID])
        os.environ[State.TRAINING_PROJECT_ID] = str(self.custom_data[State.TRAINING_PROJECT_ID])

    def _create_project(self, name: str) -> sly.ProjectInfo:
        return self.api.project.create(
            self.project.workspace_id, name, change_name_if_conflict=True
        )

    def _create_labeling_project(self) -> None:
        project = self._create_project(name=f"{self.project.name} (labeling)")
        self.custom_data[State.LABELING_PROJECT_ID] = project.id
        self.update_project = True

    def _create_trainig_project(self) -> None:
        project = self._create_project(name=f"{self.project.name} (training)")
        self.custom_data[State.TRAINING_PROJECT_ID] = project.id
        self.update_project = True

    def _create_collection(self, project_id: int, name: str):
        return self.api.entities_collection.create(project_id, name)

    def _create_labeling_collection(self) -> None:
        collection = self._create_collection(
            self.custom_data[State.LABELING_PROJECT_ID], "Labeling Collection"
        )
        self.custom_data[State.LABELING_COLLECTION_ID] = collection.id
        self.update_project = True

    def _create_labeling_queue(self) -> None:
        # members = self.api.user.get_team_members(self.project.team_id)
        # reviewers = [m.id for m in members if m.role == sly.UserRoleName.REVIEWER]
        # annotators = [m.id for m in members if m.role == sly.UserRoleName.ANNOTATOR]
        me = [self.api.user.get_my_info()]
        reviewers = [m.id for m in me]
        annotators = [m.id for m in me]
        labeling_queue = self.api.labeling_queue.create(
            name=f"Labeling Queue for project ID:{self.project.id}",
            user_ids=annotators,
            reviewer_ids=reviewers,
            collection_id=self.custom_data[State.LABELING_COLLECTION_ID],
            dynamic_classes=True,
            dynamic_tags=True,
            allow_review_own_annotations=True,
            skip_complete_job_on_empty=True,
        )
        labeling_queue = self.api.labeling_queue.get_info_by_id(labeling_queue)
        self.custom_data[State.LABELING_QUEUE_ID] = labeling_queue.id
        self.update_project = True
