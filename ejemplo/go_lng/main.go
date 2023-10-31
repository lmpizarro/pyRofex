package main

import (
	"fmt"
)



func main() {
	dlrs := [6]Ticker{{"DLR/FEB24"}, {"DLR/MAR24"}, {"DLR/ABR24"},
					    {"DLR/NOV23"}, {"DLR/DIC23"}, {"DLR/ENE24"}}
	token := Login()

 	for _, ticker := range dlrs {

		mapTickerOrderBook := orderBook(ticker.Name, token)

		for ticker, v := range mapTickerOrderBook {
			fmt.Println("ticker ", ticker)
			fmt.Println(v.OrderBookRepr())
		}

	}

	period := Seven_days_from_now()
	for _, ticker := range dlrs {

		trades := GetHistoricData(ticker.Name, token, period)

		fmt.Println("ticker ", ticker.Name, "real period FROM ", period.From, "TO ", period.To)
		histStat := HistoricStat(trades, period)

		fmt.Println("Period ", histStat.Period.From, "Mean ", histStat.StatPrices.Mean)
		for _, e := range histStat.StatDailies {
			fmt.Println(e.Period.From, e.StatPrices.Mean)
		}
	}
}
