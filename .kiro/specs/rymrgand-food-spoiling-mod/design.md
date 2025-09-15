# Design Document

## Overview

The Rymrgand Food Spoiling Mod enables the food spoiling challenge mechanics from Berath's Blessings for existing save games. The implementation involves modifying the game's challenge system, food item data, and rest mechanics to activate spoiling without requiring a new game.

## Architecture

The mod uses Pillars of Eternity 2's GameDataBundle system to override core game mechanics:

1. **Challenge System Override**: Modify the Rymrgand GodChallengeGameData to be automatically active
2. **Food Item Enhancement**: Ensure all food items have proper spoiling parameters
3. **Rest System Integration**: Enforce prepared meal requirements for resting
4. **Save Game Compatibility**: Use non-destructive overrides that maintain save compatibility

## Components and Interfaces

### Core Components

#### 1. Challenge Activation Component
- **Purpose**: Automatically enables Rymrgand challenge for existing saves
- **Implementation**: Override GodChallengeComponent with forced activation
- **Key Properties**:
  - `FoodSpoils: "true"`
  - `OnlyPreparedMealsRest: "true"`
  - Auto-activation logic for existing saves

#### 2. Food Spoiling System
- **Purpose**: Manages food deterioration over time
- **Implementation**: Enhanced ConsumableComponent data
- **Key Properties**:
  - `SpoilHours`: Time until food spoils
  - `RestType`: Determines if food can be used for resting
  - Spoil timer initialization for existing items

#### 3. Rest Validation System
- **Purpose**: Enforces prepared meal requirements
- **Implementation**: Override rest mechanics to check food types
- **Key Properties**:
  - Validate `RestType: "PreparedMeal"` for resting
  - Reject basic food items for rest
  - Maintain existing rest bonuses

### Data Structures

#### Enhanced GodChallengeGameData
```json
{
  "$type": "Game.GameData.GodChallengeGameData, Assembly-CSharp",
  "DebugName": "Rymrgand_AutoEnabled",
  "ID": "eb4a2e81-19c4-4af8-b14b-c49fb5c8c72a",
  "Components": [{
    "$type": "Game.GameData.GodChallengeComponent, Assembly-CSharp",
    "FoodSpoils": "true",
    "OnlyPreparedMealsRest": "true",
    "AutoActivateForExistingSaves": "true"
  }]
}
```

#### Food Item Categories
- **Basic Ingredients**: Short spoil times (122-280 hours)
- **Prepared Meals**: Medium spoil times (41-564 hours), can be used for resting
- **Preserved Foods**: Long spoil times (564-752 hours)
- **Alcohol**: Extended spoil times, morale bonuses

## Data Models

### Food Spoiling Tiers
1. **Tier 1 - Perishable** (122 hours): Fresh meat, fish, dairy, eggs
2. **Tier 2 - Semi-Stable** (280 hours): Vegetables, grains, nuts
3. **Tier 3 - Preserved** (564 hours): Alcohol, dried goods
4. **Tier 4 - Hardtack** (752 hours): Emergency rations

### Rest Requirements
- **Basic Food**: Cannot be used for resting when challenge is active
- **Prepared Meals**: Required for resting, provide full benefits
- **Ship Morale**: Maintained through food quality bonuses

## Error Handling

### Save Game Compatibility
- **Graceful Activation**: Challenge activates without corrupting saves
- **Fallback Mechanisms**: If spoiling fails, food remains usable
- **Mod Removal**: Save games remain playable if mod is uninstalled

### Food Item Validation
- **Missing Spoil Data**: Default to appropriate spoil times based on food type
- **Invalid Food Types**: Treat as basic ingredients with standard spoil times
- **Modded Food Items**: Inherit spoiling properties from similar vanilla items

### Rest System Failures
- **No Prepared Meals**: Provide clear error messages to players
- **Insufficient Food**: Allow emergency rest with penalties
- **System Conflicts**: Prioritize player experience over strict challenge rules

## Testing Strategy

### Unit Testing
- **Food Spoiling Logic**: Verify spoil timers work correctly
- **Rest Validation**: Ensure prepared meals are properly recognized
- **Challenge Activation**: Confirm automatic enabling for existing saves

### Integration Testing
- **Save Game Loading**: Test with various existing save states
- **Mod Compatibility**: Verify interaction with other food/challenge mods
- **Performance Impact**: Ensure spoiling system doesn't cause lag

### User Acceptance Testing
- **Existing Save Activation**: Players can enable challenge mid-playthrough
- **Food Management**: Spoiling mechanics feel balanced and fair
- **Rest Mechanics**: Prepared meal requirement is clear and manageable

### Edge Case Testing
- **Empty Inventory**: Challenge works when no food is present
- **Mass Food Spoiling**: System handles large quantities of spoiled food
- **Save/Load Cycles**: Spoil timers persist correctly across sessions