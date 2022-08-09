package main

import (
	"context"
	"fmt"
	"go.uber.org/zap"
	"summer-2022/auth"
	"summer-2022/proto"
)

/*
creds/login creds
blocks/login []block

realms/name realm{admin, data}
create
get_admin
get
list
*/

type EtcdGameStorageStorage struct {
	storage    EtcdStorage
	jwtManager auth.JWTManager
	lg         *zap.Logger
}

func NewEtcdGameStorage(etcdStorage EtcdStorage, lg *zap.Logger) *EtcdGameStorageStorage {
	return &EtcdGameStorageStorage{
		storage: etcdStorage,
		lg:      lg,
	}
}

func (st *EtcdGameStorageStorage) AddBlock(ctx context.Context, block *proto.Block) error {
	credentials, err := st.jwtManager.ParseCredentials(ctx)
	if err != nil {
		return err
	}

	marshal, err := Marshal[*proto.Block](block)
	if err != nil {
		return err
	}

	//TODO:fix size
	key := fmt.Sprintf("blocks/%s/%s", credentials.Login, block.Name)
	err = st.storage.Put(ctx, key, marshal)
	if err != nil {
		return err
	}
	return nil
}

func (st *EtcdGameStorageStorage) GetBlock(ctx context.Context, name string) ([]*proto.Block, error) {
	credentials, err := st.jwtManager.ParseCredentials(ctx)
	if err != nil {
		return nil, err
	}

	//TODO:fix size
	key := fmt.Sprintf("blocks/%s/%s", credentials.Login, name)
	kvs, err := st.storage.GetRange(ctx, key)
	if err != nil {
		return nil, err
	}

	var blocks []*proto.Block
	for _, kv := range kvs {
		block, err := Unmarshal[proto.Block](string(kv.Value))
		if err != nil {
			return nil, err
		}
		blocks = append(blocks, block)
	}

	return blocks, nil
}
