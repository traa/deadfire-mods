# Requirements Document

## Introduction

This feature enables the Rymrgand food spoiling challenge in Pillars of Eternity 2: Deadfire for existing save games without requiring a new game start. The Rymrgand challenge is one of the Berath's Blessings that makes food spoil over time and requires prepared meals for resting, adding survival mechanics to the game.

## Requirements

### Requirement 1

**User Story:** As a player with an existing save game, I want to enable the Rymrgand food spoiling challenge so that I can experience the survival mechanics without starting over.

#### Acceptance Criteria

1. WHEN the mod is installed THEN the Rymrgand challenge should be automatically activated for existing save games
2. WHEN food items are in inventory THEN they SHALL start spoiling according to their SpoilHours values
3. WHEN attempting to rest THEN the system SHALL require prepared meals (RestType: "PreparedMeal") instead of basic food
4. WHEN the challenge is active THEN the FoodSpoils flag SHALL be set to "true" globally

### Requirement 2

**User Story:** As a player, I want all existing food items to have proper spoiling timers so that the challenge mechanics work correctly from activation.

#### Acceptance Criteria

1. WHEN the mod activates THEN all food items in inventory SHALL have their spoil timers initialized
2. WHEN food spoils THEN it SHALL be removed from inventory or converted to spoiled food
3. WHEN examining food items THEN players SHALL see remaining spoil time in tooltips
4. IF food has already exceeded its spoil time THEN it SHALL immediately spoil upon mod activation

### Requirement 3

**User Story:** As a player, I want the mod to work seamlessly with existing game systems so that it doesn't break my current playthrough.

#### Acceptance Criteria

1. WHEN the mod is installed THEN existing save games SHALL load without corruption
2. WHEN the challenge is active THEN ship morale bonuses from food SHALL continue to work normally
3. WHEN using prepared meals THEN they SHALL provide proper rest bonuses
4. WHEN the mod is removed THEN save games SHALL remain playable (graceful degradation)

### Requirement 4

**User Story:** As a modder, I want the implementation to be compatible with other food-related mods so that players can use multiple mods together.

#### Acceptance Criteria

1. WHEN other food mods are present THEN the spoiling system SHALL work with modded food items
2. WHEN food items are added by other mods THEN they SHALL inherit appropriate spoil times
3. WHEN conflicts occur THEN the mod SHALL prioritize compatibility over strict challenge rules
4. WHEN loading with other mods THEN no game crashes SHALL occur due to mod interactions