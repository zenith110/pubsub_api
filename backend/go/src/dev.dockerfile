FROM golang:1.17.5-alpine3.14


WORKDIR /home/backend/graphql/
COPY . /home/backend/graphql/
## Add this go mod download command to pull in any dependencies
RUN go mod download
RUN go fmt .
CMD  ["go", "run", "server.go"]