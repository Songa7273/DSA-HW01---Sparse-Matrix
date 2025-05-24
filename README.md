# Sparse Matrix Operations

This project provides a Python implementation for performing operations (addition, subtraction, multiplication) on sparse matrices. The matrices are loaded from files, and results are saved to output files.

## Project Structure

```
code/
  src/
    main.py
    output/
      addition_result.txt
      multiplication_result.txt
      subtraction_result.txt
sample_inputs/
  easy_sample_01_2 (1).txt
  easy_sample_01_3.txt
  easy_sample_02_1 (1).txt
  easy_sample_02_2 (1).txt
  test1.txt
  test2.txt
```

## Usage

1. **Prepare Input Files:**  
   Place your matrix files in the `sample_inputs/` directory or specify their paths when prompted.  
   Each matrix file should have the following format:
   ```
   rows=3
   cols=3
   (0, 0, 1)
   (1, 2, 5)
   (2, 1, 3)
   ```
   - The first line specifies the number of rows.
   - The second line specifies the number of columns.
   - Each subsequent line specifies a non-zero entry in the format `(row, col, value)`.

2. **Run the Program:**  
   Navigate to the `code/src/` directory and run:
   ```sh
   python main.py
   ```
   Follow the prompts to select the operation and provide input file paths.

3. **Output:**  
   Results are saved in the `output/` directory as:
   - `addition_result.txt`
   - `subtraction_result.txt`
   - `multiplication_result.txt`

## Features

- Efficient sparse matrix representation using Python dictionaries.
- Supports addition, subtraction, and multiplication of matrices.
- Input validation and error handling for file formats and matrix dimensions.

## Example

**Input file (`sample_inputs/test1.txt`):**
```
rows=2
cols=2
(0, 0, 1)
(1, 1, 2)
```

**Output file (`code/src/output/addition_result.txt`):**
```
rows=2
cols=2
(0, 0, 2)
(1, 1, 4)
```

## Requirements

- Python 3.x

## License

THis is an  educational project.
