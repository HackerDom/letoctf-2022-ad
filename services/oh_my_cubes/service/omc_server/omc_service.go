package main

import (
	"context"
	"go.uber.org/zap"
	"summer-2022/auth"
	"summer-2022/proto"
)

type OMCService struct {
	proto.UnimplementedOMCServer
	storage    BlocksStorage
	jwtManager auth.JWTManager
	lg         *zap.Logger
}

func (omc *OMCService) AddBlock(ctx context.Context, block *proto.Block) (*proto.Empty, error) {
	credentials, err := omc.jwtManager.ParseCredentials(ctx)
	if err != nil {
		return nil, err
	}

	err = omc.storage.AddBlock(ctx, block, credentials.Token)
	if err != nil {
		return nil, err
	}

	return &proto.Empty{}, err
}

func (omc *OMCService) GetBlocks(_ *proto.Empty, server proto.OMC_GetBlocksServer) error {
	credentials, err := omc.jwtManager.ParseCredentials(server.Context())
	if err != nil {
		return err
	}

	blocks, err := omc.storage.GetBlocks(server.Context(), credentials.Token)
	if err != nil {
		return err
	}
	for _, block := range blocks {
		err := server.SendMsg(block)
		if err != nil {
			return err
		}
	}

	return nil
}

func (omc *OMCService) PutShared(ctx context.Context, block *proto.Block) (*proto.SharedBlockCreateResponse, error) {
	sharedBlock, err := omc.storage.PutSharedBlock(ctx, block)
	if err != nil {
		return nil, err
	}

	return &proto.SharedBlockCreateResponse{
		Metadata: sharedBlock.Metadata,
		AdminKey: sharedBlock.AdminKey,
	}, nil
}

func (omc *OMCService) GetShared(ctx context.Context, request *proto.GetSharedBlock) (*proto.SharedBlock, error) {
	shared, err := omc.storage.GetShared(ctx, request.SharedId)
	if err != nil {
		return nil, err
	}

	if shared.AdminKey != request.AdminKey {
		shared.Metadata.SecretNotes = "*********"
		shared.AdminKey = "*********"
	}

	return shared, nil
}

func NewGameService(lg *zap.Logger) proto.OMCServer {
	return &OMCService{
		lg: lg,
	}
}
