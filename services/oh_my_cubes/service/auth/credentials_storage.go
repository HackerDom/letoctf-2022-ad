package auth

import (
	"context"
	"go.uber.org/zap"
	"summer-2022/lib"
)

type CredentialsStorage interface {
	Get(ctx context.Context, login string) (lib.Credentials, error)
	Add(ctx context.Context, creds lib.Credentials) error
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

func (st *EtcdCredentialsStorage) Get(ctx context.Context, token string) (lib.Credentials, error) {
	value, err := st.storage.Get(ctx, "users/"+token)
	if err != nil {
		return lib.Credentials{}, err
	}

	creds, err := lib.Unmarshal[lib.Credentials](value)
	if err != nil {
		return lib.Credentials{}, err
	}

	return *creds, nil
}

func (st *EtcdCredentialsStorage) Add(ctx context.Context, creds lib.Credentials) error {
	key := "users/" + creds.Token

	value, err := lib.Marshal[lib.Credentials](creds)
	if err != nil {
		return err
	}

	err = st.storage.Put(ctx, key, value)
	if err != nil {
		return err
	}

	return nil
}
