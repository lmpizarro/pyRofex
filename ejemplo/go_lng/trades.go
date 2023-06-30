package main

import (
	"fmt"
	"sort"
	"time"

	"gonum.org/v1/gonum/stat"
)

type Trade struct {
	Symbol     string  `json:"symbol"`
	Servertime int64   `json:"servertime"`
	Size       float64 `json:"size"`
	Price      float64 `json:"price"`
	Datetime   string  `json:"datetime"`
}

type TradesList struct {
	Status string  `json:"status"`
	Symbol string  `json:"symbol"`
	Market string  `json:"market"`
	Trades []Trade `json:"trades"`
}

type Describe struct {
	len    int
	mean   float64
	stdev  float64
	median float64
	varz   float64
	mode   float64
	high   float64
	low    float64
	first  float64
	last   float64
}

// returns := Diff(xs)
func Diff(xs []float64) []float64 {
	xy := xs[:len(xs)-1]
	var diff []float64
	for i, x := range xy {
		diff = append(diff, xs[i+1]-x)
	}

	return diff
}

func findMinAndMax(xs []float64) (min float64, max float64) {

	min = xs[0]
	max = xs[0]
	for _, value := range xs {
		if value < min {
			min = value
		}
		if value > max {
			max = value
		}
	}
	return min, max
}

func describe(xs []float64) Describe {
	var descrXs Describe
	descrXs.len = len(xs)
	descrXs.mean = stat.Mean(xs, nil)
	descrXs.stdev = stat.StdDev(xs, nil)
	sort.Float64s(xs)
	descrXs.median = stat.Quantile(0.5, stat.Empirical, xs, nil)
	descrXs.varz = stat.Variance(xs, nil)
	descrXs.mode, _ = stat.Mode(xs, nil)
	min, max := findMinAndMax(xs)
	descrXs.high = max
	descrXs.low = min
	descrXs.first = xs[0]
	descrXs.last = xs[len(xs)-1]
	return descrXs
}

func ReduceTrades(trades []Trade) (descrPrices Describe, descrSizes Describe, sizePrice float64) {

	var prixes []float64
	var sixes []float64
	var accum_sizes float64 = 0
	var accum_prods float64 = 0
	for _, trade := range trades {
		prixes = append(prixes, trade.Price)
		sixes = append(sixes, trade.Size)
		accum_sizes += trade.Size
		accum_prods += trade.Price * trade.Size
	}

	descrPrices = describe(prixes)

	descrSizes = describe(sixes)

	return descrPrices, descrSizes, accum_prods / accum_sizes
}

func DailyOhlcTrades(trades []Trade) map[string][]Trade {
	m := make(map[string][]Trade)
	for _, trade := range trades {

		t := time.Unix(trade.Servertime/1000, 0)
		year, month, day := t.Date()

		p := fmt.Sprintf("%d-%s-%d", year, month, day)

		m[p] = append(m[p], trade)

	}

	return m
}

func (describe *Describe) DescribeRepr() string {
	return fmt.Sprintf("mean %.2f len %d stdev %.2f median %.2f var %.2f mode %.2f",
		describe.mean,
		describe.len,
		describe.stdev,
		describe.median,
		describe.varz,
		describe.mode)
}
