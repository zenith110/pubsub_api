package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/Pubsub-api/backend/models"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/jackc/pgx/v4/pgxpool"
	"net/http"
	"os"
)

var ConnectionPool* pgxpool.Pool

func main() {
	setupDatabase()

	router := chi.NewRouter()
	router.Use(middleware.Logger)
	setupRoutes(router)

	if err := http.ListenAndServe(":8080", router); err == nil {
		fmt.Println("Process listening on port 8080")
		defer ConnectionPool.Close()
	}
}

func setupDatabase() {
	pool, err := pgxpool.Connect(context.Background(), os.Getenv("DATABASE_URL"))
	if err != nil {
		_, _ = fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	ConnectionPool = pool
}

func setupRoutes(router chi.Router) {
	router.Get("/", func(writer http.ResponseWriter, request *http.Request) {
		_, err := writer.Write([]byte("root called"))
		if err != nil {
			return
		}
	})

	router.Get("/allsubs", func(writer http.ResponseWriter, request *http.Request) {
		rows, err := ConnectionPool.Query(context.Background(), "SELECT name FROM subs")
		if err != nil {
			_ = fmt.Errorf("error: %s", err.Error())
			_, _ = writer.Write([]byte(err.Error()))
			return
		}
		var subs = make([]string, 0)

		for rows.Next() {
			var subName string
			err := rows.Scan(subName)
			if err != nil {
				_ = fmt.Errorf("error: %s", err.Error())
				_, _ = writer.Write([]byte(err.Error()))
				continue
			}
			subs = append(subs, subName)
		}
		marshaledJson, err := json.Marshal(subs)
		if err != nil {
			_ = fmt.Errorf("error: %s", err.Error())
			_, _ = writer.Write([]byte(err.Error()))
			return
		}
		_, err = writer.Write(marshaledJson)
		if err != nil {
			_ = fmt.Errorf("error: %s", err.Error())
			_, _ = writer.Write([]byte(err.Error()))
			return
		}
	})

	router.Get("/onsale", func(writer http.ResponseWriter, request *http.Request) {
		rows, err := ConnectionPool.Query(context.Background(), "SELECT * FROM subs WHERE current_sale IS NOT NULL")
		if err != nil {
			_, _ = writer.Write([]byte(err.Error()))
			return
		}
		var subs = make([]models.Sub, 0)

		for rows.Next() {
			var sub models.Sub
			var subSaleString []byte
			err := rows.Scan(sub.Name, sub.ImageUrl, sub.Id, subSaleString)
			if err != nil {
				_ = fmt.Errorf("error: %s", err.Error())
				_, _ = writer.Write([]byte(err.Error()))
				continue
			}
			err = json.Unmarshal(subSaleString, &sub.CurrentSale)
			if err != nil {
				_ = fmt.Errorf("error: %s", err.Error())
				_, _ = writer.Write([]byte(err.Error()))
				continue
			}
		}
		marshal, err := json.Marshal(subs)
		if err != nil {
			_ = fmt.Errorf("error: %s", err.Error())
			_, _ = writer.Write([]byte(err.Error()))
			return
		}
		_, _ = writer.Write(marshal)


	})

	router.Get("/subs", func(writer http.ResponseWriter, request *http.Request) {
		_, err := writer.Write([]byte("subs called"))
		if err != nil {
			return
		}
	})

	router.Get("/totalcount", func(writer http.ResponseWriter, request *http.Request) {
		var count int
		row := ConnectionPool.QueryRow(context.Background(), "COUNT (*) FROM subs")
		err := row.Scan(&count)
		if err != nil {
			_ = fmt.Errorf("error: %s", err.Error())
			_, _ = writer.Write([]byte(err.Error()))
			return
		}
		_, _ = writer.Write([]byte(string(rune(count))))
	})
}