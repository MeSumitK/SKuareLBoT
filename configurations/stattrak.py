import logging
import discord
import datetime
import random
import traceback
import psutil
import os
import json
import sqlite3
import re
#import matplotlib.pyplot as plt


from cogs.utils import checks
from discord.ext import commands
from collections import Counter
from io import BytesIO


dt_format = '%Y-%m-%d %H:%M:%S'
# Yes, I saved all the legendaries like this, sue me
uniques = [
    "Ahn's Heritage",
    "Bisco's Collar",
    "Bisco's Leash",
    "Collateral Damage",
    "Fight for Survival",
    "First Snow",
    "Frozen Trail",
    "Garukhan's Flight",
    "Gruthkul's Pelt",
    "Haemophilia",
    "Inevitability",
    "Martyr of Innocence",
    "Might and Influence",
    "Omen on the Winds",
    "Overwhelming Odds",
    "Ring of Blades",
    "Ryslatha's Coil",
    "Sudden Ignition",
    "The Baron",
    "The Wise Oak",
    "Tidebreaker",
    "Violent Dead",
    "Wildfire",
    "Winter Burial",
    "Abberath's Hooves",
    "Angler's Plait",
    "Arakaali's Fang",
    "Choir of the Storm",
    "Duskdawn",
    "Esh's Mirror",
    "Esh's Visage",
    "Ewar's Mirage",
    "Hand of Thought and Motion",
    "Hand of Wisdom and Action",
    "Kitava's Feast",
    "Light of Lunaris",
    "Lycosidae",
    "Malachai's Vision",
    "Ngamahu's Flame",
    "Perseverance",
    "Presence of Chayula",
    "Primordial Eminence",
    "Primordial Harmony",
    "Primordial Might",
    "Severed in Sleep",
    "Shade of Solaris",
    "Sin's Rebirth",
    "Skin of the Lords",
    "Skin of the Loyal",
    "The Anima Stone",
    "The Anticipation",
    "The Blue Dream",
    "The Blue Nightmare",
    "The Brine Crown",
    "The Formless Flame",
    "The Formless Inferno",
    "The Green Dream",
    "The Green Nightmare",
    "The Halcyon",
    "The Infinite Pursuit",
    "The Pandemonius",
    "The Perfect Form",
    "The Red Dream",
    "The Red Nightmare",
    "The Red Trail",
    "The Snowblind Grace",
    "The Surrender",
    "Tukohama's Fortress",
    "Tulborn",
    "Tulfall",
    "United in Dream",
    "Uul-Netol's Embrace",
    "Uul-Netol's Kiss",
    "Voice of the Storm",
    "Voll's Vision",
    "Xoph's Blood",
    "Xoph's Heart",
    "Xoph's Inception",
    "Xoph's Nurture",
    "Brain Rattler",
    "Cospri's Malice",
    "Dying Sun",
    "Eye of Innocence",
    "Hallowed Ground",
    "Kitava's Thirst",
    "Kondo's Pride",
    "Obscurantis",
    "Praxis",
    "Razor of the Seventh Sun",
    "Shaper's Touch",
    "Slivertongue",
    "Snakepit",
    "Starforge",
    "The Brass Dome",
    "The Putrid Cloister",
    "The Scourge",
    "The Warden's Brand",
    "Unending Hunger",
    "Valyrium",
    "Voidwalker",
    "Witchfire Brew",
    "Amplification Rod",
    "Ascent From Flesh",
    "Ashcaller",
    "Breath of the Council",
    "Cloak of Tawm'r Isley",
    "Coated Shrapnel",
    "Cospri's Will",
    "Cragfall",
    "Death's Door",
    "Death's Opus",
    "Deidbellow",
    "Doomfletch's Prism",
    "Emperor's Mastery",
    "Ezomyte Hold",
    "Grand Spectrum",
    "Grand Spectrum",
    "Grand Spectrum",
    "Grip of the Council",
    "Hiltless",
    "Hinekora's Sight",
    "Hrimburn",
    "Hrimnor's Dirge",
    "Innsbury Edge",
    "Kaltensoul",
    "Kaom's Way",
    "Karui Charge",
    "Kiara's Determination",
    "Kintsugi",
    "Martyr's Crown",
    "Mind of the Council",
    "Ngamahu Tiki",
    "Nuro's Harp",
    "Queen's Escape",
    "Reach of the Council",
    "Realm Ender",
    "Reefbane",
    "Saemus' Gift",
    "Scaeva",
    "Shavronne's Gambit",
    "Silverbough",
    "Skirmish",
    "The Ascetic",
    "The Beast Fur Shawl",
    "The Cauteriser",
    "The Dancing Dervish",
    "The Gryphon",
    "The Oak",
    "The Overflowing Chalice",
    "The Signal Fire",
    "The Tempest",
    "Thirst for Horrors",
    "Three-step Assault",
    "Touch of Anguish",
    "Veruso's Battering Rams",
    "Voidheart",
    "Wall of Brambles",
    "Emperor's Cunning",
    "Emperor's Might",
    "Emperor's Wit",
    "Star of Wraeclast",
    "Advancing Fortress",
    "Axiom Perpetuum",
    "Cheap Construction",
    "Clayshaper",
    "Daresso's Passion",
    "Essence Worm",
    "Frostbreath",
    "Geofri's Sanctuary",
    "Glitterdisc",
    "Hair Trigger",
    "Heretic's Veil",
    "Iron Commander",
    "Malachai's Loop",
    "Obliteration",
    "Reckless Defence",
    "Rive",
    "Seven-League Step",
    "Singularity",
    "The Perandus Manor",
    "The Sorrow of the Divine",
    "The Tempestuous Steel",
    "The Writhing Jar",
    "Trypanon",
    "Umbilicus Immortalis",
    "Unstable Payload",
    "Varunastra",
    "Victario's Charity",
    "Viper's Scales",
    "Widowmaker",
    "Wyrmsign",
    "Xirgil's Crank",
    "Zerphi's Last Breath",
    "Demigod's Dominance",
    "Winterheart",
    "Slivers of Providence",
    "Agnerod West",
    "Allure",
    "Bitterdream",
    "Blightwell",
    "Caer Blaidd, Wolfpack's Den",
    "Coruscating Elixir",
    "Dead Reckoning",
    "Eclipse Solaris",
    "Extractor Mentis",
    "Eyes of the Greatwolf",
    "Faminebind",
    "Feastbind",
    "Femurs of the Saints",
    "Growing Agony",
    "Hezmana's Bloodlust",
    "Kongming's Stratagem",
    "Natural Hierarchy",
    "Night's Hold",
    "Pitch Darkness",
    "Rapid Expansion",
    "Repentance",
    "Rigwald's Command",
    "Rigwald's Crest",
    "Rigwald's Curse",
    "Rigwald's Quills",
    "Rigwald's Savagery",
    "Rolling Flames",
    "Rotgut",
    "Roth's Reach",
    "Shattered Chains",
    "Skyforth",
    "Spirit Guards",
    "Spirited Response",
    "Steel Spirit",
    "Storm Prison",
    "The Aylardex",
    "The Goddess Unleashed",
    "The Retch",
    "The Vigil",
    "The Vinktar Square",
    "Vessel of Vinktar",
    "Vessel of Vinktar",
    "Vessel of Vinktar",
    "Vessel of Vinktar",
    "Volley Fire",
    "Weight of the Empire",
    "Winter's Bounty",
    "Chitus' Needle",
    "Izaro's Turmoil",
    "Izaro's Dilemma",
    "Soulthirst",
    "Spine of the First Claimant",
    "Winds of Change",
    "Bloodgrip",
    "Broken Faith",
    "Steppan Eard",
    "The Pariah",
    "Emberwake",
    "Abberath's Horn",
    "Agnerod South",
    "Anatomical Knowledge",
    "Ancient Waystones",
    "Apparitions",
    "Assassin's Haste",
    "Atziri's Reign",
    "Blood Sacrifice",
    "Blood of Corruption",
    "Bloodplay",
    "Brawn",
    "Brinerot Flag",
    "Brinerot Mark",
    "Brinerot Whalers",
    "Brittle Barrier",
    "Brute Force Solution",
    "Call of the Brotherhood",
    "Callinellus Malleus",
    "Cameria's Maul",
    "Careful Planning",
    "Chill of Corruption",
    "Clear Mind",
    "Cold Steel",
    "Combustibles",
    "Conqueror's Efficiency",
    "Conqueror's Longevity",
    "Conqueror's Potency",
    "Corrupted Energy",
    "Crown of the Pale King",
    "Death's Hand",
    "Demigod's Beacon",
    "Doedre's Scorn",
    "Doryani's Fist",
    "Dreadarc",
    "Dyadian Dawn",
    "Efficient Training",
    "Eldritch Knowledge",
    "Empire's Grasp",
    "Energised Armour",
    "Energy From Within",
    "Fertile Mind",
    "Fevered Mind",
    "Fidelitas' Spike",
    "Fireborn",
    "Flesh-Eater",
    "Fluid Motion",
    "Fortified Legion",
    "Fragile Bloom",
    "Fragility",
    "Gorebreaker",
    "Goredrill",
    "Healthy Mind",
    "Heartbound Loop",
    "Hidden Potential",
    "Hotfooted",
    "Hungry Abyss",
    "Ichimonji",
    "Inertia",
    "Inspired Learning",
    "Intuitive Leap",
    "Jack, the Axe",
    "Jorrhast's Blacksteel",
    "Kingmaker",
    "Kingsguard",
    "Lakishu's Blade",
    "Lavianga's Wisdom",
    "Lion's Roar",
    "Lioneye's Fall",
    "Lioneye's Vision",
    "Malicious Intent",
    "Mantra of Flames",
    "Martial Artistry",
    "Might in All Forms",
    "Moonbender's Wing",
    "Mutated Growth",
    "Mutewind Pennant",
    "Mutewind Seal",
    "Mutewind Whispersteps",
    "Null's Inclination",
    "Nycta's Lantern",
    "Ornament of the East",
    "Pacifism",
    "Poacher's Aim",
    "Powerlessness",
    "Pugilist",
    "Rain of Splinters",
    "Realmshaper",
    "Redblade Band",
    "Redblade Banner",
    "Redblade Tramplers",
    "Relentless Fury",
    "Sacrificial Harvest",
    "Self-Flagellation",
    "Shaper's Seed",
    "Sire of Shards",
    "Southbound",
    "Spire of Stone",
    "Static Electricity",
    "Surgebinders",
    "Survival Instincts",
    "Survival Secrets",
    "Survival Skills",
    "Tear of Purity",
    "The Consuming Dark",
    "The Deep One's Hide",
    "The Princess",
    "The Restless Ward",
    "The Stormheart",
    "The Whispering Ice",
    "To Dust",
    "Tremor Rod",
    "Trolltimber Spire",
    "Twyzel",
    "Vaal Sentencing",
    "Ventor's Gamble",
    "Victario's Influence",
    "Warlord's Reach",
    "Weight of Sin",
    "Wildslash",
    "Ylfeban's Trickery",
    "Black Sun Crest",
    "Greed's Embrace",
    "Hall of Grandmasters",
    "Rashkaldor's Patience",
    "Warped Timepiece",
    "Agnerod North",
    "Bated Breath",
    "Belt of the Deceiver",
    "Bloodboil",
    "Brutus' Lead Sprinkler",
    "Doomsower",
    "Great Old One's Ward",
    "Kikazaru",
    "Malachai's Artifice",
    "Maligaro's Lens",
    "Maligaro's Restraint",
    "Maloney's Nightfall",
    "Ngamahu's Sign",
    "Nomic's Storm",
    "Prismweave",
    "Reverberation Rod",
    "Rumi's Concoction",
    "Scold's Bridle",
    "Sibyl's Lament",
    "Talisman of the Victor",
    "Tasalio's Sign",
    "Taste of Hate",
    "The Blood Thorn",
    "The Broken Crown",
    "The Rat Cage",
    "Timeclasp",
    "Ungil's Harmony",
    "Valako's Sign",
    "Agnerod East",
    "Demigod's Eye",
    "Sentari's Answer",
    "Oba's Cursed Trove",
    "Whakawairua Tuahu",
    "Apep's Rage",
    "Chalice of Horrors",
    "Cherrubim's Maleficence",
    "Craghead",
    "Dreamfeather",
    "Edge of Madness",
    "Flesh and Spirit",
    "Gang's Momentum",
    "Hegemony's Era",
    "Mark of the Doubting Knight",
    "Mokou's Embrace",
    "Null and Void",
    "Shadows and Dust",
    "The Dark Seer",
    "The Harvest",
    "Untainted Paradise",
    "Pledge of Hands",
    "Pyre",
    "Thousand Teeth Temu",
    "Piscator's Vigil",
    "Blood of Summer",
    "Death and Taxes",
    "Forbidden Taste",
    "Jaws of Agony",
    "Scar of Fate",
    "Soul Strike",
    "Asphyxia's Wrath",
    "Doomfletch",
    "Hyaon's Fury",
    "Kaom's Roots",
    "Hyrri's Bite",
    "Incandescent Heart",
    "Mao Kun",
    "Mjölner",
    "Queen of the Forest",
    "Demigod's Bounty",
    "The Three Dragons",
    "Windripper",
    "Atziri's Acuity",
    "Atziri's Disfavour",
    "Atziri's Promise",
    "Atziri's Splendour",
    "Atziri's Step",
    "Doryani's Catalyst",
    "Doryani's Invitation",
    "Drillneck",
    "Rearguard",
    "The Vertex",
    "Vaal Caress",
    "Vis Mortis",
    "Voideye",
    "Alberon's Warpath",
    "Dying Breath",
    "Skullhead",
    "Snakebite",
    "Solaris Lorica",
    "Dusktoe",
    "Romira's Banquet",
    "Shackles of the Wretched",
    "The Screaming Eagle",
    "Bino's Kitchen Knife",
    "Fencoil",
    "Song of the Sirens",
    "Veil of the Night",
    "Wheel of the Stormsail",
    "Briskwrap",
    "Daresso's Defiance",
    "Marylene's Fallacy",
    "Oro's Sacrifice",
    "Belly of the Beast",
    "Lifesprig",
    "Olmec's Sanctum",
    "Wings of Entropy",
    "Ashes of the Sun",
    "Chains of Time",
    "Crown of Eyes",
    "Demigod's Touch",
    "Doedre's Elixir",
    "Doon Cuebiyari",
    "Fragment of Eternity",
    "Prismatic Eclipse",
    "Relic of the Cycle",
    "Remnant of Empires",
    "Rust of Winter",
    "Splinter of the Moon",
    "Tear of Entropy",
    "Thunder of the Dawn",
    "Vestige of Divinity",
    "Berek's Grip",
    "Berek's Pass",
    "Berek's Respite",
    "Blood of the Karui",
    "Cloak of Defiance",
    "Dyadus",
    "Headhunter",
    "Immortal Flesh",
    "Lavianga's Spirit",
    "The Gull",
    "The Taming",
    "Deerstalker",
    "Lightning Coil",
    "Ming's Heart",
    "Sunblast",
    "Cybil's Paw",
    "Kongor's Undying Rage",
    "Mon'tregul's Grasp",
    "Poorjoy's Asylum",
    "Quecholli",
    "Devoto's Devotion",
    "Mindspiral",
    "The Goddess Scorned",
    "Voltaxic Rift",
    "Wideswing",
    "Deidbell",
    "Leer Cast",
    "The Anvil",
    "Auxium",
    "Death's Oath",
    "Soul Taker",
    "The Blood Dance",
    "Demigod's Stride",
    "Divination Distillate",
    "Infernal Mantle",
    "Perandus Signet",
    "Rebuke of the Vaal",
    "Daresso's Salute",
    "Death Rush",
    "Gifts from Above",
    "Shavronne's Revelation",
    "Victario's Acuity",
    "Voll's Devotion",
    "The Bringer of Rain",
    "Last Resort",
    "Void Battery",
    "Voidbringer",
    "Lightbane Raiment",
    "Lori's Lantern",
    "Thunderfist",
    "Zahndethus' Cassock",
    "Al Dhih",
    "Atziri's Foible",
    "Storm Cloud",
    "Acton's Nightmare",
    "Asenath's Gentle Touch",
    "Rat's Nest",
    "Thief's Torment",
    "Abyssus",
    "Alpha's Howl",
    "Aurumvorax",
    "Soul Mantle",
    "The Coward's Trial",
    "Darkray Vectors",
    "Icetomb",
    "Pillar of the Caged God",
    "Tabula Rasa",
    "Bronn's Lithe",
    "Carcass Jack",
    "Rainbowstride",
    "Rise of the Phoenix",
    "Bloodseeker",
    "Chober Chaber",
    "Thousand Ribbons",
    "Maelström of Chaos",
    "Matua Tupuna",
    "Starkonja's Head",
    "Chernobog's Pillar",
    "Heartbreaker",
    "Le Heup of All",
    "Shavronne's Wrappings",
    "Demigod's Triumph",
    "The Blood Reaper",
    "Aegis Aurora",
    "Atziri's Mirror",
    "Bramblejack",
    "Foxshade",
    "Prism Guardian",
    "Queen's Decree",
    "The Covenant",
    "The Supreme Truth",
    "Mortem Morsu",
    "Taryn's Shiver",
    "Goldrim",
    "Cloak of Flame",
    "Midnight Bargain",
    "Titucius' Span",
    "Ashrend",
    "Essentia Sanguis",
    "Infractem",
    "Victario's Flight",
    "Bones of Ullr",
    "Brightbeak",
    "Carnage Heart",
    "Chin Sol",
    "Darkscorn",
    "Facebreaker",
    "Goldwyrm",
    "Limbsplit",
    "Marohi Erqi",
    "Quill Rain",
    "Sin Trek",
    "Ungil's Gauche",
    "Voidhome",
    "Meginord's Vise",
    "Springleaf",
    "Vaults of Atziri",
    "Moonsorrow",
    "Rime Gaze",
    "Ambu's Charge",
    "Reaper's Pursuit",
    "Saffell's Frame",
    "Terminus Est",
    "The Goddess Bound",
    "Astramentis",
    "Crest of Perandus",
    "Daresso's Courage",
    "Kaltenhalt",
    "Lioneye's Remorse",
    "Meginord's Girdle",
    "Perandus Blazon",
    "Rathpith Globe",
    "The Ignomon",
    "The Magnate",
    "Wurm's Molt",
    "Araku Tiki",
    "Asenath's Mark",
    "Aurseize",
    "Chitus' Apex",
    "Crown of Thorns",
    "Doedre's Tenure",
    "Fairgraves' Tricorne",
    "Geofri's Crest",
    "Heatshiver",
    "Honourhome",
    "Hrimnor's Resolve",
    "Hrimsorrow",
    "Hyrri's Ire",
    "Kaom's Heart",
    "Lioneye's Paws",
    "Lochtonial Caress",
    "Maligaro's Virtuosity",
    "Mightflay",
    "Ondar's Clasp",
    "Sadima's Touch",
    "Shavronne's Pace",
    "Slitherpinch",
    "Sundance",
    "The Peregrine",
    "Wake of Destruction",
    "Wanderlust",
    "Windscream",
    "Wondertrap",
    "Blackgleam",
    "Broadstroke",
    "Death's Harp",
    "Doedre's Damning",
    "Dream Fragments",
    "Eye of Chayula",
    "Ezomyte Peak",
    "Geofri's Baptism",
    "Hrimnor's Hymn",
    "Karui Ward",
    "Malachai's Simula",
    "Rigwald's Charge",
    "Shiversting",
    "Sidhebreath",
    "The Searing Touch",
    "Demigod's Presence",
    "Divinarius",
    "Ephemeral Edge",
    "Silverbranch",
    "Voll's Protector",
    "Andvarius",
    "Blackheart",
    "Kaom's Sign",
    "Lioneye's Glare",
    "Kaom's Primacy",
    "Redbeak",
    "Stone of Lazhwar"
]
legendaries = [
    "[Acherus Drapes]",
    "[Shackles of Bryndaor]",
    "[Rattlegore Bone Legplates]",
    "[Service of Gorefiend]",
    "[Lana'thel's Lament]",
    "[Skullflower's Haemostasis]",
    "[Seal of Necrofantasia]",
    "[Koltira's Newfound Will]",
    "[Toravon's Whiteout Bindings]",
    "[Perseverance of the Ebon Martyr]",
    "[Consort's Cold Core]",
    "[Tak'theritrix's Shoulderpads]",
    "[Draugr, Girdle of the Everlasting King]",
    "[Uvanimor, the Unbeautiful]",
    "[The Instructor's Fourth Lesson]",
    "[Death March]",
    "[Mo'arg Bionic Stabilizers]",
    "[Raddon's Cascading Eyes]",
    "[Achor, the Eternal Hunger]",
    "[Loramus Thalipedes' Sacrifice]",
    "[Anger of the Half-Giants]",
    "[Delusions of Grandeur]",
    "[Cloak of Fel Flames]",
    "[Kirel Narak]",
    "[Runemaster's Pauldrons]",
    "[The Defiler's Lost Vambraces]",
    "[Fragment of the Betrayer's Prison]",
    "[Spirit of the Darkness Flame]",
    "[Ekowraith, Creator of Worlds]",
    "[Impeccable Fel Essence]",
    "[Promise of Elune, the Moon Goddess]",
    "[The Emerald Dreamcatcher]",
    "[Oneth's Intuition]",
    "[Lady and the Child]",
    "[Chatoyant Signet]",
    "[Ailuro Pouncers]",
    "[The Wildshaper's Clutch]",
    "[Fiery Red Maimers]",
    "[Luffa Wrappings]",
    "[Skysec's Hold]",
    "[Elize's Everlasting Encasement]",
    "[Dual Determination]",
    "[Oakheart's Puny Quods]",
    "[Tearstone of Elune]",
    "[Essence of Infusion]",
    "[Edraith, Bonds of Aglaya]",
    "[Aman'Thul's Wisdom]",
    "[The Dark Titan's Advice]",
    "[X'oni's Caress]",
    "[The Shadow Hunter's Voodoo Mask]",
    "[Roar of the Seven Lions]",
    "[Qa'pla, Eredun War Order]",
    "[The Apex Predator's Claw]",
    "[The Mantle of Command]",
    "[Call of the Wild]",
    "[Magnetized Blasting Cap Launcher]",
    "[Ullr's Feather Snowshoes]",
    "[Zevrim's Hunger]",
    "[War Belt of the Sentinel Army]",
    "[MKII Gyroscopic Stabilizer]",
    "[Nesingwary's Trapping Treads]",
    "[Frizzo's Fingertrap]",
    "[Helbrine, Rope of the Mist Marauder]",
    "[Butcher's Bone Apron]",
    "[Tearstone of Elune]",
    "[Essence of Infusion]",
    "[Edraith, Bonds of Aglaya]",
    "[Aman'Thul's Wisdom]",
    "[The Dark Titan's Advice]",
    "[X'oni's Caress]",
    "[Shard of the Exodar]",
    "[Belo'vir's Final Stand]",
    "[Rhonin's Assaulting Armwraps]",
    "[Cord of Infinity]",
    "[Mystic Kilt of the Rune Master]",
    "[Gravity Spiral]",
    "[Koralon's Burning Touch]",
    "[Darckli's Dragonfire Diadem]",
    "[Marquee Bindings of the Sun King]",
    "[Pyrotex Ignition Cloth]",
    "[Lady Vashj's Grasp]",
    "[Magtheridon's Banished Bracers]",
    "[Zann'esu Journey]",
    "[Ice Time]",
    "[Firestone Walkers]",
    "[Sal'salabim's Lost Tunic]",
    "[Fundamental Observation]",
    "[Gai Plin's Soothing Sash]",
    "[Jewel of the Lost Abbey]",
    "[Anvil-Hardened Wristwraps]",
    "[Eye of Collidus the Warp-Watcher]",
    "[Petrichor Lagniappe]",
    "[Leggings of The Black Flame]",
    "[Unison Spaulders]",
    "[Ei'thas, Lunar Glides of Eramas]",
    "[Ovyd's Winter Wrap]",
    "[Shelter of Rin]",
    "[Cenedril, Reflector of Hatred]",
    "[Drinking Horn Cover]",
    "[March of the Legion]",
    "[Hidden Master's Forbidden Touch]",
    "[Katsuo's Eclipse]",
    "[The Emperor's Capacitor]",
    "[Chain of Thrayn]",
    "[Ilterendi, Crown Jewel of Silvermoon]",
    "[Obsidian Stone Spaulders]",
    "[Tyr's Hand of Faith]",
    "[Maraad's Dying Breath]",
    "[Uther's Guard]",
    "[Heathcliff's Immortality]",
    "[Tyelca, Ferren Marcus's Stature]",
    "[Breastplate of the Golden Val'kyr]",
    "[Saruan's Resolve]",
    "[Liadrin's Fury Unleashed]",
    "[Aegisjalmur, the Armguards of Awe]",
    "[Whisper of the Nathrezim]",
    "[Justice Gaze]",
    "[Ashes to Dust]",
    "[Cord of Maiev, Priestess of the Moon]",
    "[Estel, Dejahna's Inspiration]",
    "[N'ero, Band of Promises]",
    "[Skjoldr, Sanctuary of Ivagont]",
    "[Xalan the Feared's Clench]",
    "[Kam Xi'raff]",
    "[X'anshi, Shroud of Archbishop Benedictus]",
    "[Muze's Unwavering Will]",
    "[Phyrix's Embrace]",
    "[Entrancing Trousers of An'juna]",
    "[Al'maiesh, the Cord of Hope]",
    "[Rammal's Ulterior Motive]",
    "[Anund's Seared Shackles]",
    "[Zenk'aram, Iridi's Anadem]",
    "[The Twins' Painful Touch]",
    "[Mangaza's Madness]",
    "[Mother Shahraz's Seduction]",
    "[Zeks Exterminatus]",
    "[Insignia of Ravenholdt]",
    "[Will of Valeera]",
    "[Mantle of the Master Assassin]",
    "[Duskwalker's Footpads]",
    "[Zoldyck Family Training Shackles]",
    "[The Dreadlord's Deceit]",
    "[Thraxi's Tricksy Treads]",
    "[Greenskin's Waterlogged Wristcuffs]",
    "[Shivarran Symmetry]",
    "[Shadow Satyr's Walk]",
    "[Denial of the Half-Giants]",
    "[Uncertain Reminder]",
    "[Eye of the Twisting Nether]",
    "[The Deceiver's Blood Pact]",
    "[Echoes of the Great Sundering]",
    "[Pristine Proto-Scale Girdle]",
    "[Al'Akir's Acrimony]",
    "[Storm Tempests]",
    "[Akainu's Absolute Justice]",
    "[Emalon's Charged Core]",
    "[Spiritual Journey]",
    "[Focuser of Jonat, the Elder]",
    "[Intact Nazjatar Molting]",
    "[Elemental Rebalancers]",
    "[Praetorian's Tidecallers]",
    "[Nobundo's Redemption]",
    "[Pillars of the Dark Portal]",
    "[Sacrolash's Dark Strike]",
    "[Power Cord of Lethtendris]",
    "[Streten's Sleepless Shackles]",
    "[Hood of Eternal Disdain]",
    "[Reap and Sow]",
    "[Kazzak's Final Curse]",
    "[Wilfred's Sigil of Superior Summoning]",
    "[Recurrent Ritual]",
    "[Sin'dorei Spite]",
    "[Wakener's Loyalty]",
    "[Alythess's Pyrogenics]",
    "[Odr, Shawl of the Ymirjar]",
    "[Feretory of Souls]",
    "[Magistrike Restraints]",
    "[Lessons of Space-Time]",
    "[Mannoroth's Bloodletting Manacles]",
    "[Timeless Stratagem]",
    "[Weight of the Earth]",
    "[Archavon's Heavy Hand]",
    "[Ayala's Stone Heart]",
    "[Naj'entus's Vertebrae]",
    "[Ceann-Ar Charger]",
    "[Kazzalax, Fujieda's Fury]",
    "[Thundergod's Vigor]",
    "[The Walls Fell]",
    "[Kakushan's Stormscale Gauntlets]",
    "[Destiny Driver]",
    "[Kargath's Sacrificed Hands]",
    "[Norgannon's Foresight]",
    "[Cinidaria, the Symbiote]",
    "[Roots of Shaladrassil]",
    "[Aggramar's Stride]",
    "[Archimonde's Hatred Reborn]",
    "[Kil'jaeden's Burning Wish]",
    "[Velen's Future Sight]",
    "[Sephuz's Secret]",
    "[Prydaz, Xavaric's Magnum Opus]"
]


class StatTrak:

    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS messages
             (unix real, timestamp timestamp, content text, id text, author text, channel text, server text)''')


    def fix_member(self, member):
        roles = ','.join([str(x.id)
                                for x in member.roles if x.name != "@everyone"])
        names = member.display_name
        self.c.execute('''INSERT OR IGNORE INTO users
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (roles, str(member.guild.id), None, member.id, names, 0, 0, 0))
        self.conn.commit()

    def fix_postcount(self, message):
        if message.guild is None:
            return
        self.c.execute('UPDATE users SET postcount = postcount + 1 WHERE (id=? AND server=?)',
                    (message.author.id, message.guild.id))
        self.conn.commit()            

    # @commands.group(pass_context=True, invoke_without_command=True)
    # async def agraph(self, ctx, member : discord.Member = None):
    #     user = ctx.message.author if member is None else member
    #     a = self.c.execute('''SELECT COUNT(id), strftime("%H", timestamp) AS cnt FROM messages WHERE server=207943928018632705 GROUP BY strftime("%H", timestamp) ORDER BY strftime("%H", timestamp) ASC;''')
    #     a = a.fetchall()
    #     x_axis = [x for x in range(25)]
    #     y_axis = [x[0] for x in a]
    #     y_axis.insert(2, 0)
    #     plt.figure()
    #     x = plt.plot(x_axis, y_axis)
    #     plt.setp(x, linewidth=1)
    #     plt.xlabel('Day of the year')
    #     plt.ylabel('messages posted')
    #     plt.title("Global activity")
    #     buf = BytesIO()
    #     plt.savefig(buf, format='png', dpi=1000)
    #     buf.seek(0)
    #     xd = discord.File(fp=buf, filename="suckmydick.png")
    #     await ctx.send(file=xd)

    

    @commands.group(name="postcount", aliases=['pc'], invoke_without_command=True)
    async def pc(self, ctx, member: discord.Member = None):
        user = ctx.author if member is None else member
        self.c.execute('SELECT postcount FROM users WHERE (server=? AND id=?)', (ctx.guild.id, user.id))
        try:
            a = self.c.fetchone()[0]
        except TypeError:
            self.fix_member(ctx.author)
            return await ctx.send("**{}** has posted **0** messages.".format(user.name))
        else:
            await ctx.send("**{}** has posted **{}** messages.".format(user.name, a))

    @pc.command(name="top", pass_context=True)
    async def postcounttop(self, ctx):
        a = self.c.execute(
            'SELECT * FROM users WHERE (server=? AND postcount > 0) ORDER BY postcount DESC LIMIT 20', (ctx.guild.id,))
        a = a.fetchall()
        b = self.c.execute(
            'SELECT SUM(postcount) AS "hello" FROM users WHERE (server=? AND postcount > 0)', (ctx.guild.id,))
        b = b.fetchone()[0]
        post_this = ""
        rank = 1
        for row in a:
            name = f'<@{row[3]}>'
            post_this += ("{}. {} : {}\n".format(rank, name, row[5]))
            rank += 1
        post_this += "\n**{0}** posts by **{1}** chatters.".format(
            b, len([x for x in ctx.guild.members]))
        em = discord.Embed(title="Current standings:",
                           description=post_this, colour=0x14e818)
        em.set_author(name=self.bot.user.name,
                      icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=em)

    async def on_member_join(self, member):
        a = self.c.execute(
            'SELECT * FROM users WHERE (id=? AND server=?)', (member.id, member.guild.id))
        a = a.fetchall()
        if a != []:
            return
        roles = ','.join([str(x.id) for x in member.roles if (
            x.name != "@everyone")])
        self.c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (roles, member.guild.id, None, member.id, member.display_name, 0, 0, 0))
        self.conn.commit()
        # xd = self.c.execute(
        #     'SELECT * FROM userconfig WHERE (guild_id=? AND user_id=?)', (member.guild.id, member.id))
        # xd = xd.fetchall()
        # if xd == []:
        #     self.c.execute('INSERT INTO userconfig VALUES (?, ?, ?, ?, ?, ?)',
        #                    (member.guild.id, member.id, None, None, False, None))
        #     self.conn.commit()

    async def on_guild_join(self, guild):
        self.c.execute('INSERT OR IGNORE  INTO servers VALUES (?, ?, ?, ?, ?, ?)',
                        (guild.id, None, None, None, None, '?,!'))
        self.conn.commit()
        self.c.execute('INSERT OR IGNORE INTO logging VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (guild.id, 1, 1, 1, 1, 1, 1, 1, None))
        self.conn.commit()
        self.c.execute('''INSERT OR IGNORE INTO role_config
                        VALUES (?, ?, ?, ?, ?)''',
                    (None, False, guild.id, None, True))
        self.conn.commit()
        self.c.execute('''INSERT OR IGNORE INTO config
                        VALUES (?, ?, ?, ?, ?, ?)''',
                    (guild.id, None, None, True, None, None))
        self.conn.commit()
        for member in guild.members:
            roles = ','.join(
                [str(x.id) for x in member.roles if x.name != "@everyone"])
            self.c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (roles, member.guild.id, None, member.id, member.display_name, 0, 0, 0))
            self.conn.commit()
            # self.c.execute('''SELECT *
            #                   FROM userconfig
            #                   WHERE (user_id=? AND guild_id=?)''',
            #                 (member.id, member.guild.id))
            # userconfig = self.c.fetchall()
            # if userconfig == []:
            #     self.c.execute('''INSERT INTO userconfig VALUES (?, ?, ?, ?, ?, ?)''',
            #     (member.guild.id, member.id, None, None, False, None))
            #     self.conn.commit()



    async def on_message(self, message):
        if message.guild is None:
            return
        if message.guild.id in (207943928018632705, 113103747126747136):
            if message.guild.id == 207943928018632705 and random.randint(1, 10000) == 1:
                legendaryRole = discord.utils.get(
                    message.guild.roles, name='Legendary')
                await message.author.add_roles(legendaryRole)
                await message.channel.send("{} just received a legendary item: **{}**".format(message.author.mention, random.choice(legendaries)))

            elif message.guild.id == 113103747126747136 and random.randint(1, 25000) == 1:
                await message.channel.send("{} just received a legendary item: **{}**".format(message.author.mention, random.choice(legendaries)))
        if (random.randint(1, 5000) == 1 and message.channel.id == 251064728795873281):
            quality = random.randint(1, 6)
            legendaryRole = discord.utils.get(
                message.guild.roles, name='Unique')
            await message.author.add_roles(legendaryRole)
            await message.channel.send("{} You found a unique, exile. It's a **{}l {}**".format(message.author.mention, quality, random.choice(uniques)))
        
        self.fix_postcount(message)
        if message.content == "":
            return
        self.c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)", (message.created_at.timestamp(), message.created_at.strftime(
            dt_format), message.clean_content, message.id, message.author.id, message.channel.id, message.guild.id))
        self.conn.commit()


def setup(bot):
    bot.add_cog(StatTrak(bot))
