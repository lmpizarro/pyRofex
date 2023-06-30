package main



type BIOF struct {
	Price float64 `json:"price"`
	Size  int     `json:"size"`
}
type PriceSizeDate struct {
	Price float64 `json:"price"`
	Size  int64   `json:"size"`
	Date  int64   `json:"date"`
}

type marketData struct {
	Status     string `json:"status"`
	MarketData struct {
		Oi PriceSizeDate `json:"OI"`
		Cl PriceSizeDate `json:"CL"`
		Hi float64       `json:"Hi"`
		Lo float64       `json:"LO"`
		Of []BIOF         `json:"OF"`
		Se PriceSizeDate `json:"SE"`
		La PriceSizeDate `json:"LA"`
		Bi []BIOF          `json:"BI"`
		Op float64       `json:"OP"`
	} `json:"marketData"`
	Depth      int  `json:"depth"`
	Aggregated bool `json:"aggregated"`
}

type Ticker struct {
	Name string
}