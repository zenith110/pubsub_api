package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"fmt"
	"pubsub-api/graph/generated"
	"pubsub-api/graph/model"
)

func (r *mutationResolver) FetchAllSubs(ctx context.Context) (*model.Pubsubs, error) {
	panic(fmt.Errorf("not implemented"))
}

func (r *mutationResolver) FetchSub(ctx context.Context, input *model.PubsubQuery) (*model.Pubsub, error) {
	panic(fmt.Errorf("not implemented"))
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

type mutationResolver struct{ *Resolver }
