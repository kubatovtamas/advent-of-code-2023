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
var pad int = 2

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
		matrix[i] = make([]rune, N+pad) // pad left and right
	}

	return matrix
}

func slideMatrix(matrix [][]rune) {
	matrix[0], matrix[1], matrix[2] = matrix[1], matrix[2], make([]rune, N)
}

func printMatrix(matrix [][]rune) {
	for _, row := range matrix {
		for _, ch := range row {
			if ch == '\u0000' {
				fmt.Printf("X")
			} else {
				fmt.Printf("%c", ch)
			}
		}
		fmt.Println()
	}
	fmt.Println()
}

func padLineLeftAndRight(line string) []rune {
	lineRunes := []rune(line)
	paddedLength := len(lineRunes) + pad
	paddedLine := make([]rune, paddedLength)

	copy(paddedLine[1:], lineRunes)

	return paddedLine
}

func main() {
	part, mode := getArgs()

	file := readInput(mode)
	defer file.Close()

	if part == 1 {
		var matrix [][]rune
		var firstLine string
		matrixIdxToUpdate := 2

		scanner := bufio.NewScanner(file)

		// 1. Init matrix, pad first line
		if scanner.Scan() {
			firstLine = scanner.Text()
			matrix = initMatrix(firstLine)
		}

		matrix[matrixIdxToUpdate] = padLineLeftAndRight(firstLine)
		slideMatrix(matrix)

		do := true
		for {
			var line string

			if scanner.Scan() {
				line = scanner.Text()
			} else {
				line = string(make([]rune, N))
				matrix[matrixIdxToUpdate] = make([]rune, N)

				do = false
			}

			matrix[matrixIdxToUpdate] = padLineLeftAndRight(line)
			printMatrix(matrix)

			// do the processing here

			slideMatrix(matrix)

			if !do {
				break
			}
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
