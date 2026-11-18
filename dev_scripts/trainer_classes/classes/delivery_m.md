# RIDER — `delivery_m`
- **Class name:** RIDER (food-delivery cyclist).
- **Bases:** front `cycling_triathlete_m` (pose, helmet, bike kept); OW `youngster` (cap -> helmet).
  `cycling_triathlete_m` OW is 32x32 bike frames, so it is not usable as a walking base.
- **NPC palette:** `npc_blue` (purple 8-A helmet/jersey/box, orange-red B-D trainers + logo).
- **Design:** original "orchid purple" brand (not Grab green / foodpanda pink / Deliveroo teal): purple helmet,
  jersey and square insulated box; black cycling shorts; Poke Ball swapped for a phone.
- **Round 2:** box is now a cube in the rider's 3/4 view, composited *behind* him over the shoulders/back:
  lit forward face (camera-left), top, and the side face toward the viewer carrying the white bowl logo
  (right half stepped 1px up for the face's skew). OW: side frames show the logo on the box side;
  back view shows the plain back face (lid band, no logo).
- **Weak spots:** the box is still a prop past the vanilla outline (by nature); logo is small and reads as a
  white/orange bowl badge rather than crisp detail; youngster body reads young.
- **Open questions:** purple OK as the in-world delivery brand? Want a brand name for later UI?
