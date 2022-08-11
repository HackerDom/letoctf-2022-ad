package auth

import (
	"context"
	"errors"
	"go.uber.org/zap"
	"google.golang.org/grpc"
)

const METADATA_KEY = "jwt"

type GRPCMiddleware interface {
	Intercept(ctx context.Context,
		req interface{},
		info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler,
	) (interface{}, error)
}

type GRPCMiddlewareImpl struct {
	tokenManager       TokenManager
	credentialsStorage CredentialsStorage
	lg                 *zap.Logger
}

func NewGRPCMiddlewareImpl(tokenManager TokenManager, credentialsStore CredentialsStorage, lg *zap.Logger) *GRPCMiddlewareImpl {
	return &GRPCMiddlewareImpl{
		tokenManager:       tokenManager,
		credentialsStorage: credentialsStore,
		lg:                 lg,
	}
}

func (mid *GRPCMiddlewareImpl) Intercept(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	clientCreds, err := mid.tokenManager.ParseCredentials(ctx)
	if err != nil {
		mid.lg.Error("auth fauled", zap.Error(err))
		return req, err
	}

	credsFound, err := mid.credentialsStorage.Get(ctx, clientCreds.Token)

	mid.lg.Info("user creds", zap.Reflect("creds", credsFound))
	mid.lg.Info("client crieds", zap.Reflect("creds", credsFound))

	if credsFound.Token != clientCreds.Token {
		return nil, errors.New("password mismatch")
	}

	return handler(ctx, req)
}
