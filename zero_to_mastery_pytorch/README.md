# Zero to Mastery PyTorch

Working through the [Zero to Mastery: Learn PyTorch for Deep Learning](https://www.learnpytorch.io/)
course, one directory per course chapter. Each directory holds the notebook I
wrote while following the chapter, the corresponding exercise notebook, and —
where a topic warranted a second pass — an extra notebook from the official
[PyTorch tutorials](https://docs.pytorch.org/tutorials/) or my own scratch
experiments.

## Setup

The notebooks were written and run in [Google Colab](https://colab.research.google.com/)
(most on a GPU runtime), so they carry their saved outputs and expect Colab's
preinstalled data-science stack. The exercise notebooks keep their "Open in
Colab" badge — that's the easiest way to run them.

To run locally instead, install with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run jupyter lab
```

Note that [pyproject.toml](pyproject.toml) only declares `torch`. The notebooks
also reach for `torchvision`, `torchinfo`, `torchmetrics`, `matplotlib`,
`numpy`, `pandas`, `scikit-learn`, `mlxtend`, `tqdm`, and `requests`, plus the
course's `helper_functions.py`, which several notebooks download at runtime from
[mrdbourke/pytorch-deep-learning](https://github.com/mrdbourke/pytorch-deep-learning).
Add those with `uv add` before running outside Colab.

Datasets (FashionMNIST, the `pizza_steak_sushi` image set, MNIST) are downloaded
by the notebooks themselves into a local `data/` directory and aren't committed.

## Notebooks

| Notebook | Covers |
|----------|--------|
| [pytorch_fundamentals/00_pytorch_fundamentals.ipynb](pytorch_fundamentals/00_pytorch_fundamentals.ipynb) | [00. PyTorch Fundamentals](https://www.learnpytorch.io/00_pytorch_fundamentals/) — tensor creation, attributes, manipulation, matrix multiplication, reshaping, indexing, NumPy interop, reproducibility, running on the GPU |
| [pytorch_fundamentals/00_pytorch_fundamentals_exercises.ipynb](pytorch_fundamentals/00_pytorch_fundamentals_exercises.ipynb) | Chapter 00 exercises |
| [pytorch_fundamentals/pytorch_basics_quickstart.ipynb](pytorch_fundamentals/pytorch_basics_quickstart.ipynb) | Extra: the official [PyTorch Quickstart](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — end-to-end FashionMNIST loop in one sitting |
| [pytorch_workflows/01_pytorch_workflow_fundamentals.ipynb](pytorch_workflows/01_pytorch_workflow_fundamentals.ipynb) | [01. PyTorch Workflow Fundamentals](https://www.learnpytorch.io/01_pytorch_workflow/) — data → build model → train → evaluate → save/load, on a linear regression toy problem |
| [pytorch_workflows/01_pytorch_workflow_exercises.ipynb](pytorch_workflows/01_pytorch_workflow_exercises.ipynb) | Chapter 01 exercises |
| [pytorch_workflows/01_pytorch_workflows_playground.ipynb](pytorch_workflows/01_pytorch_workflows_playground.ipynb) | Extra: my own playground rerunning the whole workflow on multiple linear regression |
| [pytorch_workflows/pytorch_what_is_torch_nn_really.ipynb](pytorch_workflows/pytorch_what_is_torch_nn_really.ipynb) | Extra: the official [What is `torch.nn` really?](https://docs.pytorch.org/tutorials/beginner/nn_tutorial.html) — building MNIST training from raw tensors up to `nn.Module`, `optim`, `Dataset`, and `DataLoader` |
| [pytorch_neural_network_classification/02_pytorch_neural_network_classification.ipynb](pytorch_neural_network_classification/02_pytorch_neural_network_classification.ipynb) | [02. Neural Network Classification](https://www.learnpytorch.io/02_pytorch_classification/) — binary and multi-class classification on `make_circles`/`make_blobs`, non-linearity, logits → probabilities → labels, loss functions per task |
| [pytorch_neural_network_classification/02_pytorch_classification_exercises.ipynb](pytorch_neural_network_classification/02_pytorch_classification_exercises.ipynb) | Chapter 02 exercises (`make_moons`, spirals) |
| [pytorch_computer_vision/03_pytorch_computer_vision.ipynb](pytorch_computer_vision/03_pytorch_computer_vision.ipynb) | [03. Computer Vision](https://www.learnpytorch.io/03_pytorch_computer_vision/) — FashionMNIST, `DataLoader` batching, baseline vs. non-linear vs. CNN models, `nn.Conv2d`/`nn.MaxPool2d`, timing runs, confusion matrix |
| [pytorch_computer_vision/03_pytorch_computer_vision_exercises.ipynb](pytorch_computer_vision/03_pytorch_computer_vision_exercises.ipynb) | Chapter 03 exercises |
| [pytorch_custom_datasets/04_pytorch_custom_datasets.ipynb](pytorch_custom_datasets/04_pytorch_custom_datasets.ipynb) | [04. Custom Datasets](https://www.learnpytorch.io/04_pytorch_custom_datasets/) — the `pizza_steak_sushi` image set via `ImageFolder` and a hand-written `Dataset`, transforms and data augmentation, TinyVGG, loss curves and over/underfitting |
| [pytorch_custom_datasets/04_pytorch_custom_datasets_exercises.ipynb](pytorch_custom_datasets/04_pytorch_custom_datasets_exercises.ipynb) | Chapter 04 exercises |
| [pytorch_custom_datasets/pytorch_datasets_dataloaders.ipynb](pytorch_custom_datasets/pytorch_datasets_dataloaders.ipynb) | Extra: the official [Datasets & DataLoaders](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html) tutorial |
| [pytorch_going_modular/05_pytorch_going_modular.ipynb](pytorch_going_modular/05_pytorch_going_modular.ipynb) | [05. Going Modular](https://www.learnpytorch.io/05_pytorch_going_modular/) — turning chapter 04's notebook into reusable scripts (`data_setup.py`, `model_builder.py`, `engine.py`, `utils.py`, `train.py`) with `%%writefile` |
| [pytorch_going_modular/05_pytorch_going_modular_exercise.ipynb](pytorch_going_modular/05_pytorch_going_modular_exercise.ipynb) | Chapter 05 exercises — `get_data.py`, argparse-driven `train.py`, and a `predict.py` |

The scripts written out by the chapter 05 notebooks land in a `going_modular/`
directory at runtime and aren't committed — rerun the notebook to regenerate
them.
