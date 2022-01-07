#-----------------------#
# Go make utils #
generate-schema:
	@echo "Now generating schemas for new graphql model"
	go get github.com/99designs/gqlgen/cmd@v0.14.0
	go run github.com/99designs/gqlgen backend/go/srcx generate --verbose

go-format: # Formats the entire directory
	@echo "Now formatting v2 directory"
	go fmt .
