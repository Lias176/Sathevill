import Textures
from Animation import Animation

PLAYER_WALK_UP: Animation = Animation(None, [ Textures.PLAYER_WALK_UP_0.surface, Textures.PLAYER_WALK_UP_1.surface ], 250)
PLAYER_WALK_RIGHT: Animation = Animation(None, [ Textures.PLAYER_WALK_RIGHT_0.surface, Textures.PLAYER_WALK_RIGHT_1.surface ], 250)
PLAYER_WALK_DOWN = Animation(None, [ Textures.PLAYER_WALK_DOWN_0.surface, Textures.PLAYER_WALK_DOWN_1.surface ], 250)
PLAYER_WALK_LEFT = Animation(None, [ Textures.PLAYER_WALK_LEFT_0.surface, Textures.PLAYER_WALK_LEFT_1.surface ], 250)