package auth

import (
	"context"
	"errors"
	"go.uber.org/zap"
	"summer-2022/models"
	"summer-2022/proto"
)

type AuthService struct {
	proto.UnimplementedAuthServer
	userStorage CredentialsStorage
	jwt         JWTManager
	lg          *zap.Logger
}

func NewAuthService(userStorage CredentialsStorage, jwt JWTManager, lg *zap.Logger) proto.AuthServer {
	return &AuthService{
		userStorage: userStorage,
		jwt:         jwt,
		lg:          lg,
	}
}

func (auth *AuthService) SignIn(ctx context.Context, userInfo *proto.UserInfo) (*proto.AuthInfo, error) {
	clientCredentials := models.Credentials{Login: userInfo.Login, Password: userInfo.Password}

	foundCreds, err := auth.userStorage.GetOrAdd(userInfo.Login, clientCredentials)
	if err != nil {
		return nil, err
	}

	if clientCredentials.Password != foundCreds.Password {
		return nil, errors.New("password mismatch")
	}

	token, err := auth.jwt.GetToken(clientCredentials)
	if err != nil {
		return nil, err
	}

	return &proto.AuthInfo{Token: token}, nil
}
