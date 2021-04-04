package main

import (
	. "./services"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.GET("/allsubs/", func(c *gin.Context) {
		allsubs(c)
	})
	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
