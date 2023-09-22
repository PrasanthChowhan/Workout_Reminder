class PythonPizzeria:
    # Class variable - Shared among all instances
    num_pizzas_sold = 0

    def __init__(self, pizza_name, pizza_price):
        self.pizza_name = pizza_name
        self.pizza_price = pizza_price
        # Every time a pizza is created, we update the class variable
        PythonPizzeria.num_pizzas_sold += 1

    # @classmethod example: Creating a special pizza following a shared recipe
    @classmethod
    def create_special_pizza(cls):
        special_pizza = cls("Special Pizza", 15.99)
        return special_pizza

    # @staticmethod example: Slicing a pizza (no need for instance-specific data)
    @staticmethod
    def slice_pizza():
        print("Slicing the pizza!")

# Creating an instance of PythonPizzeria
pizza1 = PythonPizzeria("Margherita", 12.99)
pizza2 = PythonPizzeria("Pepperoni", 14.99)

# Using the @classmethod to create a special pizza
special_pizza = PythonPizzeria.create_special_pizza()
print(f"Special Pizza: {special_pizza.pizza_name}, Price: ${special_pizza.pizza_price}")

# Using the @staticmethod to slice a pizza
pizza1.slice_pizza()  # Output: Slicing the pizza!
pizza2.slice_pizza()  # Output: Slicing the pizza!

# Accessing the class variable
print(f"Total Pizzas Sold: {PythonPizzeria.num_pizzas_sold}")  # Output: Total Pizzas Sold: 3
