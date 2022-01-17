package queries

import (
	"context"
	"fmt"
	"io"
	"os"
	"pubsub-api/graph/model"
	"strconv"
	"strings"
	"time"

	"github.com/jackc/pgx/v4"
	"github.com/sirupsen/logrus"
)

func FetchSub(tableName string, pubsubName string, databaseURL string) (*model.Pubsub, error) {
	var logger = logrus.New()
	now := time.Now()
	logger.SetFormatter(&logrus.JSONFormatter{})
	format := fmt.Sprint(int(now.Month())) + strconv.Itoa(now.Day()) + strconv.Itoa(now.Year()) + strconv.Itoa(now.Hour())
	file, err := os.OpenFile("logs/pubsub/fetchsub/log_" + format + ".json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		logger.Error("Could not locate the file: %v\n", err.Error())
	}
	logger.SetOutput(io.MultiWriter(file, os.Stdout))
	pubsubName = strings.ToLower(pubsubName)
	pubsubName = strings.Replace(pubsubName, " ", "-", -1)
	conn, err := pgx.Connect(context.Background(), databaseURL)
	if err != nil {
		logger.Errorf("Unable to connect to database: %v\n", err.Error(), os.Stderr)
	}
	defer conn.Close(context.Background())
	var pubsub model.Pubsub
	query := fmt.Sprintf("SELECT pubsub_name, dates, on_sale, price, image FROM %s WHERE pubsub_name = '%s' ORDER BY dates DESC LIMIT 1", tableName, pubsubName)
	err = conn.QueryRow(context.Background(), query).Scan(&pubsub.Name, &pubsub.Saledates, &pubsub.Onsale, &pubsub.Price, &pubsub.Image)
	if err != nil {
		logger.Error(os.Stderr, "QueryRow failed: %s\n", err.Error())
		os.Exit(1)
	}
	logger.Infof("Successfully got %s", pubsubName)
	return &pubsub, err
}
