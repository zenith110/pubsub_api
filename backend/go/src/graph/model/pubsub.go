package model

type Pubsub struct {
	Name     string `json:"name"`
	Image    string `json:"image"`
	OnSale   bool   `json:"onSale"`
	SaleDate string `json:"saleDate"`
}