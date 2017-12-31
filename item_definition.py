class Item:
    """Base Type for all in-game items"""
    def __init__(self, name, production_cost, quantity):
        self.d_name = name
        self.d_production_cost = production_cost
        self.d_quantity = quantity
    def cost(self):
        """Returns the production cost of this item"""
        total_cost = {}
        if self.d_production_cost:
            for prod in self.d_production_cost:
                cost = prod.cost()
                for item in cost:
                    if item in total_cost:
                        total_cost[item] += cost[item] / self.d_quantity
                    else:
                        total_cost[item] = cost[item]  / self.d_quantity
        else:
            total_cost[self.d_name] = 1

        return total_cost
    def print(self):
        """Print the cost of this Item"""
        cost = self.cost()
        print("To produce " + str(self.d_quantity) + " " + self.d_name +
              " it costs:")
        if len(cost) == 1:
            print("Nothing (Base type)")
        else:
            for item in cost:
                print(str(cost[item] * self.d_quantity) + " " + item + ", ", end="")
            print("")