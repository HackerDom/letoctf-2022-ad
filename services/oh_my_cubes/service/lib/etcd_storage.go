package lib

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"go.etcd.io/etcd/api/v3/mvccpb"
	"go.etcd.io/etcd/client/v3"
	"go.uber.org/zap"
	"time"
)

func Marshal[V any](value V) (string, error) {
	marshal, err := json.Marshal(value)
	if err != nil {
		return "", err
	}

	return string(marshal), nil
}

func Unmarshal[V any](value string) (*V, error) {
	result := new(V)
	err := json.Unmarshal([]byte(value), &result)
	if err != nil {
		return nil, err
	}

	return result, nil
}

type EtcdStoreImpl struct {
	client *clientv3.Client
}

func (etcd *EtcdStoreImpl) Put(ctx context.Context, key string, value string) error {
	_, err := etcd.client.Put(ctx, key, value)
	if err != nil {
		return err
	}

	return nil
}

func (etcd *EtcdStoreImpl) Get(ctx context.Context, key string) (string, error) {
	result, err := etcd.client.KV.Get(ctx, key)
	if err != nil {
		return "", err
	}

	if len(result.Kvs) == 0 {
		return "", errors.New("result for key " + key + "is empty")
	}
	return string(result.Kvs[0].Value), nil
}

func (etcd *EtcdStoreImpl) List(ctx context.Context, key string) ([]string, error) {
	result, err := etcd.client.KV.Get(ctx, key)
	if err != nil {
		return nil, err
	}

	var keys []string
	for _, kv := range result.Kvs {
		keys = append(keys, string(kv.Key))
	}

	return keys, nil
}

func (etcd *EtcdStoreImpl) GetRange(ctx context.Context, key string) ([]*mvccpb.KeyValue, error) {
	result, err := etcd.client.Get(ctx, key, clientv3.WithPrefix())
	if err != nil {
		return nil, err
	}
	return result.Kvs, nil
}

func NewEtcdStorage(target string, logger *zap.Logger) EtcdStorage {
	client, err := clientv3.New(clientv3.Config{
		Endpoints:   []string{fmt.Sprintf("http://%s", target)},
		DialTimeout: 2 * time.Second,
	})

	if err == context.DeadlineExceeded {
		logger.Fatal("can't connect to etcd")
	}

	return &EtcdStoreImpl{
		client: client,
	}
}

type EtcdStorage interface {
	Put(ctx context.Context, key string, value string) error
	Get(ctx context.Context, key string) (string, error)
	GetRange(ctx context.Context, key string) ([]*mvccpb.KeyValue, error)
	List(ctx context.Context, key string) ([]string, error)
}
