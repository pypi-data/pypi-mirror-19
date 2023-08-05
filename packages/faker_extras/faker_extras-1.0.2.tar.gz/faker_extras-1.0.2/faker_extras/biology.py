"""Faker data providers for biological data."""

from random import choice

from faker.providers import BaseProvider

from . import utils


class GeneticProvider(BaseProvider):
    """Genomic data provider.

    Acid data source:
    http://www.cryst.bbk.ac.uk/education/AminoAcid/the_twenty.html
    """

    acids = {
        'alanine': 'ala',
        'arginine': 'arg',
        'asparagine': 'asn',
        'aspartic acid': 'asp',
        'cysteine': 'cys',
        'glutamine': 'gln',
        'glutamic acid': 'glu',
        'glycine': 'gly',
        'histidine': 'his',
        'isoleucine': 'ile',
        'leucine': 'leu',
        'lysine': 'lys',
        'methionine': 'met',
        'phenylalanine': 'phe',
        'proline': 'pro',
        'serine': 'ser',
        'threonine': 'thr',
        'tryptophan': 'trp',
        'tyrosine': 'tyr',
        'valine': 'val',
    }

    def amino_acid_group(self):
        """Return an amino acid group."""
        return choice([
            'Aliphatic',
            'Aromatic',
            'Acidic',
            'Basic',
            'Hydroxylic',
            'Sulphur-containing',
            'Amidic',
        ])

    def amino_acid(self, symbol=True):
        """Return a random amino symbol or acid."""
        if symbol:
            vals = self.acids.keys()
            return choice(vals)
        return choice(self.acids.keys())

    def rna(self):
        """Return some RNA sequence.

        >>> rna()
        >>> AAACUAGCUG
        """
        return utils._choice_str(['U', 'C', 'G', 'A'], 10)

    def dna(self):
        """Return some DNA sequence.

        >>> dna()
        >>> CTATAGAGCT
        """
        return utils._choice_str(['T', 'C', 'G', 'A'], 10)
