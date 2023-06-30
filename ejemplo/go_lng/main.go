package main

import (
	"encoding/json"
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

		url := HistoricData(ticker, period.from, period.to)
		json_data, _ := rfx_get_req(url, token)
		var unmarshaled_data TradesList

		json.Unmarshal(json_data, &unmarshaled_data)
		if unmarshaled_data.Status == "OK" {
			trades := unmarshaled_data.Trades

			descPrices, descSizes := ReduceTrades(trades)
			fmt.Println("Prices ", descPrices.DescribeRepr())
			fmt.Println("Sizes ", descSizes.DescribeRepr())
		}

	}
}

func main__() {
	var xs = []float64{1, 2, 3, 4, 5}
	xy := xs[:len(xs)-1]
	fmt.Println(xs[1:], xy)

	var diff []float64
	for i, x := range xy {
		diff = append(diff, xs[i+1]-x)
	}
	fmt.Println(diff)
	fmt.Println(Diff(xs))
}
