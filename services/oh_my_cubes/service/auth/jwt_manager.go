package auth

import (
	"context"
	"errors"
	"fmt"
	"github.com/golang-jwt/jwt"
	"go.uber.org/zap"
	"google.golang.org/grpc/metadata"
	"summer-2022/models"
)

type JWTManagerImpl struct {
	hmacSampleSecret []byte
	lg               *zap.Logger
}

func NewJWTManagerImpl(hmacSampleSecret []byte, lg *zap.Logger) *JWTManagerImpl {
	return &JWTManagerImpl{hmacSampleSecret: hmacSampleSecret, lg: lg}
}

func (mng *JWTManagerImpl) GetToken(user models.Credentials) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"user":   user.Login,
		"secret": user.Password,
	})

	tokenString, err := token.SignedString(mng.hmacSampleSecret)
	return tokenString, err
}

func (mng *JWTManagerImpl) parseToken(tokenString string) (models.Credentials, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		}

		return mng.hmacSampleSecret, nil
	})

	if err != nil {
		return models.Credentials{}, err
	}

	if !token.Valid {
		return models.Credentials{}, errors.New("invalid token")
	}

	claims, ok := token.Claims.(jwt.MapClaims)

	if !ok {
		return models.Credentials{}, errors.New("can't parse claims from token")
	}
	mng.lg.Info("claims parsed", zap.Reflect("claims", claims))

	return models.Credentials{
		Login:    claims["user"].(string),
		Password: claims["secret"].(string),
	}, nil
}

func (mng *JWTManagerImpl) ParseCredentials(ctx context.Context) (models.Credentials, error) {
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return models.Credentials{}, errors.New("can't parse metadata")
	}

	data, ok := md[JWT_METADATA]
	if !ok {
		return models.Credentials{}, errors.New("jwt token not provided, plz login first")
	}

	tokenString := data[0]

	clientCreds, err := mng.parseToken(tokenString)
	if err != nil {
		return models.Credentials{}, err
	}
	return clientCreds, err
}

type JWTManager interface {
	GetToken(user models.Credentials) (string, error)
	ParseCredentials(ctx context.Context) (models.Credentials, error)
}
