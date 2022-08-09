package blocks

import (
	"fmt"
	"github.com/gdamore/tcell/v2"
	"log"
	"os"
	"summer-2022/tiles"
)

type Game struct {
	gameMap ScreenBuffer
}

func (g *Game) Render() {
	boxStyle := tcell.StyleDefault.Foreground(tcell.ColorWhite).Background(tcell.ColorDodgerBlue)

	// Initialize screen
	s, err := tcell.NewScreen()
	if err != nil {
		log.Fatalf("%+v", err)
	}
	if err := s.Init(); err != nil {
		log.Fatalf("%+v", err)
	}
	s.SetStyle(tiles.DefaultStyle)
	s.EnableMouse()
	s.EnablePaste()
	s.Clear()

	// Event loop
	ox, oy := -1, -1
	quit := func() {
		s.Fini()
		os.Exit(0)
	}

	for {
		for {

		}
		// Update screen
		s.Show()
		// Poll event
		ev := s.PollEvent()

		processEvent(ev, s, quit, ox, oy, boxStyle)
	}
}

func processEvent(ev tcell.Event, s tcell.Screen, quit func(), ox int, oy int, boxStyle tcell.Style) {
	// Process event
	switch ev := ev.(type) {
	case *tcell.EventResize:
		s.Sync()
	case *tcell.EventKey:
		if ev.Key() == tcell.KeyEscape || ev.Key() == tcell.KeyCtrlC {
			quit()
		} else if ev.Key() == tcell.KeyCtrlL {
			s.Sync()
		} else if ev.Rune() == 'C' || ev.Rune() == 'c' {
			s.Clear()
		}
	case *tcell.EventMouse:
		x, y := ev.Position()
		button := ev.Buttons()
		// Only process button events, not wheel events
		button &= tcell.ButtonMask(0xff)

		if button != tcell.ButtonNone && ox < 0 {
			ox, oy = x, y
		}
		switch ev.Buttons() {
		case tcell.ButtonNone:
			if ox >= 0 {
				label := fmt.Sprintf("%d,%d to %d,%d", ox, oy, x, y)
				drawBox(s, ox, oy, x, y, boxStyle, label)
				ox, oy = -1, -1
			}
		}
	}
}

func drawBox(s tcell.Screen, x1, y1, x2, y2 int, style tcell.Style, text string) {
	if y2 < y1 {
		y1, y2 = y2, y1
	}
	if x2 < x1 {
		x1, x2 = x2, x1
	}

	// Fill background
	for row := y1; row <= y2; row++ {
		for col := x1; col <= x2; col++ {
			s.SetContent(col, row, ' ', nil, style)
		}
	}

	// Draw borders
	for col := x1; col <= x2; col++ {
		s.SetContent(col, y1, tcell.RuneHLine, nil, style)
		s.SetContent(col, y2, tcell.RuneHLine, nil, style)
	}
	for row := y1 + 1; row < y2; row++ {
		s.SetContent(x1, row, tcell.RuneVLine, nil, style)
		s.SetContent(x2, row, tcell.RuneVLine, nil, style)
	}

	// Only draw corners if necessary
	if y1 != y2 && x1 != x2 {
		s.SetContent(x1, y1, tcell.RuneULCorner, nil, style)
		s.SetContent(x2, y1, tcell.RuneURCorner, nil, style)
		s.SetContent(x1, y2, tcell.RuneLLCorner, nil, style)
		s.SetContent(x2, y2, tcell.RuneLRCorner, nil, style)
	}

	drawText(s, x1+1, y1+1, x2-1, y2-1, style, text)
}

func drawText(s tcell.Screen, x1, y1, x2, y2 int, style tcell.Style, text string) {
	row := y1
	col := x1
	for _, r := range []rune(text) {
		s.SetContent(col, row, r, nil, style)
		col++
		if col >= x2 {
			row++
			col = x1
		}
		if row > y2 {
			break
		}
	}
}
