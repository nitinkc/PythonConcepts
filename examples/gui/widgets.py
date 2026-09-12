from dataclasses import dataclass

import ipywidgets as widgets


@dataclass(frozen=True, slots=True)
class Order:
    quantity: int
    category: str
    notes: str


def format_order(order: Order) -> str:
    suffix = f" Notes: {order.notes}" if order.notes else ""
    return f"Submitted {order.quantity} {order.category} item(s).{suffix}"


def create_order_form() -> widgets.Widget:
    quantity = widgets.IntSlider(
        value=1,
        min=1,
        max=20,
        description="Quantity",
        continuous_update=False,
    )
    category = widgets.Dropdown(
        options=[("Books", "books"), ("Music", "music"), ("Software", "software")],
        description="Category",
    )
    notes = widgets.Textarea(description="Notes")
    submit = widgets.Button(description="Submit", button_style="primary")
    output = widgets.Output()

    def handle_submit(button: widgets.Button) -> None:
        order = Order(quantity.value, category.value, notes.value.strip())
        with output:
            output.clear_output()
            print(format_order(order))

    submit.on_click(handle_submit)
    return widgets.VBox(
        [
            widgets.HTML("<h3>Order form</h3>"),
            widgets.HBox([quantity, category]),
            notes,
            submit,
            output,
        ],
        layout=widgets.Layout(max_width="700px"),
    )
