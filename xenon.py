#!/usr/bin/python
#encoding:utf-8

# Import standard modules.
import curses
import time

# Import hex2int.
from hex2int import hex2int, int2hex

# Main code

state = {
	'A': '\x00',
	'B': '\x00',
	'C': '\x00',
	'D': '\x00',
	'memory': '\x01\x48\xD6\x01\x65\xD7\x01\x6C\xD8\x01\x6C\xD9\x01\x6F\xDA\x01\x20\xDB\x01\x77\xDC\x01\x6F\xDD\x01\x72\xDE\x01\x6C\xDF\x01\x64\xE0\x01\x21\xE1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\xff',
	'position': '\x00',
	'step': '\x00',
	'register1': '\x00',
	'register2': '\x00',
	'address1': '\x00',
	'address2': '\x00',
	'conditional': '\x00',
	'carry': '\x00',
	'data': '\x00'
}

instruction = 'OFF'

# Initialize Curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.addstr(0, 0, 'Xenon Emulator')
stdscr.refresh()

while state['memory'][255] == '\xff':
	# Get the current piece of memory.
	position = hex2int(state['position'])
	carry = hex2int(state['carry'])
	step = hex2int(state['step'])
	current = state['memory'][position]
	new_carry = carry
	new_step = step
	new_instruction = instruction

	if step == 0:
		# NOP
		if current == '\x00':
			new_instruction = 'NOP'

		# MDM
		if current == '\x01':
			new_instruction = 'MDM'
			new_carry = 1
			new_step = 1

		# FLT
		if current == '\xFF':
			new_instruction = 'FLT'
			state['memory'] = state['memory'][0:255] + '\xfe'

	if step == 1:
		# MDM
		if carry == 1:
			state['data'] = current
			new_step = 2

	if step == 2:
		# MDM
		if carry == 1:
			state['address1'] = current
			new_carry = 0
			new_step = 0
			state['memory'] = state['memory'][0:hex2int(state['address1'])+1] + state['data'] + state['memory'][hex2int(state['address1'])+2:256]

	# Make it slow enough to watch what is happening.
	time.sleep(0.01)

	# Extract video memory.
	vidmem = state['memory'][215:255]

	# Okay. It's done. Let's set up the state.
	new_position = position + 1
	state['position'] = int2hex(new_position)
	state['carry'] = int2hex(new_carry)
	state['step'] = int2hex(new_step)
	instruction = new_instruction

	stdscr.addstr( 2, 10, 'A: 0x%X' % hex2int(state['A']))
	stdscr.addstr( 3, 10, 'B: 0x%X' % hex2int(state['B']))
	stdscr.addstr( 4, 10, 'C: 0x%X' % hex2int(state['C']))
	stdscr.addstr( 5, 10, 'D: 0x%X' % hex2int(state['D']))
	stdscr.addstr( 2, 20+3, 'position: 0x%X' % hex2int(state['position']))
	stdscr.addstr( 3, 20+7, 'step: 0x%X' % hex2int(state['step']))
	stdscr.addstr( 4, 20+2, 'register1: 0x%X' % hex2int(state['register1']))
	stdscr.addstr( 5, 20+2, 'register2: 0x%X' % hex2int(state['register2']))
	stdscr.addstr( 2, 40+3, 'address1: 0x%X' % hex2int(state['address1']))
	stdscr.addstr( 3, 40+3, 'address2: 0x%X' % hex2int(state['address2']))
	stdscr.addstr( 4, 40+0, 'conditional: 0x%X' % hex2int(state['conditional']))
	stdscr.addstr( 5, 40+6, 'fault: 0x%X' % hex2int(state['memory'][255]))
	stdscr.addstr( 2, 60+6, 'carry: 0x%X' % hex2int(state['carry']))
	stdscr.addstr( 3, 60+7, 'data: 0x%X' % hex2int(state['data']))
	stdscr.addstr( 6, 4, 'current: 0x%X' % hex2int(current))
	stdscr.addstr( 7, 5, 'opcode: %s' % new_instruction)
	stdscr.addstr( 8, 38, '|' + vidmem + '|')
	stdscr.addstr( 10, 0, repr(state['memory']))
	stdscr.refresh()

stdscr.addstr(6, 20+6, 'ERROR: A fault occured.')
stdscr.refresh()

while 1:
	pass

curses.endwin()
