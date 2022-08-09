package blocks

import "summer-2022/tiles"

type ScreenBuffer struct {
	Tiles [][]*tiles.Tile
}

func NewScreen(width uint, height uint) *ScreenBuffer {
	buffer := make([][]*tiles.Tile, height, height)
	for y := 0; uint(y) < height; y++ {
		buffer[y] = make([]*tiles.Tile, width, width)
	}
	return &ScreenBuffer{
		Tiles: buffer,
	}
}
