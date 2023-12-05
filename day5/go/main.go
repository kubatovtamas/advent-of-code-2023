package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"

	// "runtime"
	// "runtime/pprof"
	"sort"
	"strconv"
	"strings"
	"sync"
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

type SeedInterval struct {
	begin  int
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

func getLineType(line string) (lineType LineType) {
	if line[:5] == "seeds" {
		return SeedsLine
	}
	if line[len(line)-1] == ':' {
		return MapLine
	}

	return NumLine
}

func stringToIntSlice(str string) []int {
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

func parseSeedsPart1(line string) []int {
	numsPart := line[7:]
	return stringToIntSlice(numsPart)
}

func parseSeedsPart2(line string) []SeedInterval {
	numsPart := line[7:]
	intSlice := stringToIntSlice(numsPart)

	seedIntervals := make([]SeedInterval, 0)
	for i := 0; i < len(intSlice)-1; i += 2 {
		seedIntervals = append(seedIntervals, SeedInterval{begin: intSlice[i], length: intSlice[i+1]})
	}

	return seedIntervals
}

func updateMappingsForCurrState(dest, src, length int, state State, mappings *[7][]MappingInterval) {
	nth := int(state) - 1 // will never receive ListSeeds map, needed for correct indexing
	mappingForCurrState := &mappings[nth]

	newMapping := MappingInterval{src, dest, length}
	*mappingForCurrState = append(*mappingForCurrState, newMapping)
}

func getNextValueForKey(key int, mappings []MappingInterval) int {
	low, high := 0, len(mappings)-1

	for low <= high {
		mid := low + (high-low)/2
		interval := mappings[mid]

		if interval.src <= key && key < interval.src+interval.length {
			diff := key - interval.src
			return interval.dest + diff
		}

		if key < interval.src {
			high = mid - 1
		} else {
			low = mid + 1
		}
	}

	return key
}

func getMinLocationForSeedsPart1(seeds []int, mappings [7][]MappingInterval) int {
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

func calculateMinForSeedInterval(seedInterval SeedInterval, mappings [7][]MappingInterval) int {
	var wg sync.WaitGroup
	minCh := make(chan int)

	// Number of sub-intervals
	const numSubIntervals = 4
	subIntervalLength := seedInterval.length / numSubIntervals

	for i := 0; i < numSubIntervals; i++ {
		begin := seedInterval.begin + i*subIntervalLength
		end := begin + subIntervalLength
		if i == numSubIntervals-1 {
			end = seedInterval.begin + seedInterval.length // Ensure the last interval goes up to the end
		}

		wg.Add(1)
		go func(begin, end int) {
			defer wg.Done()

			subMin := math.MaxInt32
			for i := begin; i < end; i++ {
				key := i

				for _, currMappings := range mappings {
					key = getNextValueForKey(key, currMappings)
				}

				if key < subMin {
					subMin = key
				}
			}

			minCh <- subMin
		}(begin, end)
	}

	go func() {
		wg.Wait()
		close(minCh)
	}()

	overallMin := math.MaxInt32
	for minVal := range minCh {
		if minVal < overallMin {
			overallMin = minVal
		}
	}

	return overallMin
}

func getMinLocationForSeedsPart2(seeds []SeedInterval, mappings [7][]MappingInterval) int {
	var wg sync.WaitGroup
	minCh := make(chan int)

	for _, seedInterval := range seeds {
		wg.Add(1)

		go func(seedInterval SeedInterval) {
			defer wg.Done()

			localMin := calculateMinForSeedInterval(seedInterval, mappings)
			minCh <- localMin
		}(seedInterval)
	}

	go func() {
		wg.Wait()
		close(minCh)
	}()

	min := math.MaxInt32
	for minVal := range minCh {
		if minVal < min {
			min = minVal
		}
	}

	return min
}

func main() {
	// cpuFile, err := os.Create("cpu.prof")
	// if err != nil {
	// 	log.Fatal("could not create CPU profile: ", err)
	// }
	// defer cpuFile.Close()
	// if err := pprof.StartCPUProfile(cpuFile); err != nil {
	// 	log.Fatal("could not start CPU profile: ", err)
	// }
	// defer pprof.StopCPUProfile()

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
				seeds = parseSeedsPart1(line)

			case MapLine:
				currentState++
				continue

			case NumLine:
				nums := stringToIntSlice(line)
				dest, src, length := nums[0], nums[1], nums[2]

				updateMappingsForCurrState(dest, src, length, currentState, &mappings)
			}
		}

		minLocation := getMinLocationForSeedsPart1(seeds, mappings)

		fmt.Println("SOLUTION:", minLocation)
	}

	if part == 2 {
		var seeds []SeedInterval
		mappingsArr := [7][]MappingInterval{}

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
				seeds = parseSeedsPart2(line)

			case MapLine:
				currentState++
				continue

			case NumLine:
				nums := stringToIntSlice(line)
				dest, src, length := nums[0], nums[1], nums[2]

				updateMappingsForCurrState(dest, src, length, currentState, &mappingsArr)
			}
		}

		for _, mappings := range mappingsArr {
			sort.Slice(mappings, func(i, j int) bool {
				return mappings[i].src < mappings[j].src
			})
		}

		minLocation := getMinLocationForSeedsPart2(seeds, mappingsArr)

		fmt.Println("SOLUTION:", minLocation) // 27992443
	}

	// memFile, err := os.Create("mem.prof")
	// if err != nil {
	// 	log.Fatal("could not create memory profile: ", err)
	// }
	// defer memFile.Close()
	// runtime.GC() // run garbage collection to get up-to-date statistics
	// if err := pprof.WriteHeapProfile(memFile); err != nil {
	// 	log.Fatal("could not write memory profile: ", err)
	// }
}
