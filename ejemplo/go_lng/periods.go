package main

import (
	"fmt"
	"time"
)

type Period struct {
	from string
	to   string
}

func Seven_days_from_now() Period {
	var period Period
	time_to := time.Now()
	time_from := time_to.Add(time.Duration(-7*24) * time.Hour)
	d_to := fmt.Sprintf("%d-%d-%d", time_to.Year(), time_to.Month(), time_to.Day())
	d_from := fmt.Sprintf("%d-%d-%d", time_from.Year(), time_from.Month(), time_from.Day())
	period.from = d_from
	period.to = d_to
	return period
}
