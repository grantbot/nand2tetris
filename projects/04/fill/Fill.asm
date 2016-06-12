// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

(LISTEN)
  @KBD
  D=M

  // White if no key pressed
  @DRAWWHITE
  D;JEQ

  // Otherwise black
  @DRAWBLACK
  0;JMP

(DRAWBLACK)
  @color  // Memory[16]
  M=-1  // '1111111111111111' in 2's complement

  @INITDRAW
  0;JMP

(DRAWWHITE)
  @color
  M=0  // '0000000000000000'

  @INITDRAW
  0;JMP

(INITDRAW)
  // Initialize cursor to first word of screen (top-left)
  @SCREEN
  D=A

  @cursor  // Memory[17]
  M=D

(DRAW)
  // Base case. Keyboard's memory block is immediately adjacent to screen's.
  // So we know to stop if our cursor is pointing at the first word in the keyboard's
  // map, which is referenced by KBD.
  @cursor
  D=M

  @KBD
  D=D-A

  @LISTEN
  D;JEQ

  @color
  D=M  // Load desired color

  @cursor
  A=M  // Deref. Memory[17] stores an address we want to access.
  M=D  // Draw

  @cursor
  M=M+1  // Inc cursor to next word.

  @DRAW
  0;JMP


