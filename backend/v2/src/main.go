package main

import (
	"github.com/gin-gonic/gin"
	"pubsub-api/services"
)

func main() {
	r := gin.Default()
	r.GET("/allsubs/", func(c *gin.Context) {
		allsubs(c)
	})
	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
