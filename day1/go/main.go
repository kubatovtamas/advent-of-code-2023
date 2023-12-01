package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"unicode"
)

func main() {
	file, err := os.Open("../input/full")
	if err != nil {
		log.Fatalf("failed to open file: %s", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	lineNums := make([][]int, 0)
	lineNum := 0

	for scanner.Scan() {
		line := scanner.Text()
		localLineNums := make([]int, 0)

		for _, ch := range line {
			if unicode.IsDigit(ch) {
				num := int(ch - '0')
				localLineNums = append(localLineNums, num)
			}
		}

		lineNums = append(lineNums, localLineNums)

		lineNum++
	}

	sum := 0
	for _, lineNums := range lineNums {
		firstCh := lineNums[0]
		secondCh := lineNums[len(lineNums)-1]

		curr := firstCh*10 + secondCh

		sum += curr
	}

	fmt.Println(sum)

}
