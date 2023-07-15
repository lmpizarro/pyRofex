package main

import (
	"fmt"
)



func main() {
	dlrs := [6]Ticker{{"DLR/AGO23"}, {"DLR/SEP23"}, {"DLR/OCT23"},
					    {"DLR/NOV23"}, {"DLR/DIC23"}, {"DLR/ENE24"}}
	token := Login()

 	for _, ticker := range dlrs {

		mapTickerOrderBook := orderBook(ticker.Name, token)

		for k, v := range mapTickerOrderBook {
			fmt.Println(k)
			fmt.Println(v.OrderBookRepr())
		}

	}

	period := Seven_days_from_now()
	for _, ticker := range dlrs {

		trades := GetHistoricData(ticker.Name, token, period)


		histStat := HistoricStat(trades, period)

		fmt.Println(histStat.Period, histStat.StatPrices.Mean)
		for _, e := range histStat.StatDailies {
			fmt.Println(e.Period, e.StatPrices.Mean)
		}
	}
}
