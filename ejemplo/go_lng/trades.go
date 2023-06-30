package main

import "fmt"


type Trade struct {
	Symbol     string  `json:"symbol"`
	Servertime int64   `json:"servertime"`
	Size       float64 `json:"size"`
	Price      float64 `json:"price"`
	Datetime   string  `json:"datetime"`
}

type TradesList struct {
	Status string `json:"status"`
	Symbol string `json:"symbol"`
	Market string `json:"market"`
	Trades [] Trade `json:"trades"`
}

type Describe struct {
	len int
	mean float64
}

func ReduceTrades(trades []Trade) Describe{
	var describe Describe
	describe.len = len(trades)

	accum_prices := 0.0
	for _, trade := range trades{
		accum_prices += trade.Price
	}

	describe.mean = accum_prices / float64(describe.len)

	return describe
}

func (describe *Describe) DescribeRepr () string{
	return fmt.Sprintf("mean %.2f len %d", describe.mean, describe.len)
}