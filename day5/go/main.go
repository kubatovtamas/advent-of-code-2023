package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
	// "strings"
)

type State int

const (
	ListSeeds State = iota
	SeedToSoil
	SoilToFertilizer
	FertilizerToWater
	WaterToLight
	LightToTemperature
	TemperatureToHumidity
	HumidityToLocation
)

type LineType int

const (
	SeedsLine LineType = iota
	MapLine
	NumLine
)

type MappingInterval struct {
	src    int
	dest   int
	length int
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

func (s State) String() string {
	switch s {
	case ListSeeds:
		return "ListSeeds"
	case SeedToSoil:
		return "SeedToSoil"
	case SoilToFertilizer:
		return "SoilToFertilizer"
	case FertilizerToWater:
		return "FertilizerToWater"
	case WaterToLight:
		return "WaterToLight"
	case LightToTemperature:
		return "LightToTemperature"
	case TemperatureToHumidity:
		return "TemperatureToHumidity"
	case HumidityToLocation:
		return "HumidityToLocation"
	default:
		return "Unknown"
	}
}

func getLineType(line string) (lineType LineType) {
	if line[:5] == "seeds" {
		return SeedsLine
	}
	if line[len(line)-1] == ':' {
		return MapLine
	}

	return NumLine
}

func strToIntSlice(str string) []int {
	strs := strings.Split(str, " ")

	nums := make([]int, len(strs))
	for i := 0; i < len(strs); i++ {
		num, err := strconv.Atoi(strs[i])
		if err != nil {
			log.Fatalf("cannot convert %s to int", strs[i])
		}

		nums[i] = num
	}

	return nums
}

func parseSeeds(line string) []int {
	numsPart := line[7:]
	return strToIntSlice(numsPart)
}

func updateMappingsForCurrState(dest, src, length int, state State, mappings *[7][]MappingInterval) {
	nth := int(state) - 1 // will never receive ListSeeds map, needed for correct indexing
	mappingForCurrState := &mappings[nth]

	newMapping := MappingInterval{src, dest, length}
	*mappingForCurrState = append(*mappingForCurrState, newMapping)
}

func getNextValueForKey(key int, mappings []MappingInterval) int {
	for _, interval := range mappings {
		if interval.src <= key && key < interval.src+interval.length {
			diff := key - interval.src
			return interval.dest + diff
		}
	}
	return key
}

func getMinLocationForSeeds(seeds []int, mappings [7][]MappingInterval) int {
	min := math.MaxInt32
	for _, seed := range seeds {
		key := seed

		for _, currMappings := range mappings {
			key = getNextValueForKey(key, currMappings)
		}

		if key < min {
			min = key
		}
	}
	return min
}
func main() {
	part, mode := getArgs()

	file := readInput(mode)
	defer file.Close()

	if part == 1 {
		var seeds []int
		mappings := [7][]MappingInterval{}

		currentState := ListSeeds

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Text()

			if line == "" {
				continue
			}

			lineType := getLineType(line)

			switch lineType {
			case SeedsLine:
				seeds = parseSeeds(line)

			case MapLine:
				currentState++
				continue

			case NumLine:
				nums := strToIntSlice(line)
				dest, src, length := nums[0], nums[1], nums[2]

				updateMappingsForCurrState(dest, src, length, currentState, &mappings)
			}
		}

		minLocation := getMinLocationForSeeds(seeds, mappings)

		fmt.Println("SOLUTION:", minLocation)
	}
}
