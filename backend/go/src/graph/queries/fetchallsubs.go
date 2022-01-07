package queries

import (
	"context"
	"fmt"
	"github.com/jackc/pgx/v4/pgxpool"
	"os"
	"pubsub-api/graph/model"
	"strconv"
)

// Given a table name and database url, fetch all the pubsubs from the database
func FetchAllSubs(tableName string, databaseURL string) (*model.Pubsubs, error) {
	// Creates a temporary array of pointers of model.Pubsub due to weird effects when appending *model.Pubsubs.Sub
	var subs []*model.Pubsub
	// Creates the background context
	ctx := context.Background()
	// Connect to the database
	conn, err := pgxpool.Connect(ctx, databaseURL)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	// Wait to close for later
	defer conn.Close()
	// Query for all the subs
	query := fmt.Sprintf("SELECT pubsub_name, dates, on_sale, price, image FROM %s WHERE pubsub_name is not NULL ORDER BY on_sale", tableName)
	var totalSubs int = 0
	rows, connErr := conn.Query(ctx, query)
	if connErr != nil {
		fmt.Fprintf(os.Stderr, "Query failed: %v\n", err)
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
