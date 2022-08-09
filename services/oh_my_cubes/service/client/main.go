package main

import (
	"context"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"time"
)

func main() {

	logger := zap.New(zapcore.NewTee())
	//logger, _ := zap.NewDevelopment()
	defer logger.Sync()

	client := NewClient("localhost:9090", "localhost:8090", logger)
	err := client.SignIn(context.Background(), "dvl", "pwaswrd")
	if err != nil {
		logger.Fatal(err.Error())
	}

	render := NewConsoleRender(logger)
	for {
		time.Sleep(time.Millisecond * 100)
		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
		state, err := client.GetState(ctx)
		if err != nil {
			panic(err.Error())
			return
		}
		render.Render(state)
		cancel()
	}
}
