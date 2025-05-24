import os

class SparseMatrix:
    def __init__(self, FilePath=None, numRows=None, numCols=None):
        self.rows = 0
        self.cols = 0
        self.matrix = {}

        if FilePath is not None:
            self._load_from_file(FilePath)
        elif numRows is not None and numCols is not None:
            if numRows <= 0 or numCols <= 0:
                raise ValueError("Matrix dimensions must be positive")
            self.rows = numRows
            self.cols = numCols
        else:
            raise ValueError("Either FilePath or numRows and numCols must be provided.")
        
    def _load_from_file(self, FilePath):
        try:
            with open(FilePath, 'r') as f:
                lines = [line.strip() for line in f if line.strip() != '']

                if len(lines) < 2 or not lines[0].startswith('rows=') or not lines[1].startswith('cols='):
                    raise ValueError("File format is incorrect. Expected 'rows=' and 'cols=' lines.")
                
                try:
                    self.rows = int(lines[0][5:])
                    self.cols = int(lines[1][5:])
                except ValueError:
                    raise ValueError("Invalid matrix dimensions in file")

                if self.rows <= 0 or self.cols <= 0:
                    raise ValueError("Matrix dimensions must be positive")

                for line_num, line in enumerate(lines[2:], start=3):
                    line = line.strip()
                    if not line.startswith('(') or not line.endswith(')'):
                        raise ValueError(f"Line {line_num}: Entries must be in format (row,col,value)")
                    
                    entry = line[1:-1].split(',')
                    if len(entry) != 3:
                        raise ValueError(f"Line {line_num}: Need exactly 3 values in parentheses")
                    
                    try:
                        row = int(entry[0].strip())
                        col = int(entry[1].strip())
                        value = int(entry[2].strip())
                    except ValueError:
                        raise ValueError(f"Line {line_num}: Row, col and value must be integers")
                    
                    if row >= self.rows or col >= self.cols or row < 0 or col < 0:
                        continue
                    
                    self.matrix[(row, col)] = value

        except IOError:
            raise ValueError(f"Could not open file: {FilePath}")
        except Exception as e:
            raise ValueError(f"Input file error: {str(e)}")

    def getItem(self, currRow, currCol):
        if currRow >= self.rows or currCol >= self.cols or currRow < 0 or currCol < 0:
            raise IndexError("Matrix index out of bounds")
        return self.matrix.get((currRow, currCol), 0)
    
    def setItem(self, currRow, currCol, value):
        if currRow >= self.rows or currCol >= self.cols or currRow < 0 or currCol < 0:
            raise IndexError("Matrix index out of bounds")
        if value != 0:
            self.matrix[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix:
            del self.matrix[(currRow, currCol)]

    def addition(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for addition.")
        
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)

        # Copy all elements from first matrix
        for (row, col), value in self.matrix.items():
            result.setItem(row, col, value)

        # Add elements from second matrix
        for (row, col), value in other.matrix.items():
            current = result.getItem(row, col)
            result.setItem(row, col, current + value)

        return result
    
    def subtraction(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for subtraction.")
        
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)

        # Copy all elements from first matrix
        for (row, col), value in self.matrix.items():
            result.setItem(row, col, value)

        # Subtract elements from second matrix
        for (row, col), value in other.matrix.items():
            current = result.getItem(row, col)
            result.setItem(row, col, current - value)

        return result
    
    def multiplication(self, other):
        if self.cols != other.rows:
            raise ValueError(f"Matrix dimensions incompatible for multiplication: {self.rows}x{self.cols} vs {other.rows}x{other.cols}")
        
        result = SparseMatrix(numRows=self.rows, numCols=other.cols)

        # Create a column-oriented view of the second matrix
        other_columns = {}
        for (row, col), value in other.matrix.items():
            if col not in other_columns:
                other_columns[col] = {}
            other_columns[col][row] = value

        # Perform multiplication
        for (i, k), a_ik in self.matrix.items():
            if k in other_columns:
                for j, b_kj in other_columns[k].items():
                    current = result.getItem(i, j)
                    result.setItem(i, j, current + a_ik * b_kj)

        return result
    
    def SaveToFile(self, FilePath):
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(FilePath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(FilePath, 'w') as f:
                f.write(f"rows={self.rows}\n")
                f.write(f"cols={self.cols}\n")
                for (row, col) in sorted(self.matrix.keys()):
                    f.write(f"({row}, {col}, {self.matrix[(row, col)]})\n")
        except IOError:
            raise ValueError(f"Could not write to file: {FilePath}")

def main():
    print("Sparse Matrix Operations")
    print("1. Add two matrices")
    print("2. Subtract two matrices")
    print("3. Multiply two matrices")

    try:
        choice = int(input("Enter your choice (1-3): "))
        if choice not in [1, 2, 3]:
            raise ValueError("Invalid choice. Please enter a number between 1 and 3.")
        
        file1 = input("Enter the path for the first matrix file: ").strip()
        file2 = input("Enter the path for the second matrix file: ").strip()

        matrix1 = SparseMatrix(file1)
        matrix2 = SparseMatrix(file2)

        # Create output directory path
        output_dir = "output"
        
        if choice == 1:
            result = matrix1.addition(matrix2)
            output_file = os.path.join(output_dir, "addition_result.txt")
        elif choice == 2:
            result = matrix1.subtraction(matrix2)
            output_file = os.path.join(output_dir, "subtraction_result.txt")
        elif choice == 3:
            result = matrix1.multiplication(matrix2)
            output_file = os.path.join(output_dir, "multiplication_result.txt")

        result.SaveToFile(output_file)
        print(f"Operation completed successfully. Result saved to {output_file}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()