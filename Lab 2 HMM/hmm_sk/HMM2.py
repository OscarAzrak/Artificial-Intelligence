
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
    print(matrix_to_string(delta_algorithm(A, B, pi, O)))

def matrix_to_string(matrix):
    # Convert the matrix to a string
    result = ""
    for i in range(len(matrix)):
        result += str(matrix[i]) + " "
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

def delta_algorithm(A, B, pi, O):
    N = len(A)
    T = len(O)
    delta = []
    delta_index = []
    #initialize delta and delta_index
    for i in range(N):
        delta.append([0])
        delta_index.append([0])
    #initialize delta and delta_index for t = 1
    for i in range(N):
        delta[i][0] = pi[0][i] * B[i][O[0]]
        delta_index[i][0] = 0
    #run the delta algorithm
    for t in range(1, T):
        for i in range(N):
            max_delta = 0
            max_index = 0
            for j in range(N):
                if delta[j][t-1] * A[j][i] > max_delta:
                    max_delta = delta[j][t-1] * A[j][i]
                    max_index = j
            delta[i].append(max_delta * B[i][O[t]])
            delta_index[i].append(max_index)
    #find the max delta value
    max_delta = 0
    max_index = 0
    for i in range(N):
        if delta[i][T-1] > max_delta:
            max_delta = delta[i][T-1]
            max_index = i
    #backtrack to find the most likely state sequence
    state_sequence = []
    state_sequence.append(max_index)
    for t in range(T-1, 0, -1):
        state_sequence.append(delta_index[state_sequence[T-t-1]][t])
    state_sequence.reverse()
    return state_sequence

if __name__ == "__main__":
    main()