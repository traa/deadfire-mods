18 magic items that give bonuses which scale with character skills (athletics, alchemy, etc.).  They can be bought at Iolflr's Raiments in Neketaka and there is a small chance (~1%) to find them in shipwrecks, burial sites, and similar "searchable" locations on the world map.

Most of these items can eventually become overpowered, and therefore have a high purchase price.  Others have some balancing negative aspects.  Over time I've tried to tone them down but it's enticing to have some items fulfill the possibilities of top-tier items powered by your character's persona.

If you want to change their item cost, edit the item's gamedatabundle (using Notepad++ or Visual Studio Code, then format for JSON) and reduce the Cost value in the ItemMod section.  You can tweak the items easily this way via the StatusEffects sections also.

Even if other mods add items to Iolfr's Raiments, this mod will work.


Item Stats
-----------------------------
cape - Cape of Good Hope - +0.5% chance per skill in Streetwise to resist any hostile attack, -3 class resources at the start of combat
cape - Muleta i Brega
    - +0.5% chance per skill in Athletics to convert hits to grazes and grazes to misses for any weapon attack
    - +1% chance per skill in Bluff to convert hits to grazes and grazes to misses for any non-spell ability
cape - Starlight Cover - +1% chance per skill in Metaphysics to reflect any hostile spell
boots - Boots of Alacrity - +0.5% attack speed per Athletics skill, +25% movement speed, +1% per Athletics skill, +25 Disengagement Deflection
boots - The Demolitionist's Boots - +5% area of effect per skill in Explosives for Fire, Electricity, Frost, and Acid abilities, Reflex +8, Fortitute -8
boots - Boots of Gorundeia - +0.5% of hits converted to crits per Insight skill
hands - Henosis - +3% duration to all hostile and beneficial status effects received per skill in Metaphysics
hands - The Mechanic's Lein - +0.2 Penetration per skill in Mechanics, -0.5 Accuracy per skill in Mechanics
hands - Hands of Sleight - +0.1 Deflection per skill in Sleight of Hand when grazed by melee weapons, stacking up to 20 times for 20 seconds each stack
head - The Ghetto Hood - Immune to Flanking, +1% chance to reflect melee weapons per Streetwise skill when 3 or more enemies are within a 4m radius
head - Helm of History - +0.4 Power Levels per History skill level for the first (30+int%) seconds of combat, -0.2 Power levels per History skill level after (60+int%) seconds
head - The Journeyman's Bluff - +0.25 Accuracy per skill in Bluff, -1 Perception per skill in Diplomacy
head - Kain's Presence - +0.3% damage reduction per skill in intimidate for each 10% Health above 50% Health (up to 5x)
neck - Prize of the Athlon - +1% weapon attack speed per Athletics skill level
neck - Wizard's Lace - +2% spell damage per skill in Arcana, -1% Recovery time with spell attacks per skill in Arcana
ring - Quozic's Ring - +1% damage per Alchemy skill level to Fire, Electricity, Frost, and Acid attacks
ring - The Unnerv Ring - -0.5 Will per Diplomacy skill level, applied to enemies in a (5m+int%) radius
waist - Pious Comfort - 4% damage reduction + 0.5% per skill in religion when less than 50%/30%/10% health


Mod Requirements/Conflicts
-----------------------------
The Deck of Many Things DLC is required for the Starlight Cover item.
This mod was not made for turn-based mode and will not show information properly in that mode.
This mod would conflict if you you have a mod that overwrites the gsd_re_location sections of the globalscripts, which is what determines which items you get when searching places on the worldmap.  Even if other mods add items to Iolfr's Raiments, this mod will work.
Uses text-strings in the range of:
305149951 - 30515XXXX
400000000 - 410000000

Prior versions of the items in your game will be unchanged.  Merchants should refresh to newer versions after 24 hours of resting.

Do not delete this mod (to uninstall it) without removing the items from your character and selling them to a merchant, then waiting for three days.



If you want to give yourself the items, press the ` key and type:
1. iroll20s
(this will disable achievements and enable cheating)
2. giveitem <insert debugname here>


The debug name and guids of the items are:
-------------------------------------------------------------                           
back_capeofgoodhope                     40f74cf0-8bed-485f-a62a-e78f4b0b3ecc
back_muleta                             d370cc5f-962f-4d70-a067-0c26b917b4b8
back_starlight                          1b89b023-32ff-41d3-a2b6-ce9e81b55ab1
boots_alacrity                          a82e5eec-b1aa-4bf1-9ddf-b81f2fd9d742
boots_demolitionist                     64510990-133d-4823-85ee-650bf2d4a71b
boots_gorundeia                         7dfed1f4-8354-479c-81bd-18f543f80c6b
hands_henosis                           31ee487a-4ef8-4c21-b24c-13e0e5f091af
hands_mechanics                         b4fc873a-c57b-4ec3-8249-0151b057fbc8
hands_sleight                           72e3962c-56ae-4f58-bfd4-23336778484c
head_ghetto                             1a8b2ebe-d2f6-442e-87d7-4a78745c024a
head_history                            7ec630bb-41bd-448e-be6e-fb4045f5df5d
head_journeyman                         94ae22d6-5966-4c72-a3d5-ec90a1e66786
head_kain                               286fe99b-0b0e-4737-a804-211ddb33fd1f
neck_athlon                             f25fe257-6824-4633-9016-6336baf81eab
neck_wizard                             e5e5a73d-b1ca-4d64-9ba9-2e37f01a5869
ring_quozics                            154afcae-386c-4cfc-a357-b6e2eb010f51
ring_unnervring                         acd40591-8929-4905-b2cb-a6c282220a69
waist_piouscomfort                      4c2669fc-dc43-41e2-8d57-1310e4b6559c


Changelog
-------------
v1.05
Fixed the random chance to find the items in ruins and shipwrecks.
New icon for henosis

v1.04
Fixed Journeyman's Bluff to do -1 perception per Diplomacy instead of 1 - 0.5x
Journeyman's Bluff gives +0.25 Accuracy per Bluff skill, not Perception
Pious Comfort initial damage resistance 2%-->4%, 1% resistance per Religion per health tier --> 0.5%
Boots of Alacrity no longer gives immunity to dexterity afflictions
Ghetto Hood immunity to flanking --> +1 enemies needed to be flanked
Quozic's effect halved
Kain's Presence 0.4% damage reduction --> 0.3%
Starlight Cover has the Cape of the Falling Star model
Ghetto Hood has clean hood icon and model so not to confuse with another existing unique item
Kain's Presence uses horned helm model and icon so not to confuse with another existing unique item
Kain's Presence typo fixed, 0.3% not 0.03%
Helm of History status effect description fixed to automatically display correctly
Demolitionist's Boots has more accurate description relating to keywords rather than damage types
Demolitionist's Boots description to have a bigger backstory
Cape of Good Hope status description clarified to any 'hostile' attack
Quozic's ring icon changed to gui/icons/items/jewelry/ring_copper_01_l.png
Quozic's Ring has more accurate description relating to keywords rather than damage types
Unnerv ring icon changed to gui/icons/items/jewelry/ring_folly_l.png
New icons for:
Boots of alacrity
Demolitionist's Boots
Boots of Gorundeia
Mechanic's Lein
Hand of Sleight
Prize of the Athlon
Hand of Sleight cost increased
Renamed Pious Comfort's Moment of Truth to Moment of Judging to not confuse with another mod's ability named that
Italicized some of the lame poetry to make it stylishly lame instead
Changed the Journeyman's bluff lyrics to be less lame
removed the unnecessary ability explanations at the bottom of Unnerv Ring's 'Assuage' and Ghetto Hood's 'Done That'
Added my custom Movespeed Fast keyword from my Keywords Everywhere Mod to Boots of Alacrity

v1.03
Henosis changed to only have the Oneness ability, and fixed to not drastically reduce beneficial effect duration
Boots of Gorundeia decreased insight-based hits to crits +1%-->0.5%
Increased price of Boots of Gorundeia
Unnerv Ring diplomacy-based Will aura reduced from -1 --> -0.5
Increased price of Unnerv Ring
Wizard's Lace arcana-based spell damage (+2%) now also has +1% Recovery Time with spell attacks
Increased price of Wizard's Lace

v1.02
Increased price of Boots of Gorundeia
Increased price of ghetto hood
Increased price of Starlight Cover
Increased price of Muleta i' Brega, decreased athletics-based hit to miss +1%-->+0.5%
Increased price of Cape of Good Hope, increased -1 class resource --> -3
Increased price of Helm of History
Increased price of Boots of Alacrity, action speed +1%-->+0.5% per athletics
Increased price of Prize of the Athlon, weapon attack speed +2% ---> +1% per athletics
