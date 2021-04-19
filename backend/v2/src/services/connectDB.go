package services

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/go-pg/pg/v10"
)

type DB struct {
	Login Login `json:"Login"`
}

type Login struct {
	Username string `json:"Username"`
	Password string `json:"Password"`
	Database string `json:"Database"`
	Host     string `json:"Host"`
	Table    string `json:"Table"`
	Port     string `json:"Port"`
}

func ParseJson() DB {
	info, err := os.Open("settings/dblogin.json")
	if err != nil {
		fmt.Println(err)
	}
	byteValue, _ := ioutil.ReadAll(info)
	var loginJson DB

	jsonErr := json.Unmarshal(byteValue, &loginJson)
	if jsonErr != err {
		fmt.Println(jsonErr)
	}
	return loginJson
}

func GetTable() string {
	json := ParseJson()
	fmt.Println(json.Login.Table)
	return json.Login.Table
}
func CloseDB() {
	db := ConnectToDB()
	defer db.Close()
}

func ConnectToDB() *pg.DB {
	json := ParseJson()
	db := pg.Connect(&pg.Options{
		User:     json.Login.Username,
		Password: json.Login.Password,
		Database: json.Login.Database,
		Addr:     json.Login.Port,
	})
	fmt.Println(db)
	ctx := context.Background()
	if err := db.Ping(ctx); err != nil {
		fmt.Println("Could not connect!")
	}

	return db
}
