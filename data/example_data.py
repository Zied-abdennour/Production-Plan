workplaces = [
    "WP1",
    "WP2",
    "WP3",
    "WP4",
    "WP5"
]

operation_workplaces = {
    "Op1": ["WP1", "WP2"],
    "Op2": ["WP2", "WP3"],
    "Op3": ["WP3", "WP4"],
    "Op4": ["WP4", "WP5"]
}

product_operations = {
    "Controller": ["Op1", "Op2", "Op3"],
    "Sensor": ["Op1", "Op3", "Op4"],
    "Module": ["Op2", "Op3", "Op4"]
}

rates = {
    "Op1_Controller": 4,
    "Op2_Controller": 3,
    "Op3_Controller": 2.5,

    "Op1_Sensor": 5,
    "Op3_Sensor": 3,
    "Op4_Sensor": 4,

    "Op2_Module": 4,
    "Op3_Module": 2.5,
    "Op4_Module": 3
}

orders = {
    "Order1": {
        "product": "Controller",
        "quantity": 120,
        "deadline": 100
    },

    "Order2": {
        "product": "Sensor",
        "quantity": 150,
        "deadline": 130
    },

    "Order3": {
        "product": "Module",
        "quantity": 100,
        "deadline": 120
    },

    "Order4": {
        "product": "Controller",
        "quantity": 90,
        "deadline": 180
    },

    "Order5": {
        "product": "Sensor",
        "quantity": 110,
        "deadline": 210
    },

    "Order6": {
        "product": "Module",
        "quantity": 130,
        "deadline": 230
    }
}