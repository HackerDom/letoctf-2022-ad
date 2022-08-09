package auth

import (
	"context"
	"errors"
	"go.uber.org/zap"
	"google.golang.org/grpc"
)

const JWT_METADATA = "jwt"

type GRPCMiddleware interface {
	Intercept(ctx context.Context,
		req interface{},
		info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler,
	) (interface{}, error)
}

type GRPCMiddlewareImpl struct {
	jwtManager         JWTManager
	credentialsStorage CredentialsStorage
	lg                 *zap.Logger
}

func NewGRPCMiddlewareImpl(jwtManager JWTManager, credentialsStore CredentialsStorage, lg *zap.Logger) *GRPCMiddlewareImpl {
	return &GRPCMiddlewareImpl{
		jwtManager:         jwtManager,
		credentialsStorage: credentialsStore,
		lg:                 lg,
	}
}

func (mid *GRPCMiddlewareImpl) Intercept(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	clientCreds, err := mid.jwtManager.ParseCredentials(ctx)
	if err != nil {
		return req, err
	}

	credsFound, err := mid.credentialsStorage.Get(clientCreds.Login)

	mid.lg.Info("user creds", zap.Reflect("creds", credsFound))
	mid.lg.Info("client crieds", zap.Reflect("creds", credsFound))

	if credsFound.Password != clientCreds.Password {
		return nil, errors.New("password mismatch")
	}

	return handler(ctx, req)
}
