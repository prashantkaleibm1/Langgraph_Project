# LangGraph Temperature Conversion Workflow

This project demonstrates a small LangGraph workflow that converts a temperature
from Celsius to Fahrenheit. The workflow has one conversion node, is compiled
before use, and can be invoked with a temperature input.

The implementation is in [Temperature_Conversion_Workflow.ipynb](./Temperature_Conversion_Workflow.ipynb).

## Requirements

- Python 3.11
- Conda (for the environment setup below), or another Python environment manager
- Jupyter Notebook or JupyterLab to run the notebook

The notebook uses:

- `langgraph` to define, compile, run, and visualize the graph.
- `typing.TypedDict`, included in Python, to describe the workflow state.
- `IPython.display` to show the graph image in a notebook.

The project's [requirements.txt](./requirements.txt) also lists `langchain-openai`
and `python-dotenv`; they are not needed by this temperature-conversion example.

## Create the environment

From the project directory, create and activate a Conda environment:

```powershell
conda create -n langgraph-test python=3.11 -y
conda activate langgraph-test
```

Install the project dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you only need to run this example, you can install LangGraph directly instead:

```powershell
python -m pip install langgraph
```

Install Jupyter if it is not already available in the environment:

```powershell
python -m pip install notebook
```

Start Jupyter from the project directory and open
[Temperature_Conversion_Workflow.ipynb](./Temperature_Conversion_Workflow.ipynb):

```powershell
jupyter notebook
```

Run the notebook cells in order.

## Build the workflow

### 1. Define the state

The state carries the input Celsius temperature and the converted Fahrenheit
temperature:

```python
from typing import TypedDict

class TemperatureState(TypedDict):
    temp_celsius: float
    temp_fahrenheit: float
```

### 2. Create the conversion node

A LangGraph node is a function that accepts the current state and returns its
updated state. This node applies the Celsius-to-Fahrenheit formula and rounds
the result to two decimal places:

```python
def convert_temp(state: TemperatureState) -> TemperatureState:
    celsius = state["temp_celsius"]
    fahrenheit = (celsius * 9 / 5) + 32
    state["temp_fahrenheit"] = round(fahrenheit, 2)
    return state
```

### 3. Add nodes and connect the graph

`START` marks the workflow's entry point and `END` marks its completion. The
single conversion node is connected between them:

```python
from langgraph.graph import END, START, StateGraph

graph = StateGraph(TemperatureState)
graph.add_node("convert_temp", convert_temp)
graph.add_edge(START, "convert_temp")
graph.add_edge("convert_temp", END)
```

### 4. Compile the graph

Compile the `StateGraph` to create an executable workflow:

```python
workflow = graph.compile()
```

### 5. Execute the workflow

Invoke the compiled workflow with a Celsius input. The returned state includes
the original Celsius value and the converted Fahrenheit value:

```python
initial_state = {"temp_celsius": 28.5}
final_state = workflow.invoke(initial_state)
print(final_state)
```

Expected output:

```text
{'temp_celsius': 28.5, 'temp_fahrenheit': 83.3}
```

## Visualize the graph

In a notebook, render and display the graph as a Mermaid-generated PNG:

```python
from IPython.display import Image, display

display(Image(workflow.get_graph().draw_mermaid_png()))
```

The PNG renderer may need an internet connection to access its Mermaid rendering
service. To view the Mermaid diagram source as text instead:

```python
print(workflow.get_graph().draw_mermaid())
```
