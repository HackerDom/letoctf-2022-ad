package auth

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"go.uber.org/zap"
	"summer-2022/lib"
	"summer-2022/proto"
)

type AuthService struct {
	proto.UnimplementedAuthServer
	userStorage  CredentialsStorage
	tokenManager TokenManager
	lg           *zap.Logger
}

func NewAuthService(userStorage CredentialsStorage, tokenManager TokenManager, lg *zap.Logger) proto.AuthServer {
	return &AuthService{
		userStorage:  userStorage,
		tokenManager: tokenManager,
		lg:           lg,
	}
}

func (auth *AuthService) SignUp(ctx context.Context, userInfo *proto.UserInfo) (*proto.AuthInfo, error) {
	clientCredentials := lib.Credentials{Login: userInfo.Login, Token: GenerateSecureToken(32)}

	err := auth.userStorage.Add(ctx, clientCredentials)
	if err != nil {
		return nil, err
	}

	token, err := auth.tokenManager.GetToken(clientCredentials)
	if err != nil {
		return nil, err
	}

	return &proto.AuthInfo{Token: token}, nil
}

func GenerateSecureToken(length int) string {
	b := make([]byte, length)
	if _, err := rand.Read(b); err != nil {
		panic(err.Error())
	}
	return hex.EncodeToString(b)
}
