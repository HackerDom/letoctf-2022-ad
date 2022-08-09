package auth

import (
	"context"
	"go.uber.org/zap"
	"summer-2022/etcd"
	"summer-2022/models"
	"time"
)

type CredentialsStorage interface {
	Get(login string) (models.Credentials, error)
	GetOrAdd(name string, creds models.Credentials) (models.Credentials, error)
}

type EtcdCredentialsStorage struct {
	storage etcd.EtcdStorage
	lg      *zap.Logger
}

func NewEtcdCredentialsStorage(etcdStorage etcd.EtcdStorage, lg *zap.Logger) *EtcdCredentialsStorage {
	return &EtcdCredentialsStorage{
		storage: etcdStorage,
		lg:      lg,
	}
}

func (st *EtcdCredentialsStorage) Get(login string) (models.Credentials, error) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	value, err := st.storage.Get(ctx, "users/"+login)
	if err != nil {
		return models.Credentials{}, err
	}

	creds, err := etcd.Unmarshal[models.Credentials](value)
	if err != nil {
		return models.Credentials{}, err
	}

	return *creds, nil
}

func (st *EtcdCredentialsStorage) GetOrAdd(login string, creds models.Credentials) (models.Credentials, error) {
	value, err := etcd.Marshal[models.Credentials](creds)
	if err != nil {
		return models.Credentials{}, err
	}

	exist, err := st.Get(login)
	if err == nil {
		return exist, nil
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	err = st.storage.Put(ctx, "users/"+login, value)
	if err != nil {
		return models.Credentials{}, err
	}

	return creds, nil
}
