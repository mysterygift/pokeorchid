"""Trainer battle intro mock at true GBA size (240x160): Orchid battle floor + the new front pic at
the vanilla opponent spot + the Orchid message tray with the ROM font, via dev_scripts/orchid_ui.

usage: battle_mock.py FRONT_PNG ENV "CLASS NAME" OUT_PNG
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UI = os.path.abspath(os.path.join(HERE, '..', 'orchid_ui'))
sys.path = [UI] + [p for p in sys.path if os.path.abspath(p or '.') != HERE]

from PIL import Image  # noqa: E402
import kit_ext as K  # noqa: E402  (orchid_ui kit)
import battle_ext as BX  # noqa: E402
import mock_battle as M  # noqa: E402


def mock(front_png, env, who, out_png):
    def intro_scene(env=env, trainer=None, player_back='brendan', trainer_dx=0):
        out = BX.environment(env)
        K.place(out, K.sprite_rgba(front_png), BX.ENEMY_C[0], BX.ENEMY_C[1])
        back = K.sprite_rgba(K.G('trainers', 'back_pics', player_back + '.png'), 0, 64)
        K.place(out, back, 80, 80)
        return out
    M.intro_scene = intro_scene
    img = M.render(mode='msg', msg=f'{who}\nwould like to battle!', intro=True, env=env)
    img.save(out_png)
    return out_png


if __name__ == '__main__':
    print(mock(*sys.argv[1:5]))
