package auth

import (
	"context"
	"errors"
	"go.uber.org/zap"
	"summer-2022/lib"
	"summer-2022/models"
)

type CredentialsStorage interface {
	Get(ctx context.Context, login string) (models.Credentials, error)
	Add(ctx context.Context, creds models.Credentials) error
}

type EtcdCredentialsStorage struct {
	storage lib.EtcdStorage
	lg      *zap.Logger
}

func NewEtcdCredentialsStorage(etcdStorage lib.EtcdStorage, lg *zap.Logger) *EtcdCredentialsStorage {
	return &EtcdCredentialsStorage{
		storage: etcdStorage,
		lg:      lg,
	}
}

func (st *EtcdCredentialsStorage) Get(ctx context.Context, token string) (models.Credentials, error) {
	value, err := st.storage.Get(ctx, "users/"+token)
	if err != nil {
		return models.Credentials{}, err
	}

	creds, err := lib.Unmarshal[models.Credentials](value)
	if err != nil {
		return models.Credentials{}, err
	}

	return *creds, nil
}

func (st *EtcdCredentialsStorage) Add(ctx context.Context, creds models.Credentials) error {
	key := "users/" + creds.Token
	exist, err := st.storage.Exist(ctx, key)
	if err != nil {
		return err
	}

	if exist {
		return errors.New("already exist")
	}

	value, err := lib.Marshal[models.Credentials](creds)
	if err != nil {
		return err
	}

	err = st.storage.Put(ctx, key, value)
	if err != nil {
		return err
	}

	return nil
}
