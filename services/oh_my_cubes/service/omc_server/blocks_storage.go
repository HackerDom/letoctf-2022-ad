package main

import (
	"context"
	"crypto/sha1"
	"encoding/hex"
	"fmt"
	"github.com/gofrs/uuid"
	"go.uber.org/zap"
	"summer-2022/auth"
	"summer-2022/lib"
	"summer-2022/proto"
	"time"
)

type BlocksStorage interface {
	AddBlock(ctx context.Context, block *proto.Block) error
	GetBlock(ctx context.Context, name string) ([]*proto.Block, error)
	PutSharedBlock(ctx context.Context, block *proto.Block) (*proto.SharedBlock, error)
	GetShared(ctx context.Context, sharedId string) (*proto.SharedBlock, error)
}

type BlocksStorageImpl struct {
	storage    lib.EtcdStorage
	jwtManager auth.JWTManager
	lg         *zap.Logger
}

func NewEtcdOMCStorage(etcdStorage lib.EtcdStorage, lg *zap.Logger) BlocksStorage {
	return &BlocksStorageImpl{
		storage: etcdStorage,
		lg:      lg,
	}
}

func (st *BlocksStorageImpl) AddBlock(ctx context.Context, block *proto.Block) error {
	credentials, err := st.jwtManager.ParseCredentials(ctx)
	if err != nil {
		return err
	}

	//TODO:fix size
	key := fmt.Sprintf("blocks/%s/%s", credentials.Login, block.Name)

	marshal, err := lib.Marshal[*proto.Block](block)
	if err != nil {
		return err
	}
	err = st.storage.Put(ctx, key, marshal)
	if err != nil {
		return err
	}
	return nil
}

func (st *BlocksStorageImpl) GetBlock(ctx context.Context, name string) ([]*proto.Block, error) {
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
		block, err := lib.Unmarshal[proto.Block](string(kv.Value))
		if err != nil {
			return nil, err
		}
		blocks = append(blocks, block)
	}

	return blocks, nil
}

func (st *BlocksStorageImpl) PutSharedBlock(ctx context.Context, block *proto.Block) (*proto.SharedBlock, error) {
	adminKey, err := uuid.NewV1()
	if err != nil {
		return nil, err
	}

	h := sha1.New()
	h.Write([]byte(adminKey.String()))
	sharedId := hex.EncodeToString(h.Sum(nil))
	key := fmt.Sprintf("shared/%s", sharedId)

	shared := &proto.SharedBlock{
		Metadata: &proto.BlockMetadata{
			CreatedAt: time.Now().UnixNano(),
			SharedId:  sharedId,
		},
		Block:    block,
		AdminKey: adminKey.String(),
	}

	marshal, err := lib.Marshal[*proto.SharedBlock](shared)
	if err != nil {
		return nil, err
	}

	err = st.storage.Put(ctx, key, marshal)
	if err != nil {
		return nil, err
	}

	return shared, nil
}

func (st *BlocksStorageImpl) GetShared(ctx context.Context, sharedId string) (*proto.SharedBlock, error) {
	key := fmt.Sprintf("shared/%s", sharedId)
	get, err := st.storage.Get(ctx, key)
	if err != nil {
		return nil, err
	}
	return lib.Unmarshal[proto.SharedBlock](get)
}
