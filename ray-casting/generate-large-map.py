# Map generator for level.txt — "The Ancient Citadel"
# 200x200 grid. Zones: NW=defensive ward, NE=cathedral, SW=labyrinth, SE=market, Centre=citadel
# Run directly to regenerate level.txt.

SIZE = 200
m = [[0]*SIZE for _ in range(SIZE)]

def fill(r1, c1, r2, c2):
    for r in range(max(0, r1), min(SIZE, r2 + 1)):
        for c in range(max(0, c1), min(SIZE, c2 + 1)):
            m[r][c] = 1

def clear(r1, c1, r2, c2):
    for r in range(max(0, r1), min(SIZE, r2 + 1)):
        for c in range(max(0, c1), min(SIZE, c2 + 1)):
            m[r][c] = 0

def hwall(r, c1, c2, gap=None):
    for c in range(max(0, c1), min(SIZE, c2 + 1)):
        m[r][c] = 1
    if gap:
        for c in range(gap[0], gap[1] + 1):
            m[r][c] = 0

def vwall(c, r1, r2, gap=None):
    for r in range(max(0, r1), min(SIZE, r2 + 1)):
        m[r][c] = 1
    if gap:
        for r in range(gap[0], gap[1] + 1):
            m[r][c] = 0

def room(r1, c1, r2, c2, door_side, door_pos):
    """Hollow rectangle with one doorway (2 tiles wide)."""
    fill(r1, c1, r2, c2)
    clear(r1+1, c1+1, r2-1, c2-1)
    dp = door_pos
    if door_side == 'N': clear(r1, dp, r1, dp+1)
    if door_side == 'S': clear(r2, dp, r2, dp+1)
    if door_side == 'E': clear(dp, c2, dp+1, c2)
    if door_side == 'W': clear(dp, c1, dp+1, c1)

# ── Outer boundary ────────────────────────────────────────────────────────
fill(0, 0, 0, 199)
fill(199, 0, 199, 199)
fill(0, 0, 199, 0)
fill(0, 199, 199, 199)

# ── CONNECTOR BOULEVARDS — wide cross through the map ────────────────────
clear(78, 1, 82, 198)
clear(118, 1, 122, 198)
clear(1, 78, 198, 82)
clear(1, 118, 198, 122)

# ── CENTRE: The Citadel (rows 83-117, cols 83-117) ───────────────────────
# Thick outer wall with solid corner towers and 4 gatehouses
fill(83, 83, 117, 117)
clear(86, 86, 114, 114)          # hollow interior
fill(83, 83, 92, 92)             # NW tower
fill(83, 108, 92, 117)           # NE tower
fill(108, 83, 117, 92)           # SW tower
fill(108, 108, 117, 117)         # SE tower
clear(83, 97, 86, 103)           # N gate
clear(114, 97, 117, 103)         # S gate
clear(97, 83, 103, 86)           # W gate
clear(97, 114, 103, 117)         # E gate
# Inner ring wall — creates a ring corridor between two walls
fill(91, 91, 109, 109)
clear(93, 93, 107, 107)
clear(91, 98, 91, 102)           # inner N gate
clear(109, 98, 109, 102)         # inner S gate
clear(98, 91, 102, 91)           # inner W gate
clear(98, 109, 102, 109)         # inner E gate
# Central keep — solid with south-only entrance
fill(96, 96, 104, 104)
clear(98, 98, 102, 102)
clear(104, 99, 104, 101)

# ── NW: The Defensive Ward (rows 2-77, cols 2-77) ────────────────────────
# Player starts at tile (18,18). Curtain walls, bastions, inner ward rooms.

# North curtain wall with gateway and flanking bastions
hwall(8, 3, 55, gap=(22, 27))
fill(3, 3, 9, 9)                 # NW bastion
fill(3, 49, 9, 55)               # NE bastion

# East curtain wall with gateway
vwall(55, 3, 46, gap=(20, 25))
fill(39, 49, 45, 55)             # SE bastion

# Inner ward dividing wall
hwall(32, 3, 52, gap=(24, 29))
fill(28, 48, 34, 54)             # gatehouse tower

# Buildings in the inner ward
room(48, 4,  60, 17, 'N', 9)
room(48, 21, 58, 34, 'N', 26)
room(46, 38, 60, 52, 'N', 43)
clear(60, 42, 60, 45)            # second exit south for connectivity

# Features in the outer ward
fill(14, 32, 20, 38)             # guard tower (solid block)
fill(14, 58, 22, 66)             # armoury
clear(20, 60, 20, 63)            # armoury south door
hwall(12, 38, 68, gap=(47, 50))  # low defensive wall with gap

# Keep player start zone clear
clear(12, 12, 28, 28)

# ── NE: The Cathedral (rows 2-77, cols 123-197) ──────────────────────────
# Long nave with columns, side chapels, apse at north end

fill(3, 123, 77, 197)
clear(5, 125, 77, 195)

# Columns flanking the nave
for r in range(10, 68, 8):
    fill(r, 138, r+2, 139)
    fill(r, 181, r+2, 182)

# Apse at north end
fill(3, 125, 12, 195)
clear(5, 132, 10, 188)
fill(5, 132, 5, 147)             # altar left
fill(5, 173, 5, 188)             # altar right
fill(5, 157, 8, 163)             # central altar

# Side chapels off the aisles
for r in [18, 34, 50]:
    fill(r, 125, r+8, 133)
    clear(r+1, 126, r+7, 132)
    clear(r+3, 133, r+5, 133)
    fill(r, 187, r+8, 195)
    clear(r+1, 188, r+7, 194)
    clear(r+3, 187, r+5, 187)

# Wide south entrance to boulevard
clear(73, 153, 77, 167)

# ── SW: The Labyrinth (rows 123-197, cols 2-77) ──────────────────────────
# Dense winding maze — all gaps 3 tiles wide, one clear route through

hwall(130, 3,  55, gap=(5,  8))
hwall(138, 22, 76, gap=(50, 53))
hwall(146, 3,  58, gap=(30, 33))
hwall(154, 20, 76, gap=(18, 21))
hwall(162, 3,  60, gap=(55, 58))
hwall(170, 18, 76, gap=(10, 13))
hwall(178, 3,  62, gap=(38, 41))
hwall(186, 22, 76, gap=(65, 68))
hwall(194, 3,  70, gap=(25, 28))

vwall(12,  124, 148)
vwall(35,  139, 162)
vwall(55,  124, 140)
vwall(55,  148, 165)
vwall(68,  130, 155)
vwall(25,  155, 178)
vwall(45,  163, 185)
vwall(62,  170, 193)

# ── SE: The Market Forum (rows 123-197, cols 123-197) ────────────────────
# Open forum with colonnaded perimeter and market stall grid

# Colonnaded perimeter — pillars every 6 tiles
for r in range(126, 196, 6):
    fill(r, 123, r+1, 124)
    fill(r, 196, r+1, 197)
for c in range(126, 196, 6):
    fill(123, c, 124, c+1)
    fill(196, c, 197, c+1)

# Market stalls in a grid
for r in range(130, 190, 9):
    for c in range(130, 190, 9):
        fill(r, c, r+2, c+3)

# Wide main avenues clearing through the stalls
clear(123, 157, 197, 163)
clear(157, 123, 163, 197)

# ── Re-enforce outer boundary ─────────────────────────────────────────────
fill(0, 0, 0, 199)
fill(199, 0, 199, 199)
fill(0, 0, 199, 0)
fill(0, 199, 199, 199)

with open('level.txt', 'w') as f:
    for row in m:
        f.write(''.join(str(c) for c in row) + '\n')

print("level.txt written")
