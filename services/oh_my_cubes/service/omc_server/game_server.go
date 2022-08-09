package main

import (
	"go.uber.org/zap"
	"summer-2022/omc"
	"summer-2022/proto"
	"time"
)

type OMCService struct {
	proto.UnimplementedOMCServer
	lg *zap.Logger
}

func NewGameService(lg *zap.Logger) proto.OMCServer {
	engine := omc.NewGameEngine(50, 20)
	go engine.SnapshotCreator(time.Millisecond * 100)
	return &OMCService{
		lg: lg,
	}
}
