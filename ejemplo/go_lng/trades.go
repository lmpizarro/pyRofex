package main

import (
	"fmt"
	"gonum.org/v1/gonum/stat"
	"sort"
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
}

func ReduceTrades(trades []Trade) Describe {
	var describe Describe

	var xs []float64
	accum_prices := 0.0
	for _, trade := range trades {
		accum_prices += trade.Price
		xs = append(xs, trade.Price)
	}

	describe.len = len(xs)
	describe.mean = stat.Mean(xs, nil)
	describe.stdev = stat.StdDev(xs, nil)
	sort.Float64s(xs)
	describe.median =  stat.Quantile(0.5, stat.Empirical, xs, nil)
	return describe
}

func (describe *Describe) DescribeRepr() string {
	return fmt.Sprintf("mean %.2f len %d stdev %.2f median %.2f",
		describe.mean,
		describe.len,
		describe.stdev,
		describe.median)
}
