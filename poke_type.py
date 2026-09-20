"""
====================================================================
               POKÉMON TYPE SYSTEM: THE PokeType CLASS
====================================================================
Models Pokémon elemental types and their interactions using the
Type Object Pattern.
====================================================================
"""

class PokeType:
    """
    Represents an elemental type in Pokémon (e.g., Fire, Water, Grass).
    Encapsulates offensive type advantages and defensive resistances.
    """
    _registry = {}

    def __init__(self, name, super_effective=None, not_very_effective=None, no_effect=None):
        """
        Initializes a PokeType with its offensive matchup sets.
        - super_effective: types that take 2.0x damage from this type
        - not_very_effective: types that take 0.5x damage from this type
        - no_effect: types that take 0.0x damage from this type
        """
        self.name = str(name).strip().capitalize()
        self.super_effective = {str(t).strip().capitalize() for t in (super_effective or [])}
        self.not_very_effective = {str(t).strip().capitalize() for t in (not_very_effective or [])}
        self.no_effect = {str(t).strip().capitalize() for t in (no_effect or [])}

    def effectiveness_against(self, defender_type):
        """
        Offensive perspective:
        Calculates the damage multiplier when an attack of this type hits defender_type.
        Returns 2.0 for super effective, 0.5 for not very effective, 0.0 for immune, and 1.0 for neutral.
        """
        if isinstance(defender_type, PokeType):
            target = defender_type.name
        else:
            target = str(defender_type).strip().capitalize()

        if target in self.no_effect:
            return 0.0
        if target in self.super_effective:
            return 2.0
        if target in self.not_very_effective:
            return 0.5
        return 1.0

    def defensive_multiplier_against(self, incoming_move_type):
        """
        Defensive perspective:
        Calculates the damage multiplier this Pokémon takes when struck by incoming_move_type.
        """
        attacker_type = PokeType.get(incoming_move_type)
        return attacker_type.effectiveness_against(self)

    def add_advantage(self, defender_type):
        """Adds a super effective advantage (2.0x) against defender_type."""
        target = defender_type.name if isinstance(defender_type, PokeType) else str(defender_type).strip().capitalize()
        self.super_effective.add(target)
        self.not_very_effective.discard(target)
        self.no_effect.discard(target)

    def add_disadvantage(self, defender_type):
        """Adds a not-very-effective disadvantage (0.5x) against defender_type."""
        target = defender_type.name if isinstance(defender_type, PokeType) else str(defender_type).strip().capitalize()
        self.not_very_effective.add(target)
        self.super_effective.discard(target)
        self.no_effect.discard(target)

    def add_immunity(self, defender_type):
        """Adds an immunity (0.0x) against defender_type."""
        target = defender_type.name if isinstance(defender_type, PokeType) else str(defender_type).strip().capitalize()
        self.no_effect.add(target)
        self.super_effective.discard(target)
        self.not_very_effective.discard(target)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"PokeType('{self.name}')"

    def __eq__(self, other):
        """
        Enables seamless comparison with both PokeType instances and strings:
        poke_type == 'Electric' or poke_type == PokeType.get('Electric')
        """
        if isinstance(other, PokeType):
            return self.name.lower() == other.name.lower()
        if isinstance(other, str):
            return self.name.lower() == other.strip().lower()
        return False

    def __hash__(self):
        return hash(self.name.lower())

    @classmethod
    def register(cls, poke_type):
        """Registers a PokeType instance in the shared registry."""
        cls._registry[poke_type.name.lower()] = poke_type
        return poke_type

    @classmethod
    def get(cls, name_or_instance):
        """
        Retrieves a PokeType instance from the registry.
        If given a PokeType, returns it as-is.
        If given an unknown string, automatically creates and registers a neutral type.
        """
        if isinstance(name_or_instance, cls):
            return name_or_instance
        
        name_clean = str(name_or_instance).strip().lower()
        if name_clean in cls._registry:
            return cls._registry[name_clean]

        # Dynamically create and register unknown type (defaults to neutral interactions)
        new_type = cls(name_or_instance)
        cls._registry[name_clean] = new_type
        return new_type

    @classmethod
    def all_types(cls):
        """Returns a list of all registered PokeType objects."""
        return list(cls._registry.values())


def _init_default_types():
    """Initializes standard types based on pokemon_data TYPE_CHART."""
    from pokemon_data import TYPE_CHART

    # Standard types in the game
    known_types = [
        "Normal", "Fire", "Water", "Grass", "Electric",
        "Flying", "Ghost", "Psychic", "Bug", "Steel", "Dragon"
    ]
    for type_name in known_types:
        PokeType.register(PokeType(type_name))

    # Populate matchups from TYPE_CHART
    for (attacker, defender), mult in TYPE_CHART.items():
        atk_obj = PokeType.get(attacker)
        if mult == 2.0:
            atk_obj.add_advantage(defender)
        elif mult == 0.5:
            atk_obj.add_disadvantage(defender)
        elif mult == 0.0:
            atk_obj.add_immunity(defender)

# Auto-initialize standard types when module is loaded
_init_default_types()
