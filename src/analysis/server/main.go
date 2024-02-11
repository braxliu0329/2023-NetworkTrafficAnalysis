package main

import (
	"fmt"
	"log"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
)

func main() {
	fmt.Println("")
	app := fiber.New()
	app.Use(cors.New(cors.Config{
		AllowOrigins: "http://localhost:3000",
		AllowHeaders: "Origin, Content-Type, Accept",
	}))
	app.Static("/", "../client/dist")
	app.Get("/healthcheck", func(c *fiber.Ctx) error {
		return c.SendString("OK")
	})
	log.Fatal(app.Listen(":4000"))
}
