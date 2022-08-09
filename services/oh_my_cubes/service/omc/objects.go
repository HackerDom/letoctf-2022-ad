package omc

import "summer-2022/tiles"

type GameObject struct {
	Tile byte
}

type Terrain struct {
	GameObject
	Durability int
}

type Player struct {
	GameObject
	Name   string
	Health uint
}

func NewTileDirt() *Terrain {
	return &Terrain{
		GameObject{Tile: tiles.Tile_Dirt},
		100,
	}
}

var Empty = &GameObject{Tile: tiles.Tile_Empty}
