package services

type Login struct {
	Username string `json:"Username"`
	Password string `json:"Password"`
	Database string `json:"Database"`
	Host     string `json:"Host"`
	Table    string `json:"Table"`
	Port     string `json:"Port"`
}

func GetTable() {

}
func CloseDB() {

}

func ConnectToDB() {

}
