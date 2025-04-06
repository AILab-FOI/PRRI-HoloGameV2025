-- title:   game title
-- author:  game developer, email, etc.
-- desc:    short description
-- site:    website link
-- license: MIT License (change this to your license of choice)
-- version: 0.1
-- script:  lua

t=0
x=96
y=24

function TIC()

	if btn(0) then y=y-1 end
	if btn(1) then y=y+1 end
	if btn(2) then x=x-1 end
	if btn(3) then x=x+1 end

	cls(13)
	spr(1+t%60//30*2,x,y,14,3,0,0,2,2)
	print("HELLO WORLD!",84,84)
	t=t+1
end

# <TILES>
# 000:00000000000000aa00000aaa0000aaaa00009aaa000099990000dd2d0000dddd
# 001:00000000a0000000aaa00000aaa00000aaa00000999000009d900000dd000000
# 002:000000aa00000aaa0000aaaa00009aaa000099990000dd2d0000dddd0000ccdd
# 003:a0000000aaa00000aaa00000aaa00000999000009d900000dd000000d0000000
# 016:0000ccdd00000ded00000eed00000eee00000eed000022220000220000033203
# 017:d0000000dd000000de000000d000000000000000220000002200000033000000
# 018:00000ded00000eed00000eee00000eed0000022e000002220000033200003303
# 019:dd000000de000000d000000000000000d0000000200000003000000030000000
# </TILES>

# <WAVES>
# 000:00000000ffffffff00000000ffffffff
# 001:0123456789abcdeffedcba9876543210
# 002:0123456789abcdef0123456789abcdef
# </WAVES>

# <SFX>
# 000:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000304000000000
# </SFX>

# <TRACKS>
# 000:100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </TRACKS>

# <PALETTE>
# 000:1a1c2c5d275dfa0c34ff9d65ffe255a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2565591333c57
# </PALETTE>

