"""All Holon NPC / sign / trainer text (install_holon.py). Poryscript format() wraps the lines; \\p = new box."""

# Placeholder trainer ids (include/constants/holon.h aliases them to existing vanilla trainers until the
# trainers stream's Holon Researcher trainers are merged).
TRAINER_IDS = {"c1": "TODO_TRAINER_HOLON_RESEARCHER_1", "c2": "TODO_TRAINER_HOLON_RESEARCHER_2",
               "l1": "TODO_TRAINER_HOLON_RESEARCHER_3", "l2": "TODO_TRAINER_HOLON_RESEARCHER_4",
               "t1": "TODO_TRAINER_HOLON_RESEARCHER_5", "t2": "TODO_TRAINER_HOLON_RESEARCHER_6"}

TRAINERS = {
    "c1": dict(intro="These ruins sit on a Power Spot. You're standing right on my sensor line!",
               defeat="My readings... scrambled completely.",
               post="The old track here carried carved stone down to the lake, long before our tower was built."),
    "c2": dict(intro="Delta Species gather wherever the Power Spot energy runs strong. Let me show you mine!",
               defeat="Fascinating. Your Pokémon adapt so quickly.",
               post="The energy changes a Pokémon's type, but never its heart. Or so we hope."),
    "l1": dict(intro="The marsh readings are off the charts! Don't trample my instruments!",
               defeat="I'll have to recalibrate everything...",
               post="The pillars channel the lake's energy into that sphere. We just collect what spills over."),
    "l2": dict(intro="A visitor? This part of the shore is closed for research!",
               defeat="Hmph. Fine, look around. Just don't touch the pillars.",
               post="The domes by the shore? Sealed. We've never found a way in, and the elders won't say."),
    "t1": dict(intro="Authorised staff only past this point!",
               defeat="I suppose you've earned a look.",
               post="Every machine on this floor stores energy drawn from the Power Spot."),
    "t2": dict(intro="Want to see what a Delta Pokémon can do on a full charge?",
               defeat="Overloaded... and I lost anyway.",
               post="Our head of research says the drain is temporary. The farmers don't believe her."),
}

SAILOR_PLACEHOLDER = ("Ahoy! Whenever you're ready to head home, just say the word.\\p"
                      "(Placeholder: the voyage return menu is added by the core voyage stream.)")

COAST = {
    "lass": "Folks call this the Mirage Forest. The trails twist so much they seem to move. "
            "Keep to the path east and you'll reach Holon Village.",
    "sign": "Mirage Forest\\nHolon Village: follow the path east.",
}

VILLAGE = {
    # the four "drained flora" lines (out/batch4/NOTES.md)
    "farmer_nw": "Third season the berries won't set. Leaves come up grey as ash, closer to that tower they get.",
    "farmer_se": "My gran said this soil grew anything. Now look at it. Power Spot, they call it... more like a drain.",
    "lass": "The grass round the lake used to be so green. Now it's all washed out near those stone pillars.",
    "walkway": "A seasonal fluctuation, nothing more. The readings from the Power Spot are perfectly within tolerance.",
    "mentor": "That old house belonged to Holon's stone carvers. When the tower went up they left, "
              "and nobody's lived there since.",
    "farmer_n": "Farming's hard work, but nobody in Holon ever went hungry. Well... nobody used to.",
    "centre_visitor": "I'm only here to study the Delta Species. Your Pokémon Center works just like ours back home!",
    "sign_town": "Holon Village\\nWelcome, travellers from across the sea.",
    "sign_lake": "South: Holon Lake\\nNorth: Holon Village",
    "sign_farm": "Holon Farms\\nPlease leave the berry trees to the farmers.",
    "sign_tower": "Holon Research Tower\\nStudying the Power Spots and the Delta Species.",
}

HOUSES = [  # (graphics, text) for House1..7
    ("OBJ_EVENT_GFX_OLD_WOMAN", "My husband worked the fields for fifty years. These days he just sits by the window "
                                "and watches that tower."),
    ("OBJ_EVENT_GFX_BOY_1", "Mum says the researchers came from far away. They've got computers bigger than our house!"),
    ("OBJ_EVENT_GFX_MAN_3", "Holon's weather used to be gentle. Now storms roll in off the lake with no warning at all."),
    ("OBJ_EVENT_GFX_WOMAN_3", "You came by boat? That old sailor must trust you. He doesn't bring just anyone to Holon."),
    ("OBJ_EVENT_GFX_FISHERMAN", "The lake fish have changed. Half my catch looks like it's been dipped in metal!"),
    ("OBJ_EVENT_GFX_GIRL_3", "I saw a Pikachu that wasn't Electric-type! Grandpa says they're called Delta Species."),
    ("OBJ_EVENT_GFX_OLD_MAN", "Long ago, folk carved diamonds into stones all over Holon. Nobody remembers why any more."),
]

RUINS = {
    "lore": "There's a scrap of paper tucked under a loose board...\\p"
            "'The Power Spots must never be tapped. What the land gives freely, it can take back.'",
    "shelf": "Dusty old books about stone carving. The pages have gone brittle.",
}

TOWER1 = {
    "reception": "Welcome to the Holon Research Tower. Visitors are welcome on the ground floor.",
    "r1": "We study Holon's Power Spots and the Delta Species that appear around them.",
    "r2": "Our readings show the land's energy falling every season. We're... looking into it.",
    "visitor": "I came to ask why my field's gone grey. They told me to fill in a form.",
    "bed": "A neatly made bed for researchers on the night shift.",
}

TOWER2 = {
    "npc": "Those round machines store the energy we draw from the Power Spot. Please don't touch them!",
    "machine": "A round machine humming with stored energy.",
    "offer": "I'm the head of research here. You've come a long way to see Holon.\\p"
             "This Eevee was born right beside the Power Spot. Its type shifted as it grew. "
             "A Delta Species!\\pWe can't give it the attention it deserves. Would you take care of it?",
    "declined": "I see. If you change your mind, I'll be here.",
    "after": "Delta Species are proof of how much power sleeps under Holon. Raise that Eevee well.",
}

LAKE = {
    "sphere": "A great stone sphere rests in the plinth's socket. Diamonds are carved all over it. It feels cold.",
    "sphere_glow": "The stone sphere is glowing with a soft blue light. The air around it hums.",
    "cynthia_placeholder": "...\\p(Placeholder: Cynthia's battle script is added by the trainers stream.)",
    "gyarados_ran": "The Gyarados dived back under the surface...",
    "mentor": "Those stone domes by the shore have been sealed since before my grandmother's time. "
              "Whatever's inside is meant to stay there.",
    "sign": "Holon Lake\\nPlease do not disturb the stone pillars.",
    "dome": "The doorway is sealed with a carved stone slab. A diamond is cut into its face.",
    "pillar": "A tall carved pillar rising out of the lake. It hums faintly.",
}
