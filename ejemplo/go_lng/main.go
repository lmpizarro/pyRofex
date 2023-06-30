package main

import (
	"fmt"
	"time"
)

func main() {
	dlrs := [6]string{"DLR/AGO23", "DLR/SEP23", "DLR/OCT23", "DLR/NOV23", "DLR/DIC23", "DLR/ENE24"}
	token := Login()

	for _, ticker := range dlrs {
		market_data, _ := GetMarketData(ticker, token)
		last := market_data.Last()
		ask := market_data.Ask()
		bid := market_data.Bid()

		fmt.Println(ticker)
		fmt.Println(ask)
		fmt.Println(bid)
		t_last := time.Unix(last.Date/1000, 0)
		fmt.Println(t_last, last.Price, last.Size)

		period := Seven_days_from_now()
		trades := GetHistoricData(ticker, token, period)
		descPrices, descSizes := ReduceTrades(trades)
		fmt.Println("Prices ", descPrices.DescribeRepr())
		fmt.Println("Sizes ", descSizes.DescribeRepr())

	}
}

