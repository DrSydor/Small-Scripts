"""
This script takes in a spreadsheet of raw CRISPR guides from CHOPCHOP and
returns a forward and reverse sequences with the proper alterations needed
for work in the lab's CRISPR workflow.
"""

from Bio.Seq import Seq
import pandas as pd

def CRISPR_seq_mod(oligo_seq):
    '''
    This function takes in an oligo string and then adds on the required
    bases to allow it to be used in our lab's CRISPR cloning strategy. It also
    creates the reverse complement.

    Parameters
    ----------
    oligo_seq : STRING
        A string containing the raw CRISPR guide sequence from CHOPCHOP

    Returns
    -------
    The modified forward and reverse oligo sequences, for_seq and rev_seq.

    '''
    oligo_seq = oligo_seq.upper() #ensure entire string is uppercase

    oligo_last3_rem = oligo_seq[:-3] # remove last three bases (NGG motif)

    oligo_last3_rem_org = oligo_last3_rem # make a copy so we can save over the original string yet still use the original for a check below

    if oligo_last3_rem[0] != 'G':
        oligo_last3_rem = 'G' + oligo_last3_rem # Add one more 'G' if first base is not 'G'

    oligo_rev = Seq(oligo_last3_rem).reverse_complement()

    for_seq = 'CACC' + oligo_last3_rem
    rev_seq = 'AAAC' + oligo_rev

    if oligo_last3_rem_org[0] != 'G': # if a 'G' was added above, we need to add a 'C' to the reverse complement's 3' end.
        rev_seq = rev_seq + 'C'

    return for_seq, rev_seq

df = pd.read_excel('CRISPR Primer Design- raw sequences.xlsx') # Change filename appropriately

df['for_seq'] = df.apply(lambda row:CRISPR_seq_mod(row['Raw_seq'])[0], axis = 1)
df['rev_seq'] = df.apply(lambda row:CRISPR_seq_mod(row['Raw_seq'])[1], axis = 1)

df.to_excel("CRISPR Primer Design- final edited sequences.xlsx")
