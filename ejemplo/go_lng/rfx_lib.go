package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

const Url = "https://api.remarkets.primary.com.ar/"
const auth = "auth/getToken"
const market_data = "rest/marketdata/get?marketId=ROFX&symbol=%v&entries=BI,OF,LA,OP,CL,HI,LO,SE,OI&depth=%v"
const historic_trades = "rest/data/getTrades?marketId=ROFX&symbol=%v&dateFrom=%v&dateTo=%v"

var MesesToString = map[string]string{"ENE": "01", "FEB": "02", "MAR": "03", "ABR": "04", "MAY": "05", "JUN": "06",
	"JUL": "07", "AGO": "08", "SEP": "9", "OCT": "10", "NOV": "11", "DIC": "12"}

var MesesToInt = map[string]int{"ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6,
	"JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 2}

var MesesToMonth = map[string]string{"ENE": "JAN", "FEB": "FEB", "MAR": "MAR", "ABR": "APR", "MAY": "05", "JUN": "06",
	"JUL": "07", "AGO": "AUG", "SEP": "SEP", "OCT": "OCT", "NOV": "NOV", "DIC": "DIC"}

/*
BI: BIDS Mejor oferta de compra en el Book
OF: OFFERS Mejor oferta de venta en el Book
LA: LAST Último precio operado en el mercado
OP: OPENING PRICE Precio de apertura
CL: CLOSING PRICE Precio de cierre
SE: SETTLEMENT PRICE Precio de ajuste (solo para futuros)
HI: TRADING SESSION HIGH PRICE Precio máximo de la rueda
LO: TRADING SESSION LOW PRICE Precio mínimo de la rueda
TV: TRADE VOLUME Volumen operado en contratos/nominales para ese security
OI: OPEN INTEREST Interés abierto (solo para futuros)
IV: INDEX VALUE Valor del índice (solo para índices)
EV: TRADE EFFECTIVE VOLUME Volumen efectivo de negociación para ese security
NV: NOMINAL VOLUME Volumen nominal de negociación para ese security
*/

func MarketDataUrl(symbol string, depth int) string {
	return fmt.Sprintf(Url+market_data, symbol, depth)
}

func HistoricData(symbol, fromDate, toDate string) string {
	// TODO:  YYYY-MM-DD
	return fmt.Sprintf(Url+historic_trades, symbol, fromDate, toDate)
}

// https://mholt.github.io/json-to-go/

const Url_Auth = Url + auth

func rfx_get_req(url, token string) ([]byte, error) {
	r, err := http.NewRequest("GET", url, nil)
	if err != nil {
		panic(err)
	}
	r.Header.Add("X-Auth-Token", token)
	client := &http.Client{}
	res, err := client.Do(r)
	if err != nil {
		panic(err)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("status code %v", res.StatusCode)
	}
	body, err := io.ReadAll(res.Body) // response body is []byte
	if err != nil {
		return nil, fmt.Errorf("byte to string fail")
	}

	return body, nil
}

// https://mholt.github.io/json-to-go/

func GetMarketData(contract, token string) (marketData, error) {

	url := MarketDataUrl(contract, 2)
	res, err := rfx_get_req(url, token)
	var unmarshaled_data marketData
	if err != nil {
		return unmarshaled_data, fmt.Errorf("error %v", err)
	}
	err = json.Unmarshal(res, &unmarshaled_data)
	if unmarshaled_data.Status != "OK" {

		return unmarshaled_data, fmt.Errorf("error unmarshall")

	}
	return unmarshaled_data, err
}

func (md *marketData) Bid() []BIOF {
	return md.MarketData.Bi
}

func (md *marketData) Ask() []BIOF {
	return md.MarketData.Of
}

func (md *marketData) Last() PriceSizeDate {
	return md.MarketData.La
}

func GetHistoricData(ticker, token string, period Period) []Trade {
	url := HistoricData(ticker, period.From, period.To)

	json_data, _ := rfx_get_req(url, token)
	var unmarshaled_data TradesList

	json.Unmarshal(json_data, &unmarshaled_data)

	if unmarshaled_data.Status == "OK" {
		return unmarshaled_data.Trades

	}

	var trades []Trade
	return trades
}
