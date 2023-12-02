package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

var availableCubes = map[string]int{
	"red":   12,
	"green": 13,
	"blue":  14,
}

func splitOffGameId(line string) (int, string) {
	noPrefixLine := strings.TrimPrefix(line, "Game ")

	groups := strings.Split(noPrefixLine, ":")
	gameNumStr, restOfLine := groups[0], strings.Join(groups[1:], "")

	gameNum, err := strconv.Atoi(gameNumStr)
	if err != nil {
		log.Fatalf("cannot convert %s to int", gameNumStr)
	}

	return gameNum, restOfLine
}

func getGameSets(line string) []string {
	sets := strings.Split(line, ";")

	for i := 0; i < len(sets); i++ {
		sets[i] = strings.TrimSpace(sets[i])
	}

	return sets
}

func getSetCubes(set string) map[string]int {
	setCubes := make(map[string]int)

	numColorGroups := strings.Split(set, ", ")

	for _, numColor := range numColorGroups {
		elems := strings.Split(numColor, " ")

		quantStr, color := elems[0], elems[1]

		quant, err := strconv.Atoi(quantStr)
		if err != nil {
			log.Fatalf("cannot convert %s to int", quantStr)
		}

		setCubes[color] = quant
	}

	return setCubes
}

func validCubeQuantities(setCubes map[string]int) bool {
	for color, quant := range setCubes {
		if availableCubes[color] < quant {
			return false
		}
	}

	return true
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

func main() {
	part, mode := getArgs()

	file := readInput(mode)
	defer file.Close()

	if part == 1 {
		sumValidIds := 0

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Text()

			gameId, restOfLine := splitOffGameId(line)

			gameSets := getGameSets(restOfLine)
			gameIsValid := true
			for _, gameSet := range gameSets {
				setCubes := getSetCubes(gameSet)

				if !validCubeQuantities(setCubes) {
					gameIsValid = false
					break
				}
			}

			if gameIsValid {
				sumValidIds += gameId
			}
		}

		fmt.Println(sumValidIds)
	}

	if part == 2 {
		sumCubePowers := 0

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Text()

			_, restOfLine := splitOffGameId(line)

			gameSets := getGameSets(restOfLine)
			maxQuantCubes := make(map[string]int)
			for _, gameSet := range gameSets {
				setCubes := getSetCubes(gameSet)

				for color, quant := range setCubes {
					if maxQuantCubes[color] < quant {
						maxQuantCubes[color] = quant
					}
				}

			}

			powerOfCubes := 1
			for _, quant := range maxQuantCubes {
				powerOfCubes *= quant
			}

			sumCubePowers += powerOfCubes
		}

		fmt.Println(sumCubePowers)
	}
}
