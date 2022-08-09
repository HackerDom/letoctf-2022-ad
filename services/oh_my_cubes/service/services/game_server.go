package services

import (
	"context"
	"go.uber.org/zap"
	"summer-2022/auth"
	"summer-2022/omc"
	"summer-2022/proto"
	"time"
)

type GameService struct {
	proto.UnimplementedOMCServer
	lg     *zap.Logger
	engine *omc.GameEngine
}

func NewGameService(lg *zap.Logger) proto.OMCServer {
	engine := omc.NewGameEngine(50, 20)
	go engine.SnapshotCreator(time.Millisecond * 100)
	return &GameService{
		lg:     lg,
		engine: engine,
	}
}

func (s *GameService) GetState(ctx context.Context, empty *proto.Empty) (*proto.State, error) {
	user := auth.GetUser(ctx)
	s.lg.Info("Get state called by user " + user)
	return &proto.State{
		Character: &proto.CharacterInfo{
			Health: 0,
		},
		Tiles: s.engine.GetSnapshot(),
	}, nil
}

func (s *GameService) SendAction(ctx context.Context, action *proto.Action) (*proto.State, error) {
	user := auth.GetUser(ctx)

	s.lg.Info("Send action called by user "+user, zap.Reflect("action", action))
	return nil, nil
}
