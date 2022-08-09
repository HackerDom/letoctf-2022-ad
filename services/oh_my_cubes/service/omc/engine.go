package omc

import (
	"errors"
	"math/rand"
	"sync"
	"time"
)

type GameEngine struct {
	actions chan Action
	state   *State
	mut     sync.Mutex
}

func NewGameEngine(width int, height int) *GameEngine {
	state := &State{
		Width:    width,
		Height:   height,
		Map:      make([][]*GameObject, width, width),
		snapshot: nil,
	}

	for i := 0; i < width; i++ {
		for j := 0; j < height; j++ {
			state.Map[i] = make([]*GameObject, height, height)
		}
	}

	engine := &GameEngine{
		actions: make(chan Action),
		state:   state,
		mut:     sync.Mutex{},
	}

	engine.generateMaze()
	state.createSnapshot()

	return engine
}

func (engine *GameEngine) GetSnapshot() [][]byte {
	return engine.state.snapshot
}

func (engine *GameEngine) GetPlayer(login string) (*Player, error) {
	player, ok := engine.state.players[login]
	if !ok {
		return nil, errors.New("player not exist")
	}

	return player, nil
}

func (engine *GameEngine) ApplyAction(action Action) {
	engine.actions <- action
}

func (engine *GameEngine) StartActionMonitor() {
	for {
		select {
		case action := <-engine.actions:
			engine.mut.Lock()
			action.Apply(engine.state)
			engine.mut.Unlock()
		}
	}
}

func (engine *GameEngine) SnapshotCreator(period time.Duration) {
	for range time.Tick(period) {
		engine.mut.Lock()
		engine.state.createSnapshot()
		engine.mut.Unlock()
	}
}

func (engine *GameEngine) generateMaze() {
	rand.Seed(time.Now().UnixNano())
	state := engine.state

	for x := 0; x < state.Width; x++ {
		for y := 0; y < state.Height; y++ {
			if x%2 == 0 {
				dirt := NewTileDirt()
				state.Map[x][y] = &dirt.GameObject
			} else {
				state.Map[x][y] = Empty
			}
		}
	}
}
