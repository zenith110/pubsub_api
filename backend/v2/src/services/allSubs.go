package services

import (
	"fmt"

	"github.com/gin-gonic/gin"
)

type Subs struct {
	All_Subs []Sub
}
type Sub struct {
	name string
}

// Grabs all the subs currently available from the database
// And packages it into a json file
func AllSubs(c *gin.Context) {
	connection := ConnectToDB()
	fmt.Println(connection)
	// query := ("SELECT pubsub_name FROM %s" +
	// 	" WHERE pubsub_name is not NULL ORDER BY on_sale")
	// queryFormat := fmt.Sprintf(query, GetTable())
	// cur, _ := connection.pi
	// fmt.Println(cur)
	// c.JSON(200, gin.H{
	// 	"message": "pong",
	// })
}
