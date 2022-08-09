package main

import (
	"context"
	"fmt"
	"go.uber.org/zap"
	"summer-2022/proto"
)

func main() {

	//logger := zap.New(zapcore.NewTee())
	logger, _ := zap.NewDevelopment()
	defer logger.Sync()

	client := NewClient("localhost:9090", "localhost:8090", logger)
	err := client.SignIn(context.Background(), "dvl111")
	if err != nil {
		logger.Fatal(err.Error())
	}

	block := &proto.Block{
		Name:        "AwsomeBlock",
		Description: "Test",
	}

	logger.Info("put block")
	err = client.PutBlock(context.Background(), block)
	if err != nil {
		logger.Fatal(err.Error())
	}
	logger.Info("put block")

	blocks, err := client.GetBlocks(context.Background())
	if err != nil {
		logger.Fatal(err.Error())
	}
	fmt.Printf("blocks %+v", blocks)

	sharedBlock := &proto.Block{
		Name:        "SharedBlock",
		Description: "Test",
	}
	shared, err := client.PutShared(context.Background(), sharedBlock)
	if err != nil {
		return
	}
	fmt.Printf("blocks %+v", shared)

	getShared, err := client.GetShared(context.Background(), &proto.GetSharedBlock{
		SharedId: shared.Metadata.SharedId,
		AdminKey: shared.AdminKey,
	})
	if err != nil {
		logger.Fatal(err.Error())
	}

	fmt.Printf("blocks %+v", getShared)

	//render := NewConsoleRender(logger)
	//for {
	//	time.Sleep(time.Millisecond * 100)
	//	state, err := client.GetState(ctx)
	//	if err != nil {
	//		panic(err.Error())
	//		return
	//	}
	//	render.Render(state)
	//	cancel()
	//}
}
