from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


class Knapsack:
    def __init__(self):
        self.items = []
        self.dimensions = 4
        self.greedy_sol = []
        self.create_data()
        self.weight = 50


    def create_data(self):
        for i in range(self.dimensions):
            row = []
            for j in range(self.dimensions):
                weight = random.randint(1, 20)
                value = random.randint(1, 20)
                row.append((weight, value))
            self.items.append(row)


    def greedy(self):
        ratio = []

        for i in range(self.dimensions):
            row = [False] * self.dimensions
            self.greedy_sol.append(row)

        index = 0
        # creates 1d array of ratios
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                # array contains index value and ratio
                ratio.append((index, self.items[i][j][1]/self.items[i][j][0]))
                index += 1

        # sorts by ratio
        ratio.sort(key=lambda x : x[1], reverse = True)

        avaliable_space = self.weight

        for i in range(len(ratio)):

            # get 2d equivalent of indexes
            row = ratio[i][0] // self.dimensions
            col = ratio[i][0] % self.dimensions

            if(avaliable_space - self.items[row][col][0] >= 0):
                avaliable_space = avaliable_space - self.items[row][col][0]
                self.greedy_sol[row][col] = True

        print(ratio)


@app.route('/')
def index():
    knapsack = Knapsack()
    for row in knapsack.items:
        print(row)

    knapsack.greedy()

    for row in knapsack.greedy_sol:
        print(row)

    return render_template('index.html', knapsack=knapsack)


if __name__ == '__main__':
    app.run(debug=True)
