package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

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

func calcDailyScore(numWinningNumbers int) int {
	if numWinningNumbers == 0 {
		return 0
	}

	return 1 << (numWinningNumbers - 1)
}

func contains(slice []int, num int) bool {
	for _, v := range slice {
		if v == num {
			return true
		}
	}
	return false
}

func preprocessLine(line string, pattern *regexp.Regexp) string {
	line = line[len("Card "):]
	line = pattern.ReplaceAllString(line, " ")

	return line
}

func extractStringInfo(line string) (gameId string, winnerPart string, havePart string) {
	groups := strings.Split(line, ": ")
	// line = groups[1]
	gameId, line = groups[0], groups[1]

	cardGroups := strings.Split(line, " | ")
	winnerPart, havePart = cardGroups[0], cardGroups[1]

	return
}

func convertToNumSlices(winnerPart string, havePart string) (winnerNums []int, haveNums []int) {
	winnerSlice := strings.Split(winnerPart, " ")
	haveSlice := strings.Split(havePart, " ")

	winnerNums = make([]int, len(winnerSlice))
	haveNums = make([]int, len(haveSlice))

	for i, val := range winnerSlice {
		numericVal, err := strconv.Atoi(val)
		if err != nil {
			log.Fatalf("cannot convert %v to int", val)
		}

		winnerNums[i] = numericVal
	}

	for i, val := range haveSlice {
		numericVal, err := strconv.Atoi(val)
		if err != nil {
			log.Fatalf("cannot convert %v to int", val)
		}

		haveNums[i] = numericVal
	}

	return
}

func getNumOfWinningNums(winnerNums []int, haveNums []int) int {
	numWinningNumbers := 0
	for _, num := range haveNums {
		if contains(winnerNums, num) {
			numWinningNumbers++
		}
	}

	return numWinningNumbers
}

func convertGameIdToInt(gameId string) int {
	gameIdInt, err := strconv.Atoi(strings.TrimSpace(gameId))
	if err != nil {
		log.Fatalf("cannot convert game id '%v' to int", gameId)
	}

	return gameIdInt
}

func main() {
	part, mode := getArgs()

	file := readInput(mode)
	defer file.Close()

	if part == 1 {
		solution := 0

		multipleWhitespacePattern, err := regexp.Compile(`\s{2,}`)
		if err != nil {
			log.Fatal(err)
		}

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Text()

			line = preprocessLine(line, multipleWhitespacePattern)

			// gameId, winnerPart, havePart := extractStringInfo(line)
			_, winnerPart, havePart := extractStringInfo(line)

			winnerNums, haveNums := convertToNumSlices(winnerPart, havePart)

			numWinningNumbers := getNumOfWinningNums(winnerNums, haveNums)

			dailyScore := calcDailyScore(numWinningNumbers)

			solution += dailyScore
		}

		fmt.Println("SOLUTION:", solution)
	}

	if part == 2 {
		solution := 0
		gameIdQuantity := make(map[int]int)

		multipleWhitespacePattern, err := regexp.Compile(`\s{2,}`)
		if err != nil {
			log.Fatal(err)
		}

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Text()

			line = preprocessLine(line, multipleWhitespacePattern)

			gameIdStr, winnerPart, havePart := extractStringInfo(line)

			winnerNums, haveNums := convertToNumSlices(winnerPart, havePart)

			numWinningNumbers := getNumOfWinningNums(winnerNums, haveNums)

			gameId := convertGameIdToInt(gameIdStr)

			processTimes := gameIdQuantity[gameId] + 1 // default is zero, but we need default 1

			// Add how many of the current card we have
			solution += processTimes

			for j := 0; j < numWinningNumbers; j++ {
				// For the next cards, increase quantity
				idx := gameId + j + 1
				gameIdQuantity[idx] += processTimes
			}

		}

		fmt.Println("SOLUTION:", solution)
	}
}
