package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"unicode"
)

type stringComparisonFunc func(string, string) bool
type modifyStringFunc func(string) string

var stringMap = map[string]int{
	"one":   1,
	"two":   2,
	"three": 3,
	"four":  4,
	"five":  5,
	"six":   6,
	"seven": 7,
	"eight": 8,
	"nine":  9,
}

var runeMap = map[rune]int{
	'0': 0,
	'1': 1,
	'2': 2,
	'3': 3,
	'4': 4,
	'5': 5,
	'6': 6,
	'7': 7,
	'8': 8,
	'9': 9,
}

func removeFirstChar(s string) string {
	if len(s) > 0 {
		return s[1:]
	}
	return s
}

func removeLastChar(s string) string {
	if len(s) > 0 {
		return s[:len(s)-1]
	}
	return s
}

func extractNum(line string, stringCompare stringComparisonFunc, stringShorten modifyStringFunc) (int, error) {
	for len(line) > 0 {
		for k, v := range runeMap {
			if stringCompare(line, string(k)) {
				return v, nil
			}
		}

		for k, v := range stringMap {
			if stringCompare(line, k) {
				return v, nil
			}
		}

		line = stringShorten(line)
	}

	return 0, fmt.Errorf("no number could be extracted from %s", line)
}

func getArg() int {
	if len(os.Args) != 2 {
		log.Fatal("Usage: go run main.go <1 or 2>")
	}

	arg, err := strconv.Atoi(os.Args[1])
	if err != nil || (arg != 1 && arg != 2) {
		log.Fatal("Argument must be either 1 or 2")
	}

	return arg
}

func readInput(name string) *os.File {
	path := fmt.Sprintf("../input/%s", name)
	file, err := os.Open(path)
	if err != nil {
		log.Fatalf("failed to open file: %s", err)
	}

	return file
}

func main() {
	part := getArg()

	file := readInput("full")
	defer file.Close()

	if part == 1 {
		scanner := bufio.NewScanner(file)

		sum := 0
		for scanner.Scan() {
			line := scanner.Text()
			localLineNums := make([]int, 0)

			for _, ch := range line {
				if unicode.IsDigit(ch) {
					num := int(ch - '0')
					localLineNums = append(localLineNums, num)
				}
			}

			firstNum, lastNum := localLineNums[0], localLineNums[len(localLineNums)-1]
			sum += firstNum*10 + lastNum
		}

		fmt.Println(sum)
	}

	if part == 2 {
		sum := 0

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Text()

			firstNum, err := extractNum(line, strings.HasPrefix, removeFirstChar)
			if err != nil {
				log.Fatalf("Error: %s", err.Error())
			}

			lastNum, err := extractNum(line, strings.HasSuffix, removeLastChar)
			if err != nil {
				log.Fatalf("Error: %s", err.Error())
			}

			sum += firstNum*10 + lastNum
		}

		fmt.Println(sum)
	}

}
