from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def solve_knapsack(matrix):
    best_items = []
    max_weight = 30
    best_ratio = -1
    while max_weight > 0 and best_ratio != 0:
        best_ratio = 0  # Reset best_ratio for each iteration
        selected_item = None
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                weight, value = matrix[i][j]
                ratio = value / weight
                if ratio > best_ratio and weight <= max_weight:
                    best_ratio = ratio
                    selected_item = (i, j)
        if selected_item:
            best_items.append(selected_item)
            max_weight -= matrix[selected_item[0]][selected_item[1]][0]
            matrix[selected_item[0]][selected_item[1]][1] = -1  # Mark selected item as used
    return best_items

@app.route('/')
def index():
    # Create a 10x10 matrix of random weights and values
    matrix = [[(random.randint(1, 10), random.randint(1, 100)) for _ in range(10)] for _ in range(10)]
    return render_template('index.html', matrix=matrix)

@app.route('/solve_knapsack', methods=['POST'])
def solve_knapsack_route():
    matrix = request.json['matrix']
    best_items = solve_knapsack(matrix)
    return jsonify({'best_items': best_items})

if __name__ == '__main__':
    app.run(debug=True)
