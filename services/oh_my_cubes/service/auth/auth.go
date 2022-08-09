package auth

import (
	"context"
	"crypto/rand"
	"encoding/hex"
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
	clientCredentials := models.Credentials{Login: userInfo.Login, Token: GenerateSecureToken(32)}

	err := auth.userStorage.Add(ctx, clientCredentials)
	if err != nil {
		return nil, err
	}

	token, err := auth.jwt.GetToken(clientCredentials)
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
