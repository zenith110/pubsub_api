// Code generated by github.com/99designs/gqlgen, DO NOT EDIT.

package model

type Pubsub struct {
	Name      string `json:"name"`
	Image     string `json:"image"`
	Saledates string `json:"saledates"`
	Onsale    string `json:"onsale"`
	Price     string `json:"price"`
}

type Pubsubs struct {
	Sub   []*Pubsub `json:"sub"`
	Total string    `json:"total"`
}
