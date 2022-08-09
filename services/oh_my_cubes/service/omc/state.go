package omc

type State struct {
	Width    int
	Height   int
	Map      [][]*GameObject
	snapshot [][]byte
	players  map[string]*Player
}

func (s *State) createSnapshot() {
	snapshot := make([][]byte, s.Width, s.Width)
	for x := 0; x < s.Width; x++ {
		snapshot[x] = make([]byte, s.Height, s.Height)
		for y := 0; y < s.Height; y++ {
			tile := s.Map[x][y].Tile
			snapshot[x][y] = tile
		}
	}

	s.snapshot = snapshot
}
