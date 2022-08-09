package main

import (
	"fmt"
	"github.com/gofrs/uuid"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"net"
	"summer-2022/auth"
	"summer-2022/lib"
	"summer-2022/proto"
)

func main() {
	logger, _ := zap.NewDevelopment()
	defer logger.Sync()

	etcdStorage := lib.NewEtcdStorage("localhost:2379", logger)

	credsStorage := auth.NewEtcdCredentialsStorage(etcdStorage, logger)
	jwtManager := auth.NewJWTManagerImpl([]byte("secret"), logger)

	//omc
	authMiddleware := auth.NewGRPCMiddlewareImpl(jwtManager, credsStorage, logger)

	opts := []grpc.ServerOption{
		grpc.UnaryInterceptor(authMiddleware.Intercept),
	}
	omcServer := grpc.NewServer(opts...)
	omcApi := NewGameService(logger)

	//auth
	authServer := grpc.NewServer()
	authService := auth.NewAuthService(credsStorage, jwtManager, logger)

	host := "localhost"

	go func() {
		logger.Info("Starting auth server")
		proto.RegisterAuthServer(authServer, authService)
		startServer(host, 8090, logger, authServer)
	}()

	proto.RegisterOMCServer(omcServer, omcApi)
	startServer(host, 9090, logger, omcServer)
}

func run() {
	uid, _ := uuid.NewV1()
	v1, _ := uuid.TimestampFromV1(uid)
	time, _ := v1.Time()
	ts := time.UnixNano()
	fmt.Println(time.UnixNano(), ts)
}

func startServer(host string, port int, logger *zap.Logger, server *grpc.Server) {
	logger.Info("Starting game server")
	omcListener, err := net.Listen("tcp", fmt.Sprintf("%s:%d", host, port))
	if err != nil {
		logger.Fatal("failed to listen: %v", zap.Error(err))
	}

	err = server.Serve(omcListener)

	if err != nil {
		logger.Fatal("grpc server failed", zap.Error(err))
	}
}
