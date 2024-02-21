import math
import requests

def print_grid(arr):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            print(arr[i][j], end=" ")
        print()

def find_empty_location(arr, l):
    for row in range(len(arr)):
        for col in range(len(arr[0])):
            if arr[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False

def used_in_row(arr, row, num):
    return num in arr[row]

def used_in_col(arr, col, num):
    for row in arr:
        if row[col] == num:
            return True
    return False

def used_in_box(arr, startRow, startCol, num):
    size = int(math.sqrt(len(arr)))
    for i in range(size):
        for j in range(size):
            if arr[i + startRow][j + startCol] == num:
                return True
    return False

def check_location_is_safe(arr, row, col, num):
    size = int(math.sqrt(len(arr)))
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % size, col - col % size, num)

def solve_sudoku_all_solutions(arr):
    l = [0, 0]
    if not find_empty_location(arr, l):
        # Si no hay más celdas vacías, significa que hemos encontrado una solución
        print("Solución del Sudoku:")
        print_grid(arr)
        print()
        return True
    
    row = l[0]
    col = l[1]
    solutions_found = False
    
    for num in range(1, len(arr) + 1):
        if check_location_is_safe(arr, row, col, num):
            arr[row][col] = num
            # Intentamos resolver el sudoku recursivamente con esta nueva asignación
            if solve_sudoku_all_solutions(arr):
                solutions_found = True
            # Deshacemos la asignación para explorar otras posibles soluciones
            arr[row][col] = 0
            
    return solutions_found


def solve_sudoku(arr):
    l = [0, 0]
    if not find_empty_location(arr, l):
        return True
    
    row = l[0]
    col = l[1]
    
    for num in range(1, len(arr) + 1):
        if check_location_is_safe(arr, row, col, num):
            arr[row][col] = num
            if solve_sudoku(arr):
                return True
            arr[row][col] = 0
            
    return False


if __name__ == "__main__":
    api_url = "https://sudoku-api.vercel.app/api/dosuku"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        sudoku_data = response.json()
        # Acceder a la cuadrícula del sudoku dentro de la estructura de datos devuelta por la API
        grid = sudoku_data["newboard"]["grids"][0]["value"]

        grid_size = len(grid)
        op = input("1. Mostrar una solucion\n2. Mostrar todas las soluciones\n")
        if op == "1":
            print("Sudoku sin resolver:")
            print_grid(grid)
            if math.sqrt(grid_size).is_integer():
                if solve_sudoku(grid):
                    print("Solución del Sudoku:")
                    print_grid(grid)
                else:
                    print("No se encontró solución para el Sudoku proporcionado.")
            else:
                print("El Sudoku proporcionado no tiene un tamaño cuadrado válido.")
        elif op == "2":
            print("Sudoku sin resolver:")
            print_grid(grid)
            if math.sqrt(grid_size).is_integer():
                if not solve_sudoku_all_solutions(grid):
                    print("No se encontró ninguna solución para el Sudoku proporcionado.")
            else:
                print("El Sudoku proporcionado no tiene un tamaño cuadrado válido.")
    else:
        print("No se pudo obtener el Sudoku de la API.")
