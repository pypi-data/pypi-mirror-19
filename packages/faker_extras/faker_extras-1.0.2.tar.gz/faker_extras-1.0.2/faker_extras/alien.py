"""Faker data providers for alien like data."""

from random import choice, randrange

from faker.providers import BaseProvider


class AlienProvider(BaseProvider):
    """Provide alien data."""

    cons = list('bcdfghjklmnpqrstuvwxyz')
    vowl = list('aeiou')

    def alien_species(self, capitalize=False):
        """Generate an alien species.

        Names from: http://www.ufos-aliens.co.uk/cosmicspecies.htm
        """
        names = [
            'agharians',
            'alpha-draconians',
            'altairians',
            'amphibians',
            'anakim',
            'antarctican',
            'atlans',
            'bernarians',
            'booteans',
            'burrowers',
            'chameleon',
            'chupacabra',
            'draco-borgs',
            'dragonworms',
            'dwarfs',
            'eva-borgs',
            'orgizahn',
            'grails',
            'greens,the',
            'greys,the',
            'tau-cetians',
        ]
        name = choice(names)
        if capitalize:
            name[0] = name[0].upper()
        return name

    def alien_name(self):
        """Return an alien name."""
        vowel_count = randrange(1, 3)

        def atom_lg():
            return '{c1}{v1}{c2}{c3}{v2}{c4}'.format(
                c1=choice(self.cons).upper(),
                v1=choice(self.vowl) * vowel_count,
                c2=choice(self.cons),
                c3=choice(self.cons),
                v2=choice(self.vowl),
                c4=choice(self.cons),
            )

        def atom_med():
            return '{c1}{v1}{c2}{c3}{v2}'.format(
                c1=choice(self.cons).upper(),
                v1=choice(self.vowl) * vowel_count,
                c2=choice(self.cons),
                c3=choice(self.cons),
                v2=choice(self.vowl),
            )

        def atom_sm():
            return '{c1}{v1}{c2}'.format(
                c1=choice(self.cons).upper(),
                v1=choice(self.vowl) * vowel_count,
                c2=choice(self.cons),
            )

        funcs = [atom_lg, atom_med, atom_sm]
        fst, sec, thrd = choice(funcs), choice(funcs), choice(funcs)
        tokens = ['-', '\'', ' ']
        token = choice(tokens)
        return '{}{token}{} {}'.format(fst(), sec(), thrd(), token=token)
