import argparse
import sys
import wolfeutils.comparative.panseq.labelNewick
import wolfeutils.comparative.panseq.seqtools


#######################
# Create Panseq Fasta #
#######################
def createPanseqFastaArgs(args):
    parser = argparse.ArgumentParser(
        description='Create panseq-compatible fastas')
    parser.add_argument('fasta',
                        help='Fasta file to convert to panseq headers')
    parser.add_argument('--enumerate',
                        type=bool,
                        help="Just label contigs by position; don't infer contig name")
    return parser.parse_args(args)


def createPanseqFastaCli():
    args = createPanseqFastaArgs(sys.argv[1:])
    wolfeutils.comparative.panseq.seqtools.main(args.fasta, args.enumerate)


################
# Label Newick #
################
def labelNewickArgs(args):
    parser = argparse.ArgumentParser(
        description='Add otu labels to unlabeled tree as output by Panseq')
    parser.add_argument('treefile', help='Unlabeleld newick tree')
    parser.add_argument('namesfile', help='Panseq phylip_name_conversion.txt file')
    parser.add_argument('--relabeled-tree',
                        type=argparse.FileType('w'),
                        help='Relabeled tree output name (defaults to stdout)')
    return parser.parse_args(args)


def labelNewickCli():
    args = labelNewickArgs(sys.argv[1:])
    tree = wolfeutils.comparative.panseq.labelNewick.labelTree(args.treefile,
                                                               args.namesfile)
    if args.relabeled_tree:
        args.relabeled_tree.write(tree)
    else:
        print(tree)  # Default write to stdout


##########################
# PGAP Standard Analysis #
##########################
def pgapBasicAnalysisArgs(args):
    # Usage:
    # pgap_base_figures.py path/to/pgap/dir [path/to/annotated/genbanks]
    parser = argparse.ArgumentParser(
        description='Run Standard PGAP Analysis')
    parser.add_argument('pgap-dir',
                        help='PGAP Directory')
    return parser.parse_args(args)


def pgapBasicAnalysisCli():
    args = pgapBasicAnalysisArgs(sys.argv[1:])
    wolfeutils.comparative.pgap.workflows.basicAnalysis.main(args.pgap_dir)
