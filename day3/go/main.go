package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"unicode"
)

type Row []rune
type Matrix struct {
	Data              []Row
	N                 int
	M                 int
	Pad               int
	MatrixIdxToUpdate int
}

func getArgs() (int, string) {
	if len(os.Args) != 3 {
		log.Fatal("Usage: go run main.go <1 or 2> <full or example>")
	}

	part, err := strconv.Atoi(os.Args[1])
	if err != nil || (part != 1 && part != 2) {
		log.Fatal("First argument must be either 1 or 2")
	}

	mode := os.Args[2]
	// if mode != "example" && mode != "full" {
	// 	log.Fatal("Second argument must be either example or full")
	// }

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

func padLineLeftAndRight(line string, pad int) []rune {
	lineRunes := []rune(line)
	paddedLength := len(lineRunes) + pad
	paddedLine := make([]rune, paddedLength)

	copy(paddedLine[pad/2:], lineRunes)

	return paddedLine
}

func runeSliceToInt(runes []rune) int {
	result := 0
	for _, r := range runes {
		if r < '0' || r > '9' {
			log.Fatalf("invalid rune: %q is not a digit", r)
		}
		result = result*10 + int(r-'0')
	}
	return result
}

func getSurroundingIndicesForNum(begin, end int) [][]int {
	length := end - begin + 1

	a := make([]int, length+2)
	c := make([]int, length+2)

	for i := 0; i < length+2; i++ {
		a[i] = begin - 1 + i
		c[i] = a[i]
	}

	b := []int{begin - 1, end + 1}

	return [][]int{a, b, c}
}

func isValidSymbol(r rune) bool {
	if r != '\u0000' && r != '.' {
		return true
	}

	return false
}
func checkSurroundingsHaveSymbol(matrix *Matrix, surroundingIndices [][]int) bool {
	for rowIdx, row := range surroundingIndices {
		for _, colIdx := range row {
			if isValidSymbol(matrix.Data[rowIdx][colIdx]) {
				return true
			}
		}
	}

	return false
}

func newMatrix(line string) *Matrix {
	width := len(line)
	height := 3

	matrix := Matrix{
		Data:              make([]Row, height),
		N:                 width,
		M:                 height,
		Pad:               2,
		MatrixIdxToUpdate: 2,
	}

	for i := range matrix.Data {
		matrix.Data[i] = make(Row, (matrix.N + matrix.Pad))
	}

	return &matrix
}

func (m *Matrix) slide() {
	m.Data[0], m.Data[1] = m.Data[1], m.Data[2]
	m.Data[2] = make([]rune, m.N)
}

func (m Matrix) print() {
	emptyWhiteBox := '\u25A1'
	for _, row := range m.Data {
		for _, ch := range row {
			if ch == '\u0000' {
				fmt.Printf("%c", emptyWhiteBox)
			} else {
				fmt.Printf("%c", ch)
			}
		}
		fmt.Println()
	}
	fmt.Println()
}

func (m *Matrix) update(withRow Row) {
	m.Data[m.MatrixIdxToUpdate] = withRow
}

func main() {
	part, mode := getArgs()

	file := readInput(mode)
	defer file.Close()

	if part == 1 {
		sum := 0
		var matrix *Matrix
		var firstLine string

		scanner := bufio.NewScanner(file)

		// 1. Init matrix
		if scanner.Scan() {
			firstLine = scanner.Text()
			matrix = newMatrix(firstLine)
		}

		// 2. Set up the padding of first row of the matrix
		matrix.update(padLineLeftAndRight(firstLine, matrix.Pad))
		matrix.slide()

		do := true
		lineNum := 1
		for {
			var line string

			// 3. Read lines of input, do one more padding line when no more input
			if scanner.Scan() {
				line = scanner.Text()
			} else {
				line = string(make([]rune, matrix.N))
				matrix.update(make(Row, matrix.N))

				do = false
			}

			// 4. Update the matrix with a new line
			matrix.update(padLineLeftAndRight(line, matrix.Pad))

			// 5. Check the middle line of the matrix
			var numBegin int
			var numEnd int
			isReadingNum := false
			buffer := make([]rune, 0)
			for i := matrix.Pad / 2; i <= matrix.N+matrix.Pad/2; i++ {
				ch := matrix.Data[1][i]

				if !isReadingNum && unicode.IsDigit(ch) {
					// Start reading a congiguous number
					isReadingNum = true
					numBegin = i
				}

				if isReadingNum {
					if unicode.IsDigit(ch) {
						// Keep adding to the buffer, it's still the same number
						buffer = append(buffer, ch)
					} else {
						// End of a contiguous number
						isReadingNum = false
						numEnd = i - 1

						surroundings := getSurroundingIndicesForNum(numBegin, numEnd)
						hasSymbolSurrounding := checkSurroundingsHaveSymbol(matrix, surroundings)

						if hasSymbolSurrounding {
							currentNum := runeSliceToInt(buffer)
							sum += currentNum
						}

						// always empty the buffer
						buffer = make([]rune, 0)
					}
				}
			}

			// 6. Slide the matrix one row
			matrix.slide()

			if !do {
				break
			}
			lineNum++
		}

		fmt.Println("SOLUTION:", sum)
	}

	if part == 2 {
		scanner := bufio.NewScanner(file)

		for scanner.Scan() {
			line := scanner.Text()
			fmt.Println(line)
		}
	}
}
