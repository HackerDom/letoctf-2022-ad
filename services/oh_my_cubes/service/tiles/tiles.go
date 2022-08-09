package tiles

import "github.com/gdamore/tcell/v2"

const (
	Tile_Empty = 0
	Tile_Dirt  = 1
)

var DefaultStyle = tcell.StyleDefault.Background(tcell.ColorReset).Foreground(tcell.ColorReset)

type Tile struct {
	Rune  rune
	Style tcell.Style
}

var Dirt = Tile{
	Rune:  ' ',
	Style: tcell.StyleDefault.Foreground(tcell.ColorWhite).Background(tcell.ColorDarkGreen),
}

var Empty = Tile{
	Rune:  ' ',
	Style: tcell.StyleDefault.Foreground(tcell.ColorReset).Background(tcell.ColorReset),
}

var tileByIndex = map[byte]Tile{
	Tile_Empty: Empty,
	Tile_Dirt:  Dirt,
}

var indexByTiles map[interface{}]byte

func init() {
	indexByTiles = map[interface{}]byte{}
	for index, tile := range tileByIndex {
		indexByTiles[tile] = index
	}
}

func GetTileSample(index byte) Tile {
	return tileByIndex[index]
}

func GetTileIndex() {

}
