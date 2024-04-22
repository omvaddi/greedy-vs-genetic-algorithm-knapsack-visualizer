from flask import Flask, render_template, request, jsonify
import random
import geneticalgorithm
app = Flask(__name__)


class Knapsack:
    def __init__(self):
        self.items = []
        self.dimensions = 10

        self.greedy_sol = []
        self.greedy_weight = 0
        self.greedy_value = 0

        self.genetic_sol = []
        self.genetic_weight = 0
        self.genetic_value = 0

        self.create_data()
        self.weight = 300

    def create_data(self):
        for i in range(self.dimensions):
            row = []
            for j in range(self.dimensions):
                weight = random.randint(1, 20)
                value = random.randint(1, 20)
                row.append((weight, value))
            self.items.append(row)

    def greedy(self):
        self.greedy_sol.clear()
        selected_index = 0
        available_space = self.weight
        while selected_index != -1:
            best_ratio = float('-inf')
            selected_index = -1
            selected_weight = 0
            selected_value = 0
            for i in range(self.dimensions):
                for j in range(self.dimensions):
                    weight = self.items[i][j][0]
                    value = self.items[i][j][1]
                    ratio = self.items[i][j][1] / weight
                    this_index = (i * self.dimensions) + j
                    if ratio > best_ratio and weight <= available_space and this_index not in self.greedy_sol:
                        best_ratio = ratio
                        selected_weight = weight
                        selected_value = value
                        selected_index = this_index
            if selected_index != -1:
                available_space -= selected_weight
                self.greedy_sol.append(selected_index)
                self.greedy_weight += selected_weight
                self.greedy_value += selected_value

    # genetic algorithm implementation
    def genetic(self):
        algorithm = geneticalgorithm.GeneticAlgorithm(population_size=1000, chromosome_length=self.dimensions ** 2,
                                                      crossover_rate=0.8, mutation_rate=0.05, items=self.items,
                                                      knapsack_capacity=self.weight, tournament_size=5,
                                                      dimensions=self.dimensions)
        generations = 10
        for _ in range(generations):
            algorithm.evolve()
        temp_items = algorithm.get_items()
        self.genetic_sol = algorithm.decode()
        self.genetic_weight = sum(temp_items[i][0] for i in self.genetic_sol)
        self.genetic_value = sum(temp_items[i][1] for i in self.genetic_sol)
        if self.genetic_weight > self.weight:
            self.genetic_value = 0
        print(self.genetic_sol)


@app.route('/')
def index():
    knapsack = Knapsack()
    knapsack.greedy()
    knapsack.genetic()
    return render_template('index.html', knapsack=knapsack)


@app.route('/recalculate', methods=['POST'])
def recalculate():
    knapsack = Knapsack()
    knapsack.greedy()
    knapsack.genetic()
    # package data for html
    recalculated_data = {'items': knapsack.items, "greedy_solution": knapsack.greedy_sol,
                         "greedy_weight": knapsack.greedy_weight, "greedy_value": knapsack.greedy_value,
                         "genetic_solution": knapsack.genetic_sol, "genetic_weight": knapsack.genetic_weight,
                         "genetic_value": knapsack.genetic_value}
    return jsonify(recalculated_data)


if __name__ == '__main__':
    app.run(debug=True)
