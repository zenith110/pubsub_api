package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"fmt"
	"io"
	"os"
	"pubsub-api/graph/generated"
	"pubsub-api/graph/model"
	"pubsub-api/graph/queries"
	"strconv"
	"time"

	"github.com/prometheus/common/log"
	"github.com/sirupsen/logrus"
)
var now = time.Now()
const name = "graph"
func (r *queryResolver) Pubsub(ctx context.Context, name string) (*model.Pubsub, error) {
	var logger = logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{})
	format := fmt.Sprint(int(now.Month())) + strconv.Itoa(now.Day()) + strconv.Itoa(now.Year())
	file, err := os.OpenFile("logs/pubsub/db_" + format + ".json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
        log.Errorf(err.Error(), os.Stdout)
    }

    logger.SetOutput(io.MultiWriter(file, os.Stdout))
	sub, err := queries.FetchSub(tableName, name, databaseURL, enviroment)
	if err != nil {
		log.Errorf("Pubsub was not found: %v\n", err, os.Stdout)
	}
	return sub, err
}

func (r *queryResolver) Pubsubs(ctx context.Context) (*model.Pubsubs, error) {
	var logger = logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{})
	format := fmt.Sprint(int(now.Month())) + strconv.Itoa(now.Day()) + strconv.Itoa(now.Year())
	file, err := os.OpenFile("logs/pubsubs/db_" + format + ".json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
        log.Error(err)
    }

    logger.SetOutput(file)
	subs, err := queries.FetchAllSubs(tableName, databaseURL, enviroment)
	if err != nil {
		log.Error("Pubsubs was not found: %v\n", err)
	}
	return subs, err
}

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type queryResolver struct{ *Resolver }

var tableName = os.Getenv("TABLE")
var databaseURL = os.Getenv("DATABASE_URL")
var enviroment = os.Getenv("ENVIROMENT")
