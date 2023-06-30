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

type StatAttr struct {
	Len    int     `json:"len"`
	Mean   float64 `json:"mean"`
	Stdev  float64 `json:"stdev"`
	Median float64 `json:"median"`
	Varz   float64 `json:"var"`
	Mode   float64 `json:"mode"`
	High   float64 `json:"high"`
	Low    float64 `json:"low"`
	First  float64 `json:"first"`
	Last   float64 `json:"last"`
}

type HistStatAttr struct {
	Period      Period `json:"period"`
	StatPrices  StatAttr `json:"statPrices"`
	StatSizes   StatAttr `json:"statSizes"`
	Vwap        float64 `json:"vwap"`
	StatDailies []HistStatAttr `json:"statDailies"`
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

func describe(xs []float64) StatAttr {
	var descrXs StatAttr
	descrXs.Len = len(xs)
	descrXs.Mean = stat.Mean(xs, nil)
	descrXs.Stdev = stat.StdDev(xs, nil)
	sort.Float64s(xs)
	descrXs.Median = stat.Quantile(0.5, stat.Empirical, xs, nil)
	descrXs.Varz = stat.Variance(xs, nil)
	descrXs.Mode, _ = stat.Mode(xs, nil)
	min, max := findMinAndMax(xs)
	descrXs.High = max
	descrXs.Low = min
	descrXs.First = xs[0]
	descrXs.Last = xs[len(xs)-1]
	return descrXs
}

func ReduceTrades(trades []Trade) (descrPrices StatAttr, descrSizes StatAttr, sizePrice float64) {

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

func (describe *StatAttr) DescribeRepr() string {
	return fmt.Sprintf("mean %.2f len %d stdev %.2f median %.2f var %.2f mode %.2f",
		describe.Mean,
		describe.Len,
		describe.Stdev,
		describe.Median,
		describe.Varz,
		describe.Mode)
}
