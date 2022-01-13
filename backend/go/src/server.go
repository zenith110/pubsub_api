package main

import (
	"log"
	"net/http"
	"os"
	"pubsub-api/graph"
	"pubsub-api/graph/generated"
	"pubsub-api/graph/metrics"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/playground"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

const defaultPort = "8443"
// Initalizes the prometheus data points
func init(){
	var systemMemoryTotal = metrics.SystemMemoryMetric("totalSystemMemory", "How much memory the system has", "Total")
	var usedSystemMemory = metrics.SystemMemoryMetric("usedSystemMemory", "How much memory the system has used", "Used")
	var cachedSystemMemory = metrics.SystemMemoryMetric("cachedSystemMemory", "How much memory is cached", "Cached")
	var freeSystemMemory = metrics.SystemMemoryMetric("freeSystemMemory", "How much memory is free on the system", "Free")
	var systemIdle = metrics.SystemCPUMetrics("systemIdle", "Idle readings from CPU", "Idle")
	var networkCounter = metrics.SystemCPUMetrics("networkCounter", "Network counter in kB/s", "System")
	var hardDriveCounter = metrics.SystemCPUMetrics("hardDriveCounter", "System readings from CPU in regards to disk IOPS", "User")
	prometheus.Register(systemMemoryTotal)
	prometheus.Register(usedSystemMemory)
	prometheus.Register(cachedSystemMemory)
	prometheus.Register(freeSystemMemory)
	prometheus.Register(systemIdle)
	prometheus.Register(networkCounter)
	prometheus.Register(hardDriveCounter)
}
func main() {
	port := os.Getenv("GRAPHQLPORT")
	if port == "" {
		port = defaultPort
	}

	srv := handler.NewDefaultServer(generated.NewExecutableSchema(generated.Config{Resolvers: &graph.Resolver{}}))

	http.Handle("/", playground.Handler("GraphQL playground", "/query"))
	http.Handle("/query", srv)
	http.Handle("/metrics", promhttp.Handler())
	log.Printf("connect to http://localhost:%s/ for GraphQL playground", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
