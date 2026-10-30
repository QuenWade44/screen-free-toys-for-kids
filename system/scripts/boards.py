import json
# Final board names (must match the 'Pinterest board' column in the bulk CSV exactly).
BOARDS = [
 dict(key="routine", name="Kids Routine Charts & Chore Charts", slug="kids-routine-charts", cover="Routine &amp; Chore Charts", sub="Mornings, bedtime &amp; chores by age", icon="routine", accent="#FFC24B", bg="#FFE9B8",
      desc="Morning routine charts, bedtime routine charts and chore charts for kids by age, picked by a Ph.D. school psychologist. Magnetic routine charts, ok-to-wake clocks, summer schedules and back to school routines that end the morning rush and bedtime battles. Contains affiliate links."),
 dict(key="timer", name="Visual Timers & Visual Schedules for Kids", slug="visual-timers-schedules", cover="Visual Timers &amp; Schedules", sub="Easier transitions, fewer fights", icon="timer", accent="#FF7A59", bg="#FFD9CC",
      desc="The best visual timers for kids, visual schedules, first-then boards, homework stations and wobble cushions. A school psychologist's picks for smoother transitions, better focus and fewer fights over time. Contains affiliate links."),
 dict(key="sensory", name="Sensory Bin Ideas & Sensory Toys", slug="sensory-bin-ideas", cover="Sensory Bin Ideas", sub="Toddler &amp; preschool sensory play", icon="sensory", accent="#2BB3A3", bg="#CDEFEA",
      desc="Sensory bin ideas for toddlers and preschoolers: winter, fall and Halloween sensory bins, sensory bin fillers, kinetic sand ideas, water tables and the sensory toys that keep kids busy. Contains affiliate links."),
 dict(key="screenfree", name="Screen-Free Activities & Toys for Kids", slug="screen-free-activities", cover="Screen-Free Activities", sub="Toys that beat the tablet", icon="screenfree", accent="#FF7A59", bg="#E3DAF6",
      desc="Screen-free activities for kids indoors and screen-free toys parents love: quiet time boxes, rainy day activities, magnetic tiles, pretend play kitchens, Yoto vs Toniebox and no phone summer ideas. Contains affiliate links."),
 dict(key="calm", name="Calm Down Corner & Calming Toys for Kids", slug="calm-down-corner", cover="Calm Down Corner", sub="Tools for big feelings", icon="calm", accent="#7DB9E8", bg="#D6E9F8",
      desc="Calm down corner ideas for home, calm down kits, feelings charts, fidget toys, reward charts and positive discipline tools for kids, chosen by a school psychologist to help with big feelings and meltdowns. Contains affiliate links."),
 dict(key="active", name="Indoor Play Gym & Playroom Ideas", slug="indoor-play-gym", cover="Indoor Play &amp; Playrooms", sub="Burn energy indoors", icon="active", accent="#7DB9E8", bg="#FFE0D2",
      desc="Indoor jungle gym playroom ideas, kids play couch (Nugget) builds, balance boards, indoor swings and basement playroom ideas to help kids burn energy on cold and rainy days. Contains affiliate links."),
 dict(key="gifts", name="Screen-Free Gifts for Kids by Age", slug="screen-free-gifts", cover="Screen-Free Gifts by Age", sub="Gifts kids actually play with", icon="gifts", accent="#FF7A59", bg="#FFE9B8",
      desc="Screen-free gifts for kids by age: gift ideas for 3 year olds, 5 year olds and 7 year olds, stocking stuffers for kids 3-5, Easter basket ideas with no candy and art supply gifts. Picked by a school psychologist. Contains affiliate links."),
 dict(key="travel", name="Road Trip & Camping Essentials for Kids", slug="road-trip-essentials", cover="Road Trip &amp; Camping", sub="Screen-free travel with kids", icon="travel", accent="#2BB3A3", bg="#D3EEE0",
      desc="Road trip with kids essentials, screen-free road trip activities for kids 3-5, kids travel trays, backseat organizers and kids camping essentials for calm family travel. Contains affiliate links."),
 dict(key="montessori", name="Montessori Toys & Life Skills for Kids", slug="montessori-life-skills", cover="Montessori &amp; Life&nbsp;Skills", sub="Toys that build real skills", icon="montessori", accent="#8CC7A1", bg="#E6F2DA",
      desc="Montessori toys for toddlers 2-3, busy boards, learning towers, kid-safe knife sets, bento lunch boxes and life skills for kids by age. Toys and tools that build independence. Contains affiliate links."),
 dict(key="outdoor", name="Outdoor Toys & Nature Kits for Kids", slug="outdoor-toys-nature", cover="Outdoor Toys &amp; Nature", sub="Get kids outside", icon="outdoor", accent="#8CC7A1", bg="#DDEFD0",
      desc="Outdoor toys for kids 4-8, kids gardening kits, bug catcher kits, kids binoculars and backyard games that get kids off screens and outside. Contains affiliate links."),
]
for b in BOARDS:
    assert len(b["name"]) <= 50 and len(b["desc"]) <= 500, b["name"]
json.dump(BOARDS, open("/home/claude/assets_build/boards.json", "w"), indent=1)
print("ok")
