import math
import sys

def main():
    # Read in the data
    data = sys.stdin.readlines()
    # Parse the data A, B and pi
    A = parse_matrix(data[0])
    B = parse_matrix(data[1])
    pi = parse_matrix(data[2])
    #read in the observations
    observations = data[3].split()
    O = []
    #convert the observations to integers
    for i in range(1,len(observations)):
        O.append(int(observations[i]))

    # Run the calculations
    old_log_prob = -math.inf
    iters = 0
    A, B = calculations(A, B, pi, O, iters, old_log_prob)
    # Print the results
    print(matrix_to_string(A))
    print(matrix_to_string(B))


def calculations(A, B, pi, O, iters, old_log_prob):
    c = [0 for i in range(len(O))]
    max_iter = 100
    alpha, c = forward(A, B, pi, O,c)
    beta = backward(A, B, O, c, pi)
    gamma, digamma = computeGamma(A, B, O, alpha, beta, pi)
    (A, B, pi) = reEstimate(A, B, pi, O, digamma, gamma)
    log_prob = compute_log_prob(O, c)
    iters += 1
    if (iters < max_iter) and (log_prob > old_log_prob):
        old_log_prob = log_prob
        (A, B) = calculations(A, B, pi, O, iters, old_log_prob)
    return A, B

def matrix_to_string(matrix):
    # Convert the matrix to a string
    result = ""
    result += str(len(matrix)) + " " + str(len(matrix[0])) + " "
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result += str(round(matrix[i][j],6)) + " "
        result += ""
    return result


def parse_matrix(line):
    # first value rows, second value columns

    values_list = []
    # split the line into the values
    values = line.split()
    #first value is rows
    rows = int(values[0])
    #second value is columns
    columns = int(values[1])
    #the rest of the values are the matrix values
    for i in range(2, len(values)):
        values_list.append(float(values[i]))
    matrix = []
    for i in range(rows):
        rows_m = []
        for j in range(columns):
            rows_m.append(values_list[i*columns + j])
        matrix.append(rows_m)
    return matrix
def read_data(data_list):
    row = int(data_list.pop(0))
    col = int(data_list.pop(0))
    matrix = [[0 for columns in range(col)] for rows in range(row)]
    for Mrow in range(row):
        for cols in range(col):
            matrix[Mrow][cols] = float(data_list.pop(0))
    return matrix
# forward algorithm
def forward(A, B, pi, O,c):
    # Initialize alpha and c
    alpha = [[float(0) for i in range(len(pi[0]))] for j in range(len(O))]
    # Initialize alpha and c
    for i in range(len(A)):
        alpha[i][0] = pi[0][i] * B[i][O[0]]
        c[0] += alpha[0][i]
        # Scale alpha and c
        c[0] = 1 / c[0]
    for i in range(len(A)):
        alpha[0][i] *= c[0]
    # Run the forward algorithm
    for t in range(1, len(O)):
        for i in range(len(A)):
            for j in range(len(A)):
                alpha[t][i] += alpha[t-1][j] * A[j][i]
            alpha[t][i] *= B[i][O[t]]
            c[t] += alpha[t][i]
        c[t] = 1 / c[t]
        for i in range(len(A)):
            alpha[t][i] *= c[t]
    return alpha, c

# backward algorithm

def backward(A, B, O, c, pi):
    # Initialize beta
    beta = [[float(0) for i in range(len(pi[0]))] for j in range(len(O))]
    # Initialize beta
    for i in range(len(A)):
        beta[len(O)-1][i] = c[len(O)-1]
    # Run the backward algorithm
    for t in range(len(O)-2, -1, -1):
        for i in range(len(pi[0])):
            for j in range(len(pi[0])):
                beta[t][i] += A[i][j] * B[j][O[t+1]] * beta[t+1][j]
            beta[t][i] *= c[t]
    return beta

# compute gamma
def computeGamma(A, B, O, alpha, beta, pi):
    # Initialize gamma and digamma
    gamma = [[float(0) for columns in range(len(pi[0]))] for rows in range(len(O))]
    digamma = [[[float(0) for j in range(len(pi[0]))] for columns in range(len(pi[0]))] for rows in range(len(O))]
    # Compute gamma and digamma
    for t in range(0, len(O) - 1):
        for i in range(len(pi[0])):
            for j in range(len(pi[0])):
                digamma[t][i][j] = alpha[t][i] * A[i][j] * B[j][O[t+1]] * beta[t+1][j]
                gamma[t][i] += digamma[t][i][j]


    for i in range(len(pi[0])):
        gamma[len(O)-1][i] = alpha[len(O)-1][i]
    return gamma, digamma

# re-estimate A, B and pi
def reEstimate(A, B, pi, O, digamma, gamma):
    # Re-estimate pi
    for i in range(len(A)):
        pi[0][i] = gamma[0][i]
    # Re-estimate A
    for i in range(len(pi[0])):
        denom = 0
        for t in range(len(O) - 1):
            denom += gamma[t][i]
        for j in range(len(pi[0])):
            numer = 0
            for t in range(len(O) - 1):
                numer += digamma[t][i][j]
            A[i][j] = numer / denom
    # Re-estimate B
    for i in range(len(pi[0])):
        denom = 0
        for t in range(len(O)):
            denom += gamma[t][i]
        for j in range(len(B[0])):
            numer = 0
            for t in range(len(O)):
                if O[t] == j:
                    numer += gamma[t][i]

            B[i][j] = numer / denom
    return A, B, pi

def compute_log_prob(O, c):
    log_prob = 0
    for i in range(0, len(O)):
        log_prob += math.log(c[i], 10)
    log_prob = -log_prob
    return log_prob




if __name__ == "__main__":
    main()







