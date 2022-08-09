package omc

import (
	"errors"
	"strconv"
)

const (
	ActionType_Move = 1
)

type Action interface {
	Apply(state *State)
}

type Move struct {
	player  string
	xOffset int
	yOffset int
}

func (m Move) Apply(state *State) {
	//TODO implement me
	panic("implement me")
}

func ParseAction(actionType int, args map[string]string) (Action, error) {
	switch actionType {
	case ActionType_Move:
		xDirectionStr, ok := args["x"]
		if ok {
			return nil, errors.New("can't find x direction")
		}
		yDirectionStr, ok := args["y"]
		if ok {
			return nil, errors.New("can't find y direction")
		}
		xDir, err := strconv.Atoi(xDirectionStr)
		if err != nil {
			return nil, err
		}
		yDir, err := strconv.Atoi(yDirectionStr)
		if err != nil {
			return nil, err
		}

		return Move{
			player:  "player",
			xOffset: xDir % 2,
			yOffset: yDir % 2,
		}, nil
	}
	return nil, nil
}
