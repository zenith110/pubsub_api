package queries

import (
	"context"
	"fmt"
	"github.com/jackc/pgx/v4"
	"os"
	"pubsub-api/graph/model"
	"strings"
)

func FetchSub(tableName string, pubsubName string, databaseURL string) (*model.Pubsub, error) {
	pubsubName = strings.ToLower(pubsubName)
	pubsubName = strings.Replace(pubsubName, " ", "-", -1)
	conn, err := pgx.Connect(context.Background(), databaseURL)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close(context.Background())
	var pubsub model.Pubsub
	query := fmt.Sprintf("SELECT pubsub_name, dates, on_sale, price, image FROM %s WHERE pubsub_name = '%s' ORDER BY dates DESC LIMIT 1", tableName, pubsubName)
	err = conn.QueryRow(context.Background(), query).Scan(&pubsub.Name, &pubsub.Saledates, &pubsub.Onsale, &pubsub.Price, &pubsub.Image)
	if err != nil {
		fmt.Fprintf(os.Stderr, "QueryRow failed: %v\n", err)
		os.Exit(1)
	}

	return &pubsub, err
}
