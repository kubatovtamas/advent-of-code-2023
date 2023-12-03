package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

var M int
var N int

func getArgs() (int, string) {
	if len(os.Args) != 3 {
		log.Fatal("Usage: go run main.go <1 or 2> <full or example>")
	}

	part, err := strconv.Atoi(os.Args[1])
	if err != nil || (part != 1 && part != 2) {
		log.Fatal("First argument must be either 1 or 2")
	}

	mode := os.Args[2]
	if mode != "example" && mode != "full" {
		log.Fatal("Second argument must be either example or full")
	}

	return part, mode
}

func readInput(name string) *os.File {
	path := fmt.Sprintf("../input/%s", name)
	file, err := os.Open(path)
	if err != nil {
		log.Fatalf("failed to open file: %s", err)
	}

	return file
}

func initMatrix(line string) [][]rune {
	N = len(line)
	M = 3

	matrix := make([][]rune, M)
	for i := range matrix {
		matrix[i] = make([]rune, N)
	}

	return matrix
}

func slideMatrix(matrix [][]rune) {
	matrix[0], matrix[1], matrix[2] = matrix[1], matrix[2], make([]rune, N)
}

func printMatrix(matrix [][]rune) {
	for _, row := range matrix {
		for _, ch := range row {
			fmt.Printf("%c", ch)
		}
		fmt.Println()
	}
	fmt.Println()
}

func updateMatrix(matrix [][]rune, line string, rowIdx int) {
	matrix[rowIdx] = []rune(line)

	if rowIdx == 3 {
		slideMatrix(matrix)
	}
}

func main() {
	part, mode := getArgs()

	file := readInput(mode)
	defer file.Close()

	if part == 1 {
		var matrix [][]rune
		matrixIdxToUpdate := 0

		currLine := 1
		scanner := bufio.NewScanner(file)

		for scanner.Scan() {
			line := scanner.Text()

			// Read first line and initialize the matrix
			if currLine == 1 {
				matrix = initMatrix(line)
			}
			matrix[matrixIdxToUpdate] = []rune(line)
			// updateMatrix(matrix, line, matrixIdxToUpdate)

			printMatrix(matrix)

			matrixIdxToUpdate++
			if matrixIdxToUpdate >= 3 {
				slideMatrix(matrix)
				matrixIdxToUpdate = 2
			}

			currLine++
		}
	}

	if part == 2 {
		scanner := bufio.NewScanner(file)

		for scanner.Scan() {
			line := scanner.Text()
			fmt.Println(line)
		}
	}
}
