package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
	// "strings"
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

type State int
type LineType int

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

const (
	SeedsLine LineType = iota
	MapLine
	NumLine
)

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

func initSeeds(line string) map[int]int {
	seeds := parseSeeds(line)
	seedToLoc := make(map[int]int)

	for _, seed := range seeds {
		seedToLoc[seed] = -1
	}

	return seedToLoc
}

func updateMapForCurrState(dest, src, length int, state State, maps [7]*map[int]int) {
	nthMap := int(state) - 1 // will never receive ListSeeds map, needed for correct indexing

	mapForCurrentState := maps[nthMap]

	for i := 0; i < length; i++ {
		(*mapForCurrentState)[src+i] = dest + i
	}
}

func prettyPrintMaps(maps [7]*map[int]int) {
	mapNames := []string{
		"SeedToSoil",
		"SoilToFertilizer",
		"FertilizerToWater",
		"WaterToLight",
		"LightToTemperature",
		"TemperatureToHumidity",
		"HumidityToLocation",
	}

	for i, m := range maps {
		fmt.Println(mapNames[i] + ":")
		// Collect and sort the keys
		var keys []int
		for key := range *m {
			keys = append(keys, key)
		}
		sort.Ints(keys)

		// Print sorted key-value pairs
		for _, key := range keys {
			fmt.Printf("  %d -> %d\n", key, (*m)[key])
		}
		fmt.Println()
	}
}

func main() {
	part, mode := getArgs()

	file := readInput(mode)
	defer file.Close()

	if part == 1 {
		var seedToLocation map[int]int

		seedToSoil := make(map[int]int)
		soilToFertilizer := make(map[int]int)
		fertilizerToWater := make(map[int]int)
		waterToLight := make(map[int]int)
		lightToTemperature := make(map[int]int)
		temperatureToHumidity := make(map[int]int)
		humidityToLocation := make(map[int]int)
		maps := [7]*map[int]int{
			&seedToSoil,
			&soilToFertilizer,
			&fertilizerToWater,
			&waterToLight,
			&lightToTemperature,
			&temperatureToHumidity,
			&humidityToLocation,
		}

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
				seedToLocation = initSeeds(line)

			case MapLine:
				currentState++
				continue

			case NumLine:
				nums := strToIntSlice(line)
				dest, src, length := nums[0], nums[1], nums[2]

				updateMapForCurrState(dest, src, length, currentState, maps)
			}
		}

		// prettyPrintMaps(maps)

		for seed := range seedToLocation {
			key := seed

			for _, currMap := range maps {
				if newKey, ok := (*currMap)[key]; ok {
					key = newKey
				}
			}

			seedToLocation[seed] = key
		}

		min := math.MaxInt32
		for _, v := range seedToLocation {
			if v < min {
				min = v
			}
		}

		fmt.Println("SOLUTION:", min)
	}
}
