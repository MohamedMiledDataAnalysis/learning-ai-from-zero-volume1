"""Exercise 28.4: the description of a new tool, get_stock, written for the model.

    python python/vol1/ch28/solutions/get_stock_schema.py
"""

import json

GET_STOCK = {
    "type": "function",
    "function": {
        "name": "get_stock",
        "description": "Number of units of an item the shop has on its shelves right now.",
        "parameters": {
            "type": "object",
            "properties": {"item": {"type": "string", "description": "Item name, e.g. 'apple'."}},
            "required": ["item"],
        },
    },
}
print(json.dumps(GET_STOCK, indent=2))
