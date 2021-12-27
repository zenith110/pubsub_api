FROM golang:1.17.5-alpine3.14


WORKDIR /home/backend/v2
COPY . /home/backend/v2
## Add this go mod download command to pull in any dependencies
RUN go mod download
CMD  ["go", "run", "server.go"]