package main

import (
	"fmt"
	"time"
)

func historicStat(trades []Trade, period Period) HistStatAttr {
	var histStat HistStatAttr
		descPrices, descSizes, vprices := ReduceTrades(trades)

		histStat.StatPrices = descPrices
		histStat.StatSizes = descSizes
		histStat.Vwap = vprices
		histStat.Period = period

		m := DailyOhlcTrades(trades)
		for key, dailyTrades := range m {
			descPrices, descSizes, vprices = ReduceTrades(dailyTrades)
			histStat.StatDailies = append(histStat.StatDailies,
				HistStatAttr{StatPrices: descPrices,
					StatSizes: descSizes, Vwap: vprices, Period: Period{From: key, To: key}})
		}


	return histStat
}

type OrderBookData struct{
	Ticker string
	Ask BIOF
	Bid BIOF
	Last PriceSizeDate
	Spread float64
	MidSpread float64
	DiffLastMidSpread float64
}

func main() {
	dlrs := [6]string{"DLR/AGO23", "DLR/SEP23", "DLR/OCT23", "DLR/NOV23", "DLR/DIC23", "DLR/ENE24"}
	token := Login()
	mapTickerMarketData := make(map[string]OrderBookData)

	for _, ticker := range dlrs {
		market_data, _ := GetMarketData(ticker, token)
		last := market_data.Last()
		ask := market_data.Ask()
		bid := market_data.Bid()

		if len(ask) > 0 && len(bid) > 0 {
			var spread OrderBookData

			spread.Ticker = ticker
			spread.Ask = ask[0]
			spread.Bid = bid[0]
			spread.Last = last
			spread.Spread = spread.Ask.Price - spread.Bid.Price
			spread.MidSpread = .5 * (spread.Ask.Price + spread.Bid.Price)
			spread.DiffLastMidSpread = spread.Last.Price - spread.MidSpread
			fmt.Printf("%+v\n", spread)
			mapTickerMarketData[ticker] = spread
		}
		t_last := time.Unix(last.Date/1000, 0)
		fmt.Println(t_last.String(), last.Price, last.Size)
	}

/* 	for _, ticker := range dlrs {

		period := Seven_days_from_now()
		trades := GetHistoricData(ticker, token, period)


		histStat := historicStat(trades, period)

		fmt.Println(histStat.Period, histStat.StatPrices.Mean)
		for _, e := range histStat.StatDailies {
			fmt.Println(e.Period, e.StatPrices.Mean)
		}
	} */
}
