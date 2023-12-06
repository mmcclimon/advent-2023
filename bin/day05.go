package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"sync"
)

func main() {
	hunks := readHunks()
	seeds := makeSeedsP1(hunks[0][0])

	transformer := makeTransformer(hunks[1:])

	l1 := math.MaxInt
	l2 := math.MaxInt

	// Part 1
	for _, seed := range seeds {
		l1 = min(l1, transformer(seed))
	}

	fmt.Println("part 1:", l1)

	// Part 2
	var wg sync.WaitGroup
	var mu sync.Mutex

	for i := 0; i < len(seeds); i += 2 {
		n, span := seeds[i], seeds[i+1]

		wg.Add(1)
		go func() {
			defer wg.Done()
			best := doSpan(n, span, transformer)

			mu.Lock()
			defer mu.Unlock()

			l2 = min(l2, best)
		}()
	}

	wg.Wait()

	fmt.Println("part 2:", l2)
}

func ordie(err error) {
	if err == nil {
		return
	}

	fmt.Println(err)
	os.Exit(1)
}

func readHunks() [][]string {
	scanner := bufio.NewScanner(os.Stdin)
	hunks := make([][]string, 0)
	buf := make([]string, 0)

	for scanner.Scan() {
		line := scanner.Text()

		if line == "" {
			hunks = append(hunks, buf)
			buf = make([]string, 0)
			continue
		}

		buf = append(buf, line)
	}

	if len(buf) > 0 {
		hunks = append(hunks, buf)
	}

	ordie(scanner.Err())
	return hunks
}

func makeSeedsP1(line string) []int {
	ret := make([]int, 0)

	for _, s := range strings.Fields(strings.TrimPrefix(line, "seeds: ")) {
		n, err := strconv.Atoi(s)
		ordie(err)
		ret = append(ret, n)
	}

	return ret
}

type almanac struct{ dst, src, span int }

func makeTransformer(hunks [][]string) func(int) int {
	lookups := make([]map[int]almanac, 0)

	for _, hunk := range hunks {
		lookup := make(map[int]almanac)

		for _, line := range hunk[1:] {
			nums := make([]int, 3)
			for i, s := range strings.Fields(line) {
				n, err := strconv.Atoi(s)
				ordie(err)
				nums[i] = n
			}

			a := almanac{nums[0], nums[1], nums[2]}
			lookup[a.src] = a
		}

		lookups = append(lookups, lookup)
	}

	return func(item int) int {
		for _, lookup := range lookups {
			for k, val := range lookup {
				if k <= item && item < k+val.span {
					item = val.dst + (item - val.src)
					break
				}
			}
		}

		return item
	}
}

func doSpan(start, span int, transformer func(int) int) int {
	least := math.MaxInt

	fmt.Printf("starting span %d\n", start)
	for seed := start; seed < start+span; seed++ {
		least = min(least, transformer(seed))
	}

	fmt.Printf("finished span %d\n", start)
	return least
}
