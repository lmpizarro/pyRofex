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
	len   int
	mean  float64
	stdev float64
	median float64
	varz float64
	mode float64
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

func describe(xs []float64) Describe {
	var descrXs Describe
	descrXs.len = len(xs)
	descrXs.mean = stat.Mean(xs, nil)
	descrXs.stdev = stat.StdDev(xs, nil)
	sort.Float64s(xs)
	descrXs.median =  stat.Quantile(0.5, stat.Empirical, xs, nil)
	descrXs.varz = stat.Variance(xs, nil)
	descrXs.mode, _ = stat.Mode(xs, nil)

	return descrXs
}

func ReduceTrades(trades []Trade) (Describe, Describe) {
	// var m map[string][]Trade
	m := make(map[string][]Trade)

	var prixes []float64
	var sixes []float64
	for _, trade := range trades {
		prixes = append(prixes, trade.Price)
		sixes = append(sixes, trade.Size)

		t := time.Unix(trade.Servertime/1000, 0)
		year, month, day := t.Date()

		p := fmt.Sprintf("%d-%s-%d", year, month, day)

		m[p] = append(m[p], trade)

	}

	descrPrices := describe(prixes)

	descrSizes := describe(sixes)
	for key, value := range m {
    	fmt.Println("Key:", key, "Value:", value)
	}
	return descrPrices, descrSizes
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
