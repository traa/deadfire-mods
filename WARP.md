# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is **Rymrgand's Trial**, a Pillars of Eternity 2: Deadfire mod that enhances challenges related to Rymrgand, the god of death and entropy. The project follows Pillars of Eternity 2's official modding structure with comprehensive game data documentation.

## Key Commands

### Development Workflow
```bash
# Test mod in-game (copy to Override directory if not already there)
cp -r . "/Users/andriistepikov/Library/Application Support/Steam/steamapps/common/Pillars of Eternity II/PillarsOfEternityII.app/Contents/Override/Rymrgands Trial"

# Validate JSON files
find . -name "*.json" -exec sh -c 'echo "Checking: $1" && python -m json.tool "$1" > /dev/null' _ {} \;

# Check manifest structure
cat manifest.json | python -m json.tool

# Clean Mac-specific files
find . -name ".DS_Store" -delete
find . -name "._*" -delete
```

### Documentation Access
```bash
# Open game data documentation in browser
open docs/Modding/index.html

# Quick reference for specific sections
open docs/Modding/gamedatatypes.html  # Game data types and components
open docs/Modding/components.html     # Available components
open docs/Modding/scripts.html        # Script functions
open docs/Modding/structures.html     # Data structures
```

### Version Control
```bash
# Standard Git workflow - always test changes before committing
git add .
git commit -m "Descriptive commit message"

# Check for mod file issues
find design/ localized/ -name "*.gamedatabundle" -o -name "*.stringtable" -exec ls -la {} \;
```

## Architecture

### Project Structure
```
├── design/           # Game data modifications (.gamedatabundle files)
├── localized/        # Localization files (.stringtable files)  
├── docs/Modding/     # Comprehensive modding documentation (HTML)
├── manifest.json     # Mod metadata and compatibility information
├── README.md         # Project documentation
└── .gitignore        # File exclusions
```

### Pillars of Eternity 2 Modding Framework

#### Core Concepts
- **Game Data Objects**: JSON objects loaded from `.gamedatabundle` files
- **Components**: Modular data pieces that define object behavior and properties
- **Partial Override**: Mod files override only specified properties, leaving others unchanged
- **Load Order**: Base game → DLC → Mods (controllable via in-game Mod Manager)

#### File Types & Purpose
- **`.gamedatabundle`** - Contains GameDataObjects with component arrays
- **`.stringtable`** - Localized text for different languages
- **`.conversationbundle`** - Dialogue and conversation modifications
- **`manifest.json`** - Mod metadata (title, description, version, compatibility)

#### Game Data Structure
Every GameDataObject has:
- `$type` - Assembly type string (e.g., "Game.GameData.*, Assembly-CSharp")
- `DebugName` - Human-readable identifier
- `ID` - Globally unique identifier (GUID)
- `Components` - Array of GameDataComponent objects

### Documentation Architecture
The `docs/Modding/` directory contains complete API documentation:

- **`index.html`** - Main concepts and GameDataObject structure
- **`gamedatatypes.html`** - All available game data types and required components
- **`components.html`** - Detailed component specifications
- **`enumerations.html`** - Enum values and constants
- **`structures.html`** - Complex data structures used in components
- **`instanceids.html`** - Predefined object IDs for referencing vanilla content
- **`scripts.html`** - Available script functions for interactions
- **`conditionals.html`** - Conditional script functions
- **`preferences.html`** - AI targeting preference scripts

## Development Guidelines

### Manifest Requirements
- `ModVersion` - Increment when making changes
- `SupportedGameVersion` - Currently targets 4.0.0-5.0.0
- `Title` and `Description` - Support localization with language keys
- `Author` - Attribution information

### Game Data Creation
1. **Reference Documentation**: Always check `docs/Modding/gamedatatypes.html` for required components
2. **Component Structure**: Use `docs/Modding/components.html` for component property specifications
3. **GUID Management**: Generate unique GUIDs for new objects, reference existing ones for modifications
4. **Type Strings**: Use exact Assembly type strings from documentation

### Working with Scripts
- **Script Functions**: Reference `docs/Modding/scripts.html` for available functions
- **Parameters**: Use correct parameter types (Guid for instance IDs, specific enums, etc.)
- **Conditional Logic**: Leverage `docs/Modding/conditionals.html` for complex conditions

### Localization Workflow
1. Create base English strings in `.stringtable` files
2. Structure: `{ "Entries": [{"ID": number, "DefaultText": "text", "FemaleText": "optional"}] }`
3. Place in appropriate `localized/[language]/` subdirectories
4. Reference via string table IDs in game data components

### Testing Process
1. Copy mod to Override directory
2. Launch Pillars of Eternity 2
3. Enable mod in Options > Mod Manager
4. Test functionality in-game
5. Check game logs for errors
6. Verify with different language settings if using localization

## Advanced Modding Patterns

### Partial Overrides
- Modify existing vanilla content by using the same GUID
- Only specify properties you want to change
- Unspecified properties remain vanilla values

### Component Dependencies
- Check `gamedatatypes.html` for required vs. optional components
- Some components depend on others (e.g., StatusEffectComponent often needs additional effect components)

### Script Integration
- Use `DataScriptEventComponent` for custom script triggers
- Reference specific script functions from `scripts.html`
- Parameter validation crucial - wrong types cause runtime errors

### AI Customization
- Custom AI uses `CustomAI*` game data types
- Reference `preferences.html` for targeting behaviors
- Conditional scripts enable complex AI decision trees

## Compatibility Considerations

- **Game Version**: v4.1.0.0025 documentation base
- **Load Order**: Mod Manager controls loading sequence
- **ID Conflicts**: Avoid GUID collisions with other mods
- **Component Changes**: Breaking changes between game versions affect component structure

## File Locations

### Game Installation (Mac)
```
~/Library/Application Support/Steam/steamapps/common/Pillars of Eternity II/PillarsOfEternityII.app/Contents/
├── Override/                    # Mod installation directory
│   └── [ModName]/              # Individual mod folders
└── PillarsOfEternityII_Data/
    ├── exported/design/gamedata # Base game data
    └── *_exported/design/       # DLC game data
```

### Critical: Always work from the Override directory for testing. The game loads mods directly from this location.