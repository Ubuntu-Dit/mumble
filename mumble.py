import curses
import os

class MumbleEditor:
    def __init__(self, stdscr, filename=None):
        self.stdscr = stdscr
        self.filename = filename or "untitled.txt"
        self.text = []
        self.cursor_x = 0
        self.cursor_y = 0
        self.load_file()

    def load_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.text = f.read().splitlines()
        else:
            self.text = [""]

    def save_file(self):
        with open(self.filename, 'w') as f:
            f.write('\n'.join(self.text))

    def run(self):
        curses.curs_set(1)
        while True:
            self.stdscr.clear()
            for idx, line in enumerate(self.text):
                self.stdscr.addstr(idx, 0, line)
            self.stdscr.move(self.cursor_y, self.cursor_x)
            self.stdscr.refresh()

            key = self.stdscr.getch()
            if key == 27:  # ESC to exit
                break
            elif key == curses.KEY_BACKSPACE or key == 127:
                self.text[self.cursor_y] = self.text[self.cursor_y][:-1]
                self.cursor_x = max(0, self.cursor_x - 1)
            elif key == curses.KEY_ENTER or key == 10:
                self.text.insert(self.cursor_y + 1, "")
                self.cursor_y += 1
                self.cursor_x = 0
            elif key == curses.KEY_UP:
                self.cursor_y = max(0, self.cursor_y - 1)
            elif key == curses.KEY_DOWN:
                self.cursor_y = min(len(self.text) - 1, self.cursor_y + 1)
            elif key == curses.KEY_LEFT:
                self.cursor_x = max(0, self.cursor_x - 1)
            elif key == curses.KEY_RIGHT:
                self.cursor_x = min(len(self.text[self.cursor_y]), self.cursor_x + 1)
            else:
                ch = chr(key)
                line = self.text[self.cursor_y]
                self.text[self.cursor_y] = line[:self.cursor_x] + ch + line[self.cursor_x:]
                self.cursor_x += 1

def main(stdscr):
    editor = MumbleEditor(stdscr, "mumble.txt")
    editor.run()

curses.wrapper(main)
