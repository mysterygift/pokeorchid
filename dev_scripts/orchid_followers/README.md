# Orchid follower sprites

192x32 sheets (6 frames of 32x32: down A/B, up A/B, left A/B), drawn in each species' battle palette;
overworld_normal.pal / overworld_shiny.pal are copies of normal.pal / shiny.pal. Needs Pillow.

- Pinguin: Piplup's follower body + walk cycle recoloured, with a smaller hand-drawn head
  `python pinguin_retex.py graphics/pokemon/piplup/overworld.png graphics/pokemon/pinguin/normal.pal graphics/pokemon/pinguin/overworld.png`
- Iyepure / Torpesquid: painted fills, dark outline added automatically
  `python gen.py x dev_scripts/orchid_followers/iyepure.py graphics/pokemon/iyepure/normal.pal graphics/pokemon/iyepure/overworld.png 9`
  `python gen.py x dev_scripts/orchid_followers/torpesquid.py graphics/pokemon/torpesquid/normal.pal graphics/pokemon/torpesquid/overworld.png 10`
  (last arg = x offset of the art inside each 32px frame; art is bottom-aligned to row 29)
