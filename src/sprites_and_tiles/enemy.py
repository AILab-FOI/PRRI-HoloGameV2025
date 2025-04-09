-- title:   game title
-- author:  game developer, email, etc.
-- desc:    short description
-- site:    website link
-- license: MIT License (change this to your license of choice)
-- version: 0.1
-- script:  python


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
# 001:ccc00000cc00eeeecb0eee00cb0ee002cc0ee020cb0fe020cca0ff02cc000fff
# 002:0ccccccc00ccccccf00ccccc2f0ccccc4f0ccccc3f0ccccc200ccccc00cccccc
# 003:cccbcc00ccccc0eeccbc0eeeccbb0ee0cccb0ee0ccba0fe0cccaa0ffcccc000f
# 004:000ccccceee0cbcc000e0ccc02200bcc20420bcc20320ccc02200cccff00cccc
# 005:cccccc00ccccc00ecccc00eecccc0feecccc0feecccc0ffecccc00ffccccc000
# 006:000ccccceee0cccceeee0ccce0220ccce0240ccce0220cccff000cccfff0cccc
# 007:cccccc00ccccc00ecccc00eecccc0feecccc0feecccc0ffecccc00ffccc0e000
# 008:000cccccee00cccceee00ccce0f20ccce0f20ccce0f20cccff000cccfff0cccc
# 009:cbc00000cc00eeeebc0eeee0bb0ee002cb0ee020c90ee020cc90ff02c0000fff
# 010:cccccccc0cccccccf0cccccc00cccccc20cccccc20cccccc00cccccc0ccccccc
# 011:cccccc00ccccc00ecccc00eecccc0feecccc0feecccc0ffecccc00ffcccc0e00
# 012:000ccccceee0cccceeee0ccce0020ccce0020ccce0020cccff000cccfff0cccc
# 013:cccccc00ccccc00ecccc00eecccc0feecccc0feecccc0ffecccc00ffccccc000
# 014:000ccccceee0cccceeee0ccce0000ccce0020ccce0020cccff000cccfff0cccc
# 017:c0ee0000c0e00eee0ff00ff00f000000c00ee000cc0f0cc0c000ccc0c000ccc0
# 018:0f0ccccc000cccccc0f0ccccc000cccc0cccccccfcccccccf0cccccc00cccccc
# 019:ccc0ee00ccc0e00eccc0f00fccc0ff00cccc00e0ccccc0f0cccc000ccccc000c
# 020:00000ccceee00cccff00e0cc00c000cc000cccccc0fcccccc0f0ccccc000cccc
# 021:cccc0ef0cccc0e00cccc0ff0cccc0ff0ccccc00ecccccc00ccccc00cccccc000
# 022:000cccccee0cccccf000cccc0000cccc000cccccc00cccccc0e0ccccc000cccc
# 023:ccc0f0e0ccc000e0cc0f000ecc000000cccc000fccc000c0cc000cc0cc000cc0
# 024:000ccccc0ccccccce0cccccc00cccccc0ccccccc0cccccccf0cccccc00cccccc
# 025:0eef00000f00fff00ff0ff0cc0000000cc0e0000cc0f0c0fc000cc00c000cc00
# 026:0ccccccc000ccccc000ccccccccccccccccccccc0ccccccc0ccccccc0ccccccc
# 027:ccc0ef00ccc0e00fccc0ff0fcccc0000ccccc0f0cccc000cccc000ccccc000cc
# 028:000cccccff0cccccf0000ccc0c000ccc00cccccc0f0ccccc000ccccc000ccccc
# 029:cccc00e0cccc0e00ccc00e0fccc00ff0cccc0000cccc00ccccc00cccccc000cc
# 030:000ccccc00ccccccf000cccc0000cccc00cccccc0f0ccccc000ccccc000ccccc
# 033:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# 034:ccccccccccccccccccccccccccccccccccccccccccccccccccccccccc00ccccc
# 049:cccccc0cccc00c00ccc0000cccc00000cc00000fc000cc0f000ccc0000cccc00
# 050:c0c00ccc0000cccccccccccccccccccc0ccccccc0ccccccccccccccc0ccccccc
# </TILES>

# <SPRITES>
# 000:ccc00000cc00eeeecb0eee00cb0ee002cc0ee020cb0fe020cca0ff02cc000fff
# 001:0ccccccc00ccccccf00ccccc2f0ccccc4f0ccccc3f0ccccc200ccccc00cccccc
# 002:cccbcc00ccccc0eeccbc0eeeccbb0ee0cccb0ee0ccba0fe0cccaa0ffcccc000f
# 003:000ccccceee0cbcc000e0ccc02200bcc20420bcc20320ccc02200cccff00cccc
# 004:cccccc00ccccc00ecccc00eecccc0feecccc0feecccc0ffecccc00ffccccc000
# 005:000ccccceee0cccceeee0ccce0220ccce0240ccce0220cccff000cccfff0cccc
# 006:cccccc00ccccc00ecccc00eecccc0feecccc0feecccc0ffecccc00ffccc0e000
# 007:000cccccee00cccceee00ccce0f20ccce0f20ccce0f20cccff000cccfff0cccc
# 008:cbc00000cc00eeeebc0eeee0bb0ee002cb0ee020c90ee020cc90ff02c0000fff
# 009:cccccccc0cccccccf0cccccc00cccccc20cccccc20cccccc00cccccc0ccccccc
# 010:cccccc00ccccc00ecccc00eecccc0feecccc0feecccc0ffecccc00ffcccc0e00
# 011:000ccccceee0cccceeee0ccce0020ccce0020ccce0020cccff000cccfff0cccc
# 012:cccccc00ccccc00ecccc00eecccc0feecccc0feecccc0ffecccc00ffccccc000
# 013:000ccccceee0cccceeee0ccce0000ccce0020ccce0020cccff000cccfff0cccc
# 014:cccccccccccccc00ccccc00ecccc00eecccc0feecccc0feecccc000eccc00f0f
# 015:cccccccc000ccccceee0cccce0000ccc00220ccc00240cccf0230cccff00cccc
# 016:c0ee0000c0e00eee0ff00ff00f000000c00ee000cc0f0cc0c000ccc0c000ccc0
# 017:0f0ccccc000cccccc0f0ccccc000cccc0cccccccfcccccccf0cccccc00cccccc
# 018:ccc0ee00ccc0e00eccc0f00fccc0ff00cccc00e0ccccc0f0cccc000ccccc000c
# 019:00000ccceee00cccff00e0cc00c000cc000cccccc0fcccccc0f0ccccc000cccc
# 020:cccc0ef0cccc0e00cccc0ff0cccc0ff0ccccc00ecccccc00ccccc00cccccc000
# 021:000cccccee0cccccf000cccc0000cccc000cccccc00cccccc0e0ccccc000cccc
# 022:ccc0f0e0ccc000e0cc0f000ecc000000cccc000fccc000c0cc000cc0cc000cc0
# 023:000ccccc0ccccccce0cccccc00cccccc0ccccccc0cccccccf0cccccc00cccccc
# 024:0eef00000f00fff00ff0ff0cc0000000cc0e0000cc0f0c0fc000cc00c000cc00
# 025:0ccccccc000ccccc000ccccccccccccccccccccc0ccccccc0ccccccc0ccccccc
# 026:ccc0ef00ccc0e00fccc0ff0fcccc0000ccccc0f0cccc000cccc000ccccc000cc
# 027:000cccccff0cccccf0000ccc0c000ccc00cccccc0f0ccccc000ccccc000ccccc
# 028:cccc00e0cccc0e00ccc00e0fccc00ff0cccc0000cccc00ccccc00cccccc000cc
# 029:000ccccc00ccccccf000cccc0000cccc00cccccc0f0ccccc000ccccc000ccccc
# 030:cc0e0000c0e0c00fc000c000cc0cc000ccc00000cc000cc0c000ccc0c00cccc0
# 031:0f0e000c000000cc0ccccccc0cccccccf0ccccccf0cccccc0ccccccc00cccccc
# 032:ccccccccccccccccccccccccccccccccccccccccccccc000cccc00eeccc00eee
# 033:cccccccccccccccccccccccccccccccccccccccc00ccccccee0ccccc0000cccc
# 034:ccccccccccccccccccccccccccccccccccccccccccccc000cccc00eeccc00eee
# 035:cccccccccccccccccccccccccccccccccccccccc00ccccccee0ccccc0000cccc
# 048:ccc0fee0ccc0fee0ccc00feecccc00ffcc00e000cc0f00ffcc0f00f0ccc0f000
# 049:0220cccc0240cccc0220ccccf00ccccc00cccccc00cccccc0000ccccc000cccc
# 050:ccc00ee0ccc00ee0cccc0fffccc000ffcc0ee000c0f000ffc0ff00f0ccc00000
# 051:0220cccc0200cccc0220ccccf00ccccc00cccccc00f0cccc0000cccccccccccc
# </SPRITES>

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
# 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
# </PALETTE>

