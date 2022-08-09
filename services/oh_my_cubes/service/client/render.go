package main

//type ConsoleRender struct {
//	screen tcell.Screen
//}
//
//func NewConsoleRender(lg *zap.Logger) *ConsoleRender {
//	defStyle := tcell.StyleDefault.Background(tcell.ColorReset).Foreground(tcell.ColorReset)
//
//	// Initialize screen
//	s, err := tcell.NewScreen()
//	if err != nil {
//		log.Fatalf("%+v", err)
//	}
//	if err := s.Init(); err != nil {
//		log.Fatalf("%+v", err)
//	}
//	s.SetStyle(defStyle)
//	s.EnableMouse()
//	s.EnablePaste()
//	s.Clear()
//	return &ConsoleRender{screen: s}
//}
//
//func (r *ConsoleRender) Render(state *proto.State) {
//	//index := state.Tiles[0][0]
//	//tile := tiles.GetTileSample(index)
//	//fmt.Printf("tile %d", index)
//	//return
//	//// Event loop
//	//quit := func() {
//	//	s.Fini()
//	//	os.Exit(0)
//	//}
//	// Update screen
//
//	for x := 0; x < len(state.Tiles); x++ {
//		for y := 0; y < len(state.Tiles[x]); y++ {
//			tile := tiles.GetTileSample(state.Tiles[x][y])
//			r.screen.SetCell(x, y, tile.Style, tile.Rune)
//		}
//	}
//	//r.screen.Sync()
//	r.screen.Show()
//	time.Sleep(time.Millisecond * 100)
//
//	//// Poll event
//	//ev := r.screen.PollEvent()
//	//
//	//// Process event
//	//switch ev := ev.(type) {
//	//case *tcell.EventResize:
//	//	r.screen.Sync()
//	//case *tcell.EventKey:
//	//	if ev.Key() == tcell.KeyEscape || ev.Key() == tcell.KeyCtrlC {
//	//		quit()
//	//	} else if ev.Key() == tcell.KeyCtrlL {
//	//		r.screen.Sync()
//	//	}
//	//}
//}
