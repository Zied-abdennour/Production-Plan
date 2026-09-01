workplaces = [
    "WP1",
    "WP2",
    "WP3"
]

operation_workplaces = {
    "Op1": ["WP1", "WP2"],
    "Op2": ["WP2", "WP3"],
    "Op3": ["WP1", "WP3"]
}

product_operations = {
    "ProductA": ["Op1", "Op2", "Op3"],
    "ProductB": ["Op1", "Op3"]
}

rates = {
    "Op1_ProductA": 4,
    "Op2_ProductA": 3,
    "Op3_ProductA": 2,

    "Op1_ProductB": 5,
    "Op3_ProductB": 3
}

orders = {
    "Order1": {
        "product": "ProductA",
        "quantity": 40,
        "deadline": 50
    },

    "Order2": {
        "product": "ProductB",
        "quantity": 30,
        "deadline": 45
    },

    "Order3": {
        "product": "ProductA",
        "quantity": 25,
        "deadline": 80
    }
}