package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"fmt"
	"os"
	"pubsub-api/graph/generated"
	"pubsub-api/graph/model"
	"pubsub-api/graph/queries"
)

func (r *queryResolver) Pubsub(ctx context.Context, name string) (*model.Pubsub, error) {
	sub, err := queries.FetchSub(tableName, name, databaseURL)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Pubsub was not found: %v\n", err)
		os.Exit(1)
	}
	return sub, err
}

func (r *queryResolver) Pubsubs(ctx context.Context) (*model.Pubsubs, error) {
	subs, err := queries.FetchAllSubs(tableName, databaseURL)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Pubsubs was not found: %v\n", err)
		os.Exit(1)
	}
	return subs, err
}

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type queryResolver struct{ *Resolver }

var tableName = os.Getenv("TABLE")
var databaseURL = os.Getenv("DATABASE_URL")
