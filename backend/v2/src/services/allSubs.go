package services

import (
	"github.com/gin-gonic/gin"
)

// Grabs all the subs currently available from the database
// And packages it into a json file
func allsubs(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "pong",
	})
}
