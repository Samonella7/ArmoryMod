This is an add-on for The Battle For Wesnoth (www.wesnoth.org). It is currently only availabe on the development branch, 1.13

Please comment at https://forums.wesnoth.org/viewtopic.php?f=15&p=617608

For lack of a better way to describe this mod, here is the description that's visible on the add-on server:

Sort through your units' weapons, re-distributing them freely! Arm your swordsman with a javelin, or capture an enemy's battle-axe so your dark adept can defend herself! A complete weapon inventory system that works with all default factions, and many add-on units as well. Works in both multiplayer and campaigns--just right-click a unit to get started!


Below is a brief outline of how this add-on's code is structured:

Unit's acutal attacks are frequently recalculated based off their "weapons" and "skills." 
Skills are mostly determined by their original unit type. When the unit is first created, it's "Weapons" also match that,
but the player can trade, capture or destroy weapons freely. 
The actual attack is a weighted average of the "Weapons" and any matching "Skill." The weight depends on the type of weapon.
If the unit has no skill matching a weapon it captured, the same average will be performed with a 0-0 skill.

Whenever the weapons might have changed, the unit is essentially rebuild, based off it's Skills and Weapons to make sure it's 
Attacks are up to date. Data for the unit's Skills and Weapons are stored in the unit variables, in a container called "armorymod"
(So if the whole unit is stored in $unit|, the weapons would be in the array: $unit.variables.armorymod.weapons|)

Finally, before diving into the code structure, here is an important note about variable names:
Since every file/event usually needs the same things (a variable to temporarily store a unit or weapons for example)
it makes sense to have a naming convention; each event will use it's own container variable, so that inside of it it can
follow the same conventions as other files.
So for example, the event "armorymod_update_unit_vars" will frequently use $armorymod.update_unit_vars.unit.variables.armorymod.weapons[1].type|
Since that name is ugly and long, I use macros in each file; so now all files wil frequenly use ${WORKSPACE}unit{DOT}weapons[1].type|

All the actual code is in the directory utils/, where there are 9 files:
1) macros.cfg
	This contains basic tools that are used by all other files; things like defining what it means to "drop" a weapon,
	in terms of the underlying WML variables.
2) tools.cfg
	This file is just like macros.cfg, but it is events instead of macros. Both are just tools that the main events use.
3) variable_preparation.cfg
	This file defines all the weapon types (for example, by listing all attack names that correspond to a "sword" attack)
	It also lists specific exceptions to normal rules (for example, normally units can only use "weapons" if their unit type
	gives them one, so wolves (whose only attack is "fangs") can't use them, but a Wolf Rider, who has the same attack, can)
	This file is significant because it is the only one that should need to change in order to accomidate new unit types.
4) main_events.cfg
	This file contains all the events that are triggered from mainline Wesnoth. It does things like
	opening the inventory menu after units' deaths, as well as setting up all the necessary variables pre-scenario.
	It goes without saying that this file relies heavily on all the others.
5) update_unit_vars
	This file contains a single event, armorymod_update_unti_vars
	This is the first step to "rebuilding the unit" as described earier. It doesn't change the unit's attacks; 
	rather, it changes the "skill" and "weapon" variables to match the attacks. This is mainly important for when a unit
	is first created; since the entire notion of "sills" and "weapons" is made up by me, the default unit doesn't have any of
	these variables, and I must create them based off the unit's original attacks.
	It is also possible that other add-ons or campaigns will give the unit new attacks mid-scenario, which is why this event
	is frequently called.
6) open_armory_menu
	this file again only includes one event; It should be triggered after armorymod_update_unti_vars.
	The idea is that once we are sure the variables are up-to-date, then we can allow the player to interact with the
	weapons that these variables represent.
	So this event provides an interface for doing so, and edits the variables as appropriate.
7) rebuild_unit
	Once the player has finished playing with the variables, we should rebuild the unit so its attacks represent its new state.
	The event in this file does just that; it removes all old attacks, and replaces them based off the current "skill" and "weapon" variables.
	It relies heavily on:
8) weapon_to_attack
	Since a huge amount of the logic in the previous event is just about parsing the weapon and skill data, comparing and combining matches, etc,
	that logic was all pulled into this separate file. It is not a separate event, just Actoin WML that is dumped directly into the previous file's one.
9) animations.cfg
	This file is pretty isolated from the others; it just contains simple "animations" for all the attacks units can get that they wouldn't normally have.
	I say "animations" but really they're just sound effects: obviously I'm not making sprites for every possible unit with every possible weapon type.
	The filters are set up so that units will still use their own animations when possible.
	
	