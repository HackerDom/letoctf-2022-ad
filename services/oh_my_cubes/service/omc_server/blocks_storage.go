package main

import (
	"context"
	"crypto/sha1"
	"encoding/hex"
	"fmt"
	"github.com/gofrs/uuid"
	"go.uber.org/zap"
	"strings"
	"summer-2022/auth"
	"summer-2022/lib"
	"summer-2022/proto"
	"time"
)

type OmcStorage interface {
	AddBlock(ctx context.Context, block *proto.Block, key string) error
	GetBlocks(ctx context.Context, key string) ([]*proto.Block, error)
	PutSharedBlock(ctx context.Context, block *proto.Block) (*proto.SharedBlock, error)
	GetShared(ctx context.Context, sharedId string) (*proto.SharedBlock, error)
	ListShared(ctx context.Context) ([]string, error)
}

type OmcStorageImpl struct {
	storage      lib.EtcdStorage
	tokenManager auth.TokenManager
	lg           *zap.Logger
}

func NewEtcdOMCStorage(etcdStorage lib.EtcdStorage, lg *zap.Logger) OmcStorage {
	return &OmcStorageImpl{
		storage: etcdStorage,
		lg:      lg,
	}
}

func (st *OmcStorageImpl) AddBlock(ctx context.Context, block *proto.Block, id string) error {
	key := fmt.Sprintf("blocks/%s/%s", id, block.Name)

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

func (st *OmcStorageImpl) GetBlocks(ctx context.Context, token string) ([]*proto.Block, error) {
	key := fmt.Sprintf("blocks/%s", token)
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

func (st *OmcStorageImpl) PutSharedBlock(ctx context.Context, block *proto.Block) (*proto.SharedBlock, error) {
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

func (st *OmcStorageImpl) GetShared(ctx context.Context, sharedId string) (*proto.SharedBlock, error) {
	key := fmt.Sprintf("shared/%s", sharedId)
	get, err := st.storage.Get(ctx, key)
	if err != nil {
		return nil, err
	}
	return lib.Unmarshal[proto.SharedBlock](get)
}

func (st *OmcStorageImpl) ListShared(ctx context.Context) ([]string, error) {
	list, err := st.storage.List(ctx, "shared/")

	if err != nil {
		return nil, err
	}

	var result []string
	for _, s := range list {
		result = append(result, strings.TrimPrefix(s, "shared/"))
	}

	return result, err
}
