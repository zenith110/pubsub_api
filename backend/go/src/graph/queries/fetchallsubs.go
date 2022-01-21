package queries

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"
	"pubsub-api/graph/model"
	"strconv"
	"time"

	"github.com/jackc/pgx/v4/pgxpool"
	"github.com/sirupsen/logrus"
)
var now = time.Now()
// Given a table name and database url, fetch all the pubsubs from the database
func FetchAllSubs(tableName string, databaseURL string, enviroment string) (*model.Pubsubs, error) {
	var logger = logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{})
	format := fmt.Sprint(int(now.Month())) + strconv.Itoa(now.Day()) + strconv.Itoa(now.Year())
	if enviroment == "dev"{
	file, err := os.OpenFile("logs/pubsubs/fetchall/log_" + format + ".json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
        log.Fatal(err)
    }

    logger.SetOutput(io.MultiWriter(file, os.Stdout))
}else if enviroment == "prod"{
	fmt.Printf("Use s3")
}
	// Creates a temporary array of pointers of model.Pubsub due to weird effects when appending *model.Pubsubs.Sub
	var subs []*model.Pubsub
	// Creates the background context
	ctx := context.Background()
	// Connect to the database
	conn, err := pgxpool.Connect(ctx, databaseURL)
	if err != nil {
		logger.Errorf("Unable to connect to database: %v\n", err)
	}
	// Wait to close for later
	defer conn.Close()
	// Query for all the subs
	query := fmt.Sprintf("SELECT pubsub_name, dates, on_sale, price, image FROM %s WHERE pubsub_name is not NULL ORDER BY on_sale", tableName)
	var totalSubs int = 0
	rows, connErr := conn.Query(ctx, query)
	if connErr != nil {
		logger.Errorf("Query failed: %v\n", err)
		os.Exit(1)
	}
	// Loops through all the subs, create the struct for each and append to our *model.Pubsub struct
	for rows.Next() {
		var pubsub model.Pubsub
		rows.Scan(&pubsub.Name, &pubsub.Saledates, &pubsub.Onsale, &pubsub.Price, &pubsub.Image)
		subs = append(subs, &pubsub)
		totalSubs += 1
	}
	// Creates new *model.Pubsubs struct to return to the user
	var pubsubs = model.Pubsubs{Sub: subs, Total: strconv.Itoa(totalSubs)}
	return &pubsubs, err
}
