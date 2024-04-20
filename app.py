from flask import Flask, render_template, request, jsonify
import random
app = Flask(__name__)
class Knapsack:
    def __init__(self):
        self.items = []
        self.dimensions = 10
        self.greedy_sol = []
        self.create_data()
        self.weight = 30


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
            for i in range(self.dimensions):
                for j in range(self.dimensions):
                    weight = self.items[i][j][0]
                    ratio = self.items[i][j][1] / weight
                    this_index = i * self.dimensions + j
                    if ratio > best_ratio and weight <= available_space and this_index not in self.greedy_sol:
                        best_ratio = ratio
                        selected_weight = weight
                        selected_index = this_index
            if selected_index != -1:
                available_space -= selected_weight
                self.greedy_sol.append(selected_index)


@app.route('/')
def index():
    knapsack = Knapsack()
    knapsack.greedy()
    for row in knapsack.items:
        print(row)
    for row in knapsack.greedy_sol:
        print(row)
    return render_template('index.html', knapsack=knapsack)


@app.route('/recalculate', methods=['POST'])
def recalculate():
    knapsack = Knapsack()
    knapsack.greedy()
    # package data for html
    recalculated_data = {'items': knapsack.items, "greedy_solution": knapsack.greedy_sol}
    return jsonify(recalculated_data)


if __name__ == '__main__':
    app.run(debug=True)