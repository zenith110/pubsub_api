package services

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/go-pg/pg/v10"
)

type Login struct {
	Username string `json:"Username"`
	Password string `json:"Password"`
	Database string `json:"Database"`
	Host     string `json:"Host"`
	Table    string `json:"Table"`
	Port     string `json:"Port"`
}

func ParseJson() Login {
	info, err := os.Open("settings/dblogin.json")
	if err != nil {
		fmt.Println(err)
	}
	byteValue, _ := ioutil.ReadAll(info)
	var loginJson Login
	jsonErr := json.Unmarshal(byteValue, &loginJson)
	if jsonErr != err {
		fmt.Println(jsonErr)
	}
	return loginJson
}

func GetTable() string {
	json := ParseJson()
	return json.Table
}
func CloseDB() {
	db := ConnectToDB()
	defer db.Close()
}

func ConnectToDB() {
	json := ParseJson()
	db := pg.Connect(&pg.Options{
		User:     json.Username,
		Password: json.Password,
		Host:     json.Host,
		Port:     json.Port,
		Database: json.Database,
	})
	return db
}
