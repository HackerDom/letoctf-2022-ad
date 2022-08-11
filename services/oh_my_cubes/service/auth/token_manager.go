package auth

import (
	"context"
	"encoding/json"
	"errors"
	"go.uber.org/zap"
	"google.golang.org/grpc/metadata"
	"summer-2022/lib"
)

type TokenManagerImpl struct {
	lg *zap.Logger
}

func NewTokenManagerImpl(lg *zap.Logger) *TokenManagerImpl {
	return &TokenManagerImpl{lg: lg}
}

func (mng *TokenManagerImpl) GetToken(user lib.Credentials) (string, error) {
	marshal, err := json.Marshal(user)
	if err != nil {
		return "", err
	}

	return string(marshal), nil
}

func (mng *TokenManagerImpl) parseToken(tokenString string) (lib.Credentials, error) {
	var creds lib.Credentials
	err := json.Unmarshal([]byte(tokenString), &creds)
	if err != nil {
		return lib.Credentials{}, err
	}

	return creds, nil
}

func (mng *TokenManagerImpl) ParseCredentials(ctx context.Context) (lib.Credentials, error) {
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return lib.Credentials{}, errors.New("can't parse metadata")
	}

	data, ok := md[METADATA_KEY]
	if !ok {
		return lib.Credentials{}, errors.New("tokenManager token not provided, plz login first")
	}

	tokenString := data[0]

	clientCreds, err := mng.parseToken(tokenString)
	if err != nil {
		return lib.Credentials{}, err
	}
	return clientCreds, err
}

type TokenManager interface {
	GetToken(user lib.Credentials) (string, error)
	ParseCredentials(ctx context.Context) (lib.Credentials, error)
}
