# Data Labeling Workflow

This application helps you run the full end‑to‑end workflow for object detection datasets: import, smart sampling, labeling, review, moving approved data to a training project, and preparing train/val splits. Everything is controlled through a visual graph of nodes (cards) directly in the platform interface.

![Application overview](./app-overview.png)

## Features
- Visual workflow graph with clear steps and status indicators.
- Import from cloud sources with automatic recognition of popular annotation formats.
- Smart Sampling for selecting data for labeling, including AI index‑based strategies.
- Full labeling cycle via Labeling Queue: pick, annotate, review, approve.
- Automations: schedule and rule‑based runs for routine operations.
- Task history: each operation appears as a separate task with results.
- Can be launched on a new or an existing project.
- Some nodes may trigger other applications (e.g., for copying or importing data) — such actions are started as separate tasks and are visible in the history.

*Task history example:*
![Task history](./task-history.png)

*Automations example:*
![Automations](./automations.png)

## How to run
You can launch the app on a new or an existing project:

1. Find the “Data Labeling Workflow” app in the Supervisely Ecosystem.
1. Select the project in the Supervisely interface.
3. Choose an existing project or start from scratch — the app will automatically prepare the connected structure: a separate __Labeling Project__, a __Training Project__, a __labeling collection__, and a __Labeling Queue__.
4. In the run parameters, set `Restart Policy: onError`.
   - **Important:** use `onError` to enable recovery mode. If the task crashes unexpectedly, the app will restart and restore its history.
5. Click Run. You will see the graph interface with available actions and status indicators.

## Graph structure: key steps
Below are the main nodes you will see on the graph (names match the interface):

- Import from Cloud
  - Imports data from cloud sources. Each import creates a separate dataset in the Input Project. Popular annotation formats are supported.

- Input Project
  - The central “entry” project where all imported data is stored. Data here is not modified — it is used for further selection and analysis.

- OpenAI CLIP and AI Index
  - Nodes for semantic search and embeddings. Used together with Smart Sampling to select images by text prompts, similarity, or clusters.

- Smart Sampling
  - Selects a subset of data from the Input Project into the Labeling Project. Supports multiple strategies: random, diversity, clustering, and AI‑index‑based (calculated via the OpenAI CLIP model). The selected data is copied to the Labeling Project for further work.

- Labeling Project
  - A dedicated project that receives the data subset for annotation. All labeling operations are performed here. It serves as an intermediate step before moving approved data to the Training Project.

- Labeling Queue
  - Manages the annotation queue: annotators pick the next available item, then images go to review. Rejected items return to the same annotator.
  - Real‑time counters show:
    - How many images are currently being labeled.
    - How many are in review or waiting for review.
    - How many are already approved and ready to be moved to the training project.

- Train/Val Split
  - Splits data into training and validation sets. The structure mirrors the source organization, and the splits are collected into corresponding collections that can be used for model training.

- Move Labeled Data
  - Moves annotated and approved images to the Training Project.

- Training Project
  - The project for model training. It accumulates the finalized, verified data from the labeling process. New nodes for training, evaluation, comparison, and deployment can be connected to this card later.
