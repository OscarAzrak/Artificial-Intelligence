import sys

def main():
    # Read in the data
    data = sys.stdin.readlines()
    # Parse the data A, B and pi
    A = parse_matrix(data[0])
    B = parse_matrix(data[1])
    pi = parse_matrix(data[2])

    # multiply pi*A
    piA = multiply_matrices(pi, A)
    #print(piA)
    # multiply pi*A*B
    piAB = multiply_matrices(piA, B)
    #print the result
    print(matrix_to_string(piAB))



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

def multiply_matrices(A, B):
    # Initialize the result matrix
    result = []
    for i in range(len(A)):
        result.append([])
        for j in range(len(B[0])):
            result[i].append(0)

    # Multiply the two matrices
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    # Return the result
    return result

def matrix_to_string(matrix):
    # Convert the matrix to a string
    result = ""
    result += str(len(matrix)) + " " + str(len(matrix[0])) + " "
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result += str(round(matrix[i][j],3)) + " "
        result += ""
    return result

if __name__ == "__main__":
    main()
