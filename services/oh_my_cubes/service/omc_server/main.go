package main

import (
	"fmt"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"math/rand"
	"net"
	"os"
	"summer-2022/auth"
	"summer-2022/lib"
	"summer-2022/proto"
	"time"
)

func main() {
	logger, _ := zap.NewDevelopment()
	defer logger.Sync()

	rand.Seed(time.Now().UnixNano())

	etcdHost := os.Getenv("ETCD")

	etcdStorage := lib.NewEtcdStorage(etcdHost, logger)

	credsStorage := auth.NewEtcdCredentialsStorage(etcdStorage, logger)
	tokenManagerImpl := auth.NewTokenManagerImpl(logger)

	//omc
	authMiddleware := auth.NewGRPCMiddlewareImpl(tokenManagerImpl, credsStorage, logger)

	opts := []grpc.ServerOption{
		grpc.UnaryInterceptor(authMiddleware.Intercept),
	}
	omcServer := grpc.NewServer(opts...)

	blockStorage := NewEtcdOMCStorage(etcdStorage, logger)
	omcApi := NewGameService(blockStorage, tokenManagerImpl, logger)

	//auth
	authServer := grpc.NewServer()
	authService := auth.NewAuthService(credsStorage, tokenManagerImpl, logger)

	host := ""

	go func() {
		logger.Info("Starting auth server")
		proto.RegisterAuthServer(authServer, authService)
		startServer(host, 8090, logger, authServer)
	}()

	proto.RegisterOMCServer(omcServer, omcApi)
	logger.Info("Starting omc server")
	startServer(host, 9090, logger, omcServer)
}

func startServer(host string, port int, logger *zap.Logger, server *grpc.Server) {
	omcListener, err := net.Listen("tcp", fmt.Sprintf("%s:%d", host, port))
	if err != nil {
		logger.Fatal("failed to listen: %v", zap.Error(err))
	}

	err = server.Serve(omcListener)

	if err != nil {
		logger.Fatal("grpc server failed", zap.Error(err))
	}
}
