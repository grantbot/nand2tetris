// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// See page 67 for c-bit table
// See page 68 for d-bit table
// See page 69 for j-bit table

         // 0vvv vvvv vvvv vvvv a-instruction
         // 111a cccc ccdd djjj c-instruction
	// R2 = 0
  @0     // 0000 0000 0000 0000
  D=A    // 1110 1100 0001 0000
  @R2    // 0000 0000 0000 0010
  M=D    // 1110 0011 0000 1000

	// i = R0
  @R0    // 0000 0000 0000 0000
  D=M    // 1111 1100 0001 0000
  @i     // 0000 0000 0001 0000 (First variable allocation goes to RAM address 16)
  M=D    // 1110 0011 0000 1000

(LOOP)
  // If i is 0, END
  @i     // 0000 0000 0001 0000 (16)
  D=M    // 1111 1100 0001 0000
  @END   // 0000 0000 0001 0100 (20)
  D;JEQ  // 1110 0011 0000 0010

	// R2 += R1
  @R1    // 0000 0000 0000 0001
  D=M    // 1111 1100 0001 0000
  @R2    // 0000 0000 0000 0010
  M=M+D  // 1111 0000 1000 1000

	// Decrement i
  @i     // 0000 0000 0001 0000 (16)
  M=M-1  // 1111 1100 1000 1000

  @LOOP  // 0000 0000 0000 1000 (8)
  0;JMP  // 1110 1010 1000 0111

(END)
  @END   // 0000 0000 0001 0100 (20)
  0;JMP  // 1110 1010 1000 0111
