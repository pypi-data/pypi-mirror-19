"""Faker data providers for chemistry data."""

from random import choice, randrange

from faker.providers import BaseProvider


class ChemistryProvider(BaseProvider):
    """Chemistry data provider.

    Elements source: http://www.lenntech.com/periodic/name/alphabetic.htm
    """

    _elements = {
        'Actinium': 'Ac',
        'Aluminum': 'Al',
        'Americium': 'Am',
        'Antimony': 'Sb',
        'Argon': 'Ar',
        'Arsenic': 'As',
        'Astatine': 'At',
        'Barium': 'Ba',
        'Berkelium': 'Bk',
        'Beryllium': 'Be',
        'Bismuth': 'Bi',
        'Bohrium': 'Bh',
        'Boron': 'B',
        'Bromine': 'Br',
        'Cadmium': 'Cd',
        'Calcium': 'Ca',
        'Californium': 'Cf',
        'Carbon': 'C',
        'Cerium': 'Ce',
        'Cesium': 'Cs',
        'Chlorine': 'Cl',
        'Chromium': 'Cr',
        'Cobalt': 'Co',
        'Copper': 'Cu',
        'Curium': 'Cm',
        'Darmstadtium': 'Ds',
        'Dubnium': 'Db',
        'Dysprosium': 'Dy',
        'Einsteinium': 'Es',
        'Erbium': 'Er',
        'Europium': 'Eu',
        'Fermium': 'Fm',
        'Fluorine': 'F',
        'Francium': 'Fr',
        'Gadolinium': 'Gd',
        'Gallium': 'Ga',
        'Germanium': 'Ge',
        'Gold': 'Au',
        'Hafnium': 'Hf',
        'Hassium': 'Hs',
        'Helium': 'He',
        'Holmium': 'Ho',
        'Hydrogen': 'H',
        'Indium': 'In',
        'Iodine': 'I',
        'Iridium': 'Ir',
        'Iron': 'Fe',
        'Krypton': 'Kr',
        'Lanthanum': 'La',
        'Lawrencium': 'Lr',
        'Lead': 'Pb',
        'Lithium': 'Li',
        'Lutetium': 'Lu',
        'Magnesium': 'Mg',
        'Manganese': 'Mn',
        'Meitnerium': 'Mt',
        'Mendelevium': 'Md',
        'Mercury': 'Hg',
        'Molybdenum': 'Mo',
        'Neodymium': 'Nd',
        'Neon': 'Ne',
        'Neptunium': 'Np',
        'Nickel': 'Ni',
        'Niobium': 'Nb',
        'Nitrogen': 'N',
        'Nobelium': 'No',
        'Osmium': 'Os',
        'Oxygen': 'O',
        'Palladium': 'Pd',
        'Phosphorus': 'P',
        'Platinum': 'Pt',
        'Plutonium': 'Pu',
        'Polonium': 'Po',
        'Potassium': 'K',
        'Praseodymium': 'Pr',
        'Promethium': 'Pm',
        'Protactinium': 'Pa',
        'Radium': 'Ra',
        'Radon': 'Rn',
        'Rhenium': 'Re',
        'Rhodium': 'Rh',
        'Roentgenium': 'Rg',
        'Rubidium': 'Rb',
        'Ruthenium': 'Ru',
        'Rutherfordium': 'Rf',
        'Samarium': 'Sm',
        'Scandium': 'Sc',
        'Seaborgium': 'Sg',
        'Selenium': 'Se',
        'Silicon': 'Si',
        'Silver': 'Ag',
        'Sodium': 'Na',
        'Strontium': 'Sr',
        'Sulfur': 'S',
        'Tantalum': 'Ta',
        'Technetium': 'Tc',
        'Tellurium': 'Te',
        'Terbium': 'Tb',
        'Thallium': 'Tl',
        'Thorium': 'Th',
        'Thulium': 'Tm',
        'Tin': 'Sn',
        'Titanium': 'Ti',
        'Tungsten': 'W',
        'Ununbium': 'Uub',
        'Ununhexium': 'Uuh',
        'Ununoctium': 'Uuo',
        'Ununpentium': 'Uup',
        'Ununquadium': 'Uuq',
        'Ununseptium': 'Uus',
        'Ununtrium': 'Uut',
        'Ununium': 'Uuu',
        'Uranium': 'U',
        'Vanadium': 'V',
        'Xenon': 'Xe',
        'Ytterbium': 'Yb',
        'Yttrium': 'Y',
        'Zinc': 'Zn',
        'Zirconium': 'Zr',
    }

    def group(self):
        """Return a random elemental group.

        Source: https://en.wikipedia.org/wiki/Period_(periodic_table)
        """
        # There are 18 of them.
        return 'Group {}'.format(randrange(1, 19))

    def family(self):
        """Return a random elemental family."""
        return choice([
            'Alkali Metals',
            'Alkaline Earth Metals',
            'Transition Metals',
            'Earth Metals',
            'Tetrels',
            'Pnictogens',
            'Chalcogens',
            'Halogens',
            'Noble Gases',
        ])

    def period(self):
        """Return a random elemental period.

        Source: https://en.wikipedia.org/wiki/Period_(periodic_table)
        """
        # There are 8 of them - 7 real, and 1 hypothesized.
        return 'Period {}'.format(randrange(1, 9))

    def symbol(self):
        """Return a random periodic element symbol."""
        return choice(self._elements.values())

    def element(self):
        """Return a random periodic element name."""
        return choice(self._elements.keys())

    def atomic_number(self):
        """Return a random element atomic number."""
        # There are 118 of them.
        return randrange(1, 119)
