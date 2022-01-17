package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"io"
	"os"
	"pubsub-api/graph/generated"
	"pubsub-api/graph/model"
	"pubsub-api/graph/queries"
	"time"

	"github.com/prometheus/common/log"
	"github.com/sirupsen/logrus"
)
var now = time.Now()
func (r *queryResolver) Pubsub(ctx context.Context, name string) (*model.Pubsub, error) {
	var logger = logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{})
	file, err := os.OpenFile("logs/pubsub/db_.json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Infof("ayoo")
        log.Errorf(err.Error(), os.Stdout)
    }

    logger.SetOutput(io.MultiWriter(file, os.Stdout))
	sub, err := queries.FetchSub(tableName, name, databaseURL)
	if err != nil {
		log.Errorf("Pubsub was not found: %v\n", err, os.Stdout)
	}
	return sub, err
}

func (r *queryResolver) Pubsubs(ctx context.Context) (*model.Pubsubs, error) {
	var logger = logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{})
	file, err := os.OpenFile("logs/pubsubs/db_" + now.String() + ".json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
        log.Error(err)
    }

    logger.SetOutput(file)
	subs, err := queries.FetchAllSubs(tableName, databaseURL)
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
