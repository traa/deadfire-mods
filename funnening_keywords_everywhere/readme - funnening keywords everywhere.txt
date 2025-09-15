Since the dawn of Deadfire, there has been a noticeable lack of abilities that only apply for certain afflictions and status effects such as being stunned.  This is because the exported code largely does not support it, until now.  This mod adds keywords to the some of the most popular afflictions and some attack types to enable future coding for abilities that do +50% damage to stunned opponents, as an example.  I created this so that I could make the mods I want to make, but this can and should be used as a code base for future modders, so that new abilities enable the same specificity.

This will be updated as I create more keywords

--------------------------------------

The Keywords added are:

status_effect_keyword_enfeebled		93d0ed78-ef3a-4e01-97e0-bbd3610dd9c9

status_effect_keyword_paralyzed		682606a5-9d1a-47ba-9422-66173fbaadc3

status_effect_keyword_petrified		b355ae14-8407-494c-b559-30e1176a2255

status_effect_keyword_stunned		07b738c8-faa6-4aaa-91f1-5874b3c15d6a

status_effect_keyword_charmed		8668960f-c20a-458e-a6ee-7d72d7641a8f

status_effect_keyword_dominated		74557bcc-81ed-42f6-975f-d8745c36cf4a

status_effect_keyword_confused		524b2cfe-2e72-48bf-8dda-6d6767fb5b7a

status_effect_keyword_blinded		67f5ed46-22a1-40d9-b2c5-71cb8165217d

status_effect_keyword_frightened	25543574-736f-4ce7-a62e-1b599739f835

status_effect_keyword_terrified		cb6304a6-a00f-4662-aab8-27b974423b7f

status_effect_keyword_staggered		c483f797-b12d-4104-8d13-c24a6ab04bd6

status_effect_keyword_dazed		6729e2fe-4a6c-4742-9082-0c1444cd3a34

status_effect_keyword_hobbled		cc69f4c6-9e7e-4167-82dc-6749f398e351

status_effect_keyword_shaken		4e572861-b426-4469-936f-1496cb3db4df

status_effect_keyword_distracted	843eff52-ff8a-493f-afb5-9a0d6daa7f79

status_effect_keyword_disoriented	ceab5546-c77f-4f6c-b8b4-191dae058fb9

status_effect_keyword_immobilized	77134d89-42e6-47ee-8d44-b2f16c57e78f

movespeed_slow_keyword	1ac51cc2-92c2-4675-9194-c39611630b3c	(Status Effects only)

movespeed_fast_keyword	f5cbd28b-c881-4b16-8bef-d2066508303a	(Status Effects only)

jump_keyword	b4ed06e4-f3f9-4386-a936-14cb70d49b73			(Attacks only)

teleport_keyword	eb264954-e9fc-4514-a7fb-57b29576e66c		(Attacks only)

------------------------------------

Added keywords to all afflictions with these status effects, as well as the status effect itself:

Enfeebled_SE_NoHealing
a0f11546-031c-43eb-ab20-c898bc861045

Paralyzed_SE_Paralyzed
e07a73fa-2445-4ea1-b906-1b8437771bb1

Petrified_SE_Shader
8c3f9cb6-1591-4083-847c-20d4560647db

Stunned_SE_Stunned
45537b43-aa00-4ee7-8f70-84f60a6b1d65

Charmed_SE_TakeControl
cf852c4e-1e12-460b-9aa3-89449da6945d

Dominated_SE_TakeControl
6eee8a79-c54b-4366-9335-e2f04fc665b4

Confused_SE_AttacksTargetAll
03d84c0b-9bf0-4d5b-83d1-f31c5ee7486a

Blinded_SE_DisableGazeAbilities
1dbeff21-d432-477a-a946-86a3127bf262

Frightened_SE_DisableHostileAbilities
05d2691a-1be9-49dd-bbeb-f40f39b8b909

Terrified_SE_Terrified
b7079b28-c54a-4bac-be4d-de92ac5f5b1c

Staggered_SE_CannotEngage
94019d5f-9b30-4856-8927-05eafda2e398

Dazed_SE_PenetrationDebuff
1a271eb6-d086-47a5-8b88-e471e2dec92c

Hobbled_SE_ForceWalk
499e33c1-7883-4abf-9587-340c5b4d5160

Shaken_SE_PowerLevelDebuff
570ab08d-36b9-467f-9235-b7d7e875b404

Distracted_SE_PerceptionDebuff
2207bf6c-e707-4c8e-92bf-886f02d61d9d

Disoriented_SE_RecoveryDebuff
8d3a8e85-2ba2-4759-b9f0-f62739ef67f4

Immobilized_SE_CannotMove
acb85834-6da9-4f01-a637-77e33d8bca02

------------------------------------
Added Keywords to the following inspiration status effects

INS_Nimble_SE_Movement
82f1204e-98cc-4f31-bb69-3ff9b74f4010
(movespeed_fast_keyword added)

INS_Swift_SE_Movement
7647f7a3-ad4d-46eb-a9e5-dee6d9252455
(movespeed_fast_keyword added)

------------------------------------

Possible keywords to include in the future

	- Keywords for other statuses, such as Nature, Undead, etc.
	- Poison damage, DoT
	- Immunity to anything keyword
	- Immunity specific keywords
	- Concentration keyword
	- AttackResistance keyword
	- TeleportAttack, Ray
	- Lifesteal, Attribute steal, Draining
	- Temporal, Interval
	- Hastening, slowing
	- Stride
- Keywords for each affliction/inspiration
- Keyword for each level of the affliction/inspiration
- A keyword that represents all afflictions


------------------------------------

For the novice, it is important to understand that this mod will overwrite the affliction, not the status effect or ability.  If another mod edits an ability, but doesn't change its underlying affliction, then there is no conflict. I do add keywords to the base status effects listed at the top, but this isn't necessary and can be overwritten by other mods. The only important part of this mod is the overwriting of the afflictions to add keywords.

The grouping of how separate code is linked can be summarized as:
Items-->Abilities-->Affliction Status Effects-->Status Effects

So as you can see, another mod may claim to change an ability's affliction, but if it only adds keywords to the ability, then there is no conflict.  For afflictions, it is unlikely that the status effect itself is changed, so if a mod changes an affliction, it's probably conflicting with this mod. Most abilities don't use afflictions and just have status effects, and a lot of modders make abilities that just add status effects without even packaging them into an affliction.

Paralyze is just like Petrified but here I only added the keyword for each on their separate effects, so there is no overlap and anything that affects both must use both keywords.

ALL of the keywords can be found in the beginning of the status effects file.
If you want to prevent anything being overwritten, remove the entire file (attacks file, etc.) or remove the bracketed area for a piece of code and the game will work even if that section of code wasn't removed completely (the error will result in no override from that part of my mod to the game).


The Following Status Effects were skipped because:
---------------------
Ryrmgrand's Wrath - didn't have other keywords attached to them, indicating it was used as special status effects
Unbroken - movement slow is minor and for dramatics only
Form of Helpless Beast - movement slow is for dramatics only
Delemgan Racial - movement is normalizing not altering
Pet_Bird_Orbit_SE_Stride - movement speed bonus is minor and constant
Pet_BACKER_PartyAbility_SE_Stride - movement speed bonus is minor and constant
Shorewalker_Sandals_Certain_Stride_SE_MovementSpeed - movement speed bonus is minor and constant
Winged_step_SE_Stride - movement speed bonus is minor and constant
Hunters_Stride_SE_Stride - movement speed bonus is minor and constant
Blink of an Eye - movement speed is related to slowing time itself

Installation
----------------------
Place this ABOVE any of my Augmented mods and mods that include afflictions, or else it will overwrite them.


Changelog
----------------------
1.2
Added these keywords:
Jump - added to attacks only (my other mods add to abilities and attacks)
Teleport - added to attacks only (my other mods add to abilities and attacks)
Speed Slow (not added to anything yet)
Speed Fast (not added to anything yet)
(Haven't changed expansion abilities for this)
