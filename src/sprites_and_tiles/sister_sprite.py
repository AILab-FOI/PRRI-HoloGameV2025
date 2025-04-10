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
# 000:000000000000000000000011000001220000123200001151000001490000014a
# 001:0000000000000000110000002310000033210000122100005511000051110000
# 002:0000000000000011000001220000123200001151000001490000014a00000088
# 003:0000000011000000231000003321000012210000551100005111000012100000
# 016:0000008800000899000000890000089900000879000000880000008500000005
# 017:121000002820000078c100009781000077800000881000008510000088500000
# 018:0000089900000089000008990000087900000088000000890000000400000005
# 019:2820000078c10000978100007780000088100000891000008410000005000000
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
# 000:1a1c2c302734553830755d50e6b2aaca917d38b76434718d29366f3b5dc941a6f68dbedaf4f4f494b0c2566c86333c57
# </PALETTE>

