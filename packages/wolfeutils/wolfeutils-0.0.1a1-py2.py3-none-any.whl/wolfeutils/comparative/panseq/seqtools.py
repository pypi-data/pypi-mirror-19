import os
import pandas as pd
import re
import sys


def main(infasta, outname=None, enumerate=False):
    '''Create panseq-compatibile fasta Headers

    Take FASTA files named just by contig and clean them up.
    Instead of mucking around with regular expressions, just recreate the
    header to be sure it will be clean. Also check! for invalid characters.

    By default, search for "contig_XX" in the header line, and assign that
    contig number to stay consistent with the orignal. Alternatively, use
    --enumerate to simply wipe out the old contig labels and write new ones.

    A new mapping file contigMap.csv is written either way mapping from the old
    label to the onew.
    '''
    # Read FASTA
    with open(infasta, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    # Split Filename
    base = os.path.basename(infasta)
    base, ext = os.path.splitext(base)

    invalid = re.compile("[^\w]")

    if outname:
        outHandle = open(outname, 'w')
    else:
        outHandle = sys.stdout

    contigN = 0  # Header lines seen
    contigMap = []

    # Write Lines or Cleaned Headers
    for line in lines:
        l = line
        if line[0] == '>':
            if not enumerate:
                # Determine the correct contig for label
                match = re.search('contig_?(\d*)', line, flags=re.IGNORECASE)
                if match:
                    contignum = int(match.groups()[0])
                else:
                    raise StandardError('Unrecognized contig number for %s' % l)
                if invalid.search(l.split('|')[2]):
                    raise StandardError('Invalid Space in %s' % l)

                l = '>lcl|%s|contig_%d' % (base, contignum)
            else:
                # Just label contigs by position
                contigN += 1
                l = '|'.join(['>lcl', base.replace('.', '_'),
                              'contig_%s' % contigN])
            contigMap.append({'new': l, 'original': line})

        outHandle.write('%s\n' % l)
    pd.DataFrame(contigMap).to_csv('contigMap.csv')
