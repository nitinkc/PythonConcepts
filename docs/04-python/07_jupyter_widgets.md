# Interactive GUI widgets in Jupyter

`ipywidgets` adds interactive controls to Jupyter notebooks. It is best suited to exploratory tools, teaching interfaces, and small data dashboards—not desktop applications or public web applications.

## Setup

Install the repository dependencies and start JupyterLab or another compatible notebook frontend:

```bash
python -m pip install -r requirements.txt
jupyter lab
```

A widget has Python-side state synchronized with a browser view. Displaying and interacting with widgets therefore requires a live notebook kernel.

You can also use the <a href="../../lab/lab/index.html?path=GUI_Widgets.ipynb">static browser lab</a> without installing Python locally.

## Automatic controls with `interact`

`interact` selects a control from the supplied default value:

```python
from ipywidgets import fixed, interact

@interact(count=(0, 20, 1), uppercase=False, text="Python")
def preview(count: int, uppercase: bool, text: str) -> str:
    value = text.upper() if uppercase else text
    return " ".join([value] * count)
```

Common abbreviations are:

| Value | Generated control |
|---|---|
| `True` or `False` | Checkbox |
| Integer | Integer slider |
| Float | Float slider |
| String | Text box |
| List | Dropdown using the list values |
| Dictionary | Dropdown using labels and values |
| `(minimum, maximum, step)` | Bounded slider |
| `fixed(value)` | Argument with no visible control |

Use `interactive` when you need the resulting container, its child controls, or its latest result.

```python
from IPython.display import display
from ipywidgets import interactive

panel = interactive(pow, base=(1, 10), exp=(1, 5))
display(panel)
print(panel.kwargs)
```

## Explicit controls

Create widgets directly when labels, ranges, formatting, or initial values matter.

```python
import ipywidgets as widgets

quantity = widgets.IntSlider(
    value=1,
    min=1,
    max=20,
    step=1,
    description="Quantity",
    continuous_update=False,
)
category = widgets.Dropdown(
    options=[("Books", "books"), ("Music", "music")],
    description="Category",
)
notes = widgets.Textarea(description="Notes")
```

Useful controls include `IntSlider`, `FloatSlider`, `Text`, `Textarea`, `Checkbox`, `Dropdown`, `RadioButtons`, `SelectMultiple`, `Button`, `DatePicker`, `FileUpload`, and `Output`.

## Observe state changes

Widget attributes such as `value`, `description`, and `disabled` are observable traits.

```python
output = widgets.Output()


def show_quantity(change):
    with output:
        output.clear_output()
        print(f"Quantity: {change['new']}")


quantity.observe(show_quantity, names="value")
widgets.VBox([quantity, output])
```

An observer receives a change dictionary containing keys such as `name`, `old`, `new`, and `owner`. Restrict observation with `names="value"` to avoid responding to unrelated changes.

## Handle button clicks

```python
submit = widgets.Button(description="Submit", button_style="primary")
status = widgets.Output()


def submit_form(button):
    with status:
        status.clear_output()
        print(f"Submitted {quantity.value} {category.value} item(s)")


submit.on_click(submit_form)
widgets.VBox([quantity, category, notes, submit, status])
```

Write output inside an `Output` widget so repeated interactions update a predictable region instead of filling the notebook with cells.

## Layout and composition

Compose controls with `HBox`, `VBox`, `GridBox`, `Tab`, and `Accordion`.

```python
form = widgets.VBox(
    [
        widgets.HTML("<h3>Order</h3>"),
        widgets.HBox([quantity, category]),
        notes,
        submit,
        status,
    ],
    layout=widgets.Layout(max_width="700px"),
)
form
```

Use the `layout` attribute for dimensions and positioning and the `style` attribute for widget-specific presentation. Keep styling modest so the interface remains usable across notebook themes.

## Link widget values

```python
slider = widgets.IntSlider(min=0, max=100)
progress = widgets.IntProgress(min=0, max=100)
link = widgets.link((slider, "value"), (progress, "value"))
widgets.VBox([slider, progress])
```

Call `link.unlink()` when the synchronization is no longer needed. `jslink` performs synchronization in the browser and can remain responsive when the kernel is busy.

## Reusable composite widgets

A reusable interface can extend `VBox` and expose normal widget traits.

```python
class LabeledCounter(widgets.VBox):
    def __init__(self, label: str, minimum: int = 0, maximum: int = 10):
        self.slider = widgets.IntSlider(min=minimum, max=maximum)
        self.readout = widgets.Label()
        self.slider.observe(self._update, names="value")
        super().__init__([widgets.HTML(f"<b>{label}</b>"), self.slider, self.readout])
        self._update({"new": self.slider.value})

    def _update(self, change):
        self.readout.value = f"Current value: {change['new']}"
```

Prefer composition over building a custom browser widget. A truly custom widget requires a Python model plus a JavaScript frontend and is justified only when existing controls cannot provide the required behavior.

## Practical guidance

- Keep data processing in ordinary functions and let callbacks coordinate the UI.
- Avoid long blocking work in event handlers; display progress and run expensive work deliberately.
- Validate uploaded files and user-entered values before processing them.
- Close or unlink widgets that register long-lived callbacks when they are no longer needed.
- Use Streamlit, Panel, Dash, FastAPI, or a frontend framework when the interface must be deployed beyond notebooks.

## Experiment: separate UI from logic

The browser editor tests the ordinary Python logic that a widget callback would call. Change the validation and formatting rules, then use the full lab to render the controls.

```python { .python-runner title="Widget application logic experiment" }
from dataclasses import dataclass

@dataclass(frozen=True)
class Order:
    quantity: int
    category: str


def submit_order(quantity, category):
    if quantity < 1:
        raise ValueError("quantity must be positive")
    return Order(quantity=quantity, category=category)


for quantity in [2, 0]:
    try:
        print(submit_order(quantity, "books"))
    except ValueError as error:
        print(type(error).__name__, error)
```

<a class="md-button" href="../../lab/lab/index.html?path=GUI_Widgets.ipynb">Open the complete widget lab</a>

## Checkpoint

- Generate simple controls with `interact`.
- Choose and configure explicit widget classes.
- Respond to value changes and button clicks.
- Capture callback output with `Output`.
- Compose accessible layouts from small controls.
- Know when notebook widgets are not the right deployment choice.

**Example:** [`examples/gui/widgets.py`](https://github.com/nitinkc/PythonConcepts/blob/main/examples/gui/widgets.py)
