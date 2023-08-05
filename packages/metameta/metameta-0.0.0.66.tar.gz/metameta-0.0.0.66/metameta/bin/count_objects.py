#! /usr/bin/env python

"""calculates gene abundance data from annotations of an assembly

Usage:

    count_objects.py [--bam] [--delimiter] [--fastr] [--normalize] [--gff3]
                     <output>

Synopsis:

    Calculates and normalizes various forms of coverage and counting.
    This includes calculating gene abundance
    BAM files
    FASTR files

Required Arguments:

    output           CSV file containing gene ID and abundance,
                     default delimiter is "\t"

Optional Arguments:

    --bam            BAM file containing alignment data
    --delimiter      the character to delimit the output file by
                     [Default: '\t']
    --fastr          FASTR file containing read depth data
    --gff3           GFF3 formatted annotation file
    --normalize      Method to calculate coverage values (see below for more
                     information on normalization) [Default: aprb]

Supported Normalization Methods:

    arpb             Average Reads Per Base: average depth coverage of each
                     base
    rpk              Reads Per Kilobase: number of reads mapping to a
                     contig divided by kilobases in the contig (contig length
                     divided by 1,000)
    rpkt             rpk times 1,000
    rpkm             rpk times 1,000,000
    rpkb             rpk times 1,000,000,000


Copyright:

    count_objects.py count various forms of biological data
    Copyright (C) 2015  Alex Hyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import division
from __future__ import print_function

import argparse
from bio_utils.iterators.gff3 import gff3_iter
from bio_utils.iterators.fastr import fastr_iter
from bio_utils.iterators.m8 import m8_iter
from bio_utils.verifiers.binary import binary_verifier
from bio_utils.verifiers.fastr import fastr_verifier
from bio_utils.verifiers.gff3 import gff3_verifier
from bio_utils.verifiers.m8 import m8_verifier
from metameta.metameta_utils.fastr_utils import decompress_fastr
from metameta.metameta_utils.output import output
import pysam
import re
import statistics
import sys


__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Inactive'
__version__ = '0.0.0.17'

def compute_gene_abundance_from_bam(bam_file, gff3_file, database,
                                    normalization, out_file):
    with open(out_file, 'a') as out_handle:
        with pysam.AlignmentFile(bam_file, 'rb') as bam_handle:
            with open(gff3_file, 'rU') as gff3_handle:
                for entry in gff3_iter(gff3_handle):
                    db_id = extract_db_id(entry['attributes'], database)
                    if int(entry['start']) > int(entry['end']):
                        start = int(entry['end']) - 1
                        end = int(entry['start']) - 1
                    else:
                        start = int(entry['start']) - 1
                        end = int(entry['end']) - 1
                    if normalization == 'arpb':
                        reads_per_base = [pileUp.n for pileUp in bam_handle.
                            pileup(entry['seq_id'], start, end)]
                        coverage = normalize(normalization,
                                             per_base_depth=reads_per_base)
                    else:
                        read_count = len([read for read in bam_handle.fetch(
                            entry['seqid'], start, end)])
                        gene_length = end - start
                        coverage = normalize(normalization,
                                             read_count=read_count,
                                             length=gene_length)
                    if db_id is not None:
                        out_handle.write('{0}\t{1}\n'.format(db_id, coverage))


def compute_gene_abundance_from_blast(blast_files, out_file):
    with open(out_file, 'w') as out_handle:
        genes = {}
        for blast_file in blast_files:
            with open(blast_file, 'rU') as blast_handle:
                for entry in m8_iter(blast_handle):
                    try:
                        assert entry['subjectID'] in genes
                    except AssertionError:
                        genes[entry['subjectID']] = {}
                    try:
                        genes[entry['subjectID']][blast_file] += 1
                    except KeyError:
                        genes[entry['subjectID']][blast_file] = 1
        # Ensure there is a number for every gene
        for gene in genes:
            for blast_file in blast_files:
                try:
                    assert blast_file in genes[gene]
                except AssertionError:
                    genes[gene][blast_file] = 0
        out_handle.write('Genes\t{0}\n'.format('\t'.join(blast_files)))
        for key in genes.keys():
            out_handle.write('{0}'.format(key))
            for blast_file in blast_files:
                out_handle.write('\t{0}'.format(str(genes[key][blast_file])))
            out_handle.write('\n')


def compute_gene_abundance_from_fastr(fastr_file, gff3_file, database,
                                      normalization, out_file):
    if normalization != 'arpb':
        message = 'FASTR files can only be used to calculate coverage as ' \
                  'Average Reads Per Base (arpb). Run this program with the' \
                  ' "--normalzie arpb" flag or use a different file type to ' \
                  'calculate coverage from.'
        output(message, 0, 0, fatal=True)
    gff3_dict = gff3_to_dict(gff3_file, database)
    with open(out_file, 'a') as out_handle:
        with open(fastr_file, 'rb') as fastr_handle:
            for entry in fastr_iter(fastr_handle):
                if entry['name'] in gff3_dict:
                    fastr_sequence = decompress_fastr(entry['sequence'])
                    coverage_sequence = [int(base) for base in
                                         fastr_sequence.split('-')]
                    if entry['name'] in gff3_dict:
                        for gene in gff3_dict[entry['name']]:
                            gene = gff3_dict[entry['name']][gene]
                            if gene['start'] < gene['end']:
                                start = int(gene['end']) - 1
                                end = int(gene['start']) - 1
                            else:
                                start = int(gene['start']) - 1
                                end = int(gene['end']) - 1
                            reads_per_base = coverage_sequence[start:end]
                            coverage = normalize(normalization,
                                                 per_base_depth=reads_per_base)
                            db_id = extract_db_id(gene['attributes'], database)
                            if db_id is not None:
                                out_handle.write('{0}\t{1}\n'.format(db_id,
                                                                 coverage))


def extract_db_id(attributes, database):
    id_regex = re.compile('{0}:.*?;'.format(database))
    search_results = re.findall(id_regex, attributes)
    if len(search_results) == 1:
        db_id = search_results[0].lstrip('{0}:'.format(database)).rstrip(';')
        return db_id
    else:
        return None


def gff3_to_dict(gff3_file, database):
    gff3_dict = {}
    with open(gff3_file, 'rU') as gff3_handle:
        for entry in gff3_iter(gff3_handle):
            db_id = extract_db_id(entry['attributes'], database)
            if db_id is None:
                continue
            elif entry['seqid'] not in gff3_dict:
                gff3_dict[entry['seqid']] = {}
            gff3_dict[entry['seqid']][db_id] = entry
    return gff3_dict


def normalization_method(method):
    acceptable_methods = ['rpkt', 'rpkm', 'rpkb', ' rpk', 'arpb']
    if method in acceptable_methods:
        return str(method)
    else:
        message = '{0} is not a supported normalization method. Supported ' \
                  'normalization methods follow:\n{1}'.format(method,
                                        '\n'.join(acceptable_methods))
        output(message, 0, 0, fatal=True)


def normalize(normalization, length=0, read_count=0,
              per_base_depth=None):
    normalized_coverage = False
    if normalization == 'read_count':
        return read_count
    elif 'rpk' in normalization:
        normalization_factor = {
            'rpk': 1,
            'rpkt': 1000,
            'rpkm': 1000000,
            'rpkb': 1000000000
        }
        normalized_coverage = (read_count / (length / 1000)) * \
                              normalization_factor[normalization]
    elif normalization_method == 'arpb':
        assert type(per_base_depth) is list
        normalized_coverage = statistics.mean(per_base_depth)
    return normalized_coverage


def split_args(arguments):
    arguments = [i.lstrip() for i in arguments.split(',')]
    return arguments


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('--gff3', metavar='GFF3',
                        default=None,
                        nargs='?',
                        help='PROKKA GFF3 file with annotations for the same'
                             + ' metagenome as the FASTA or FASTR file')
    parser.add_argument('output', metavar='out_prefix',
                        default=None,
                        nargs='?',
                        help='name of TSV file to write')
    parser.add_argument('--bam', metavar='BAM',
                        default=None,
                        nargs='?',
                        help='BAM file containing mapping data')
    parser.add_argument('--blast', metavar='BLAST Table',
                        default=None,
                        nargs='?',
                        type=split_args,
                        help='BLAST output to convert to count table')
    parser.add_argument('-d', '--database', metavar='DB',
                        default='ko',
                        help='extract hits from database "DB" [default: ko]')
    parser.add_argument('--fastr', metavar='FASTR',
                        default=None,
                        nargs='?',
                        help='FASTR file containing read depth data for a ' +
                             'metatranscriptome mapped onto a metagenome')
    parser.add_argument('-l', '--log_file', metavar='LOG',
                        default=None,
                        help='log file to print all messages to')
    parser.add_argument('--normalize', metavar='normalization method',
                        type=normalization_method,
                        default='arpb',
                        help='how to normailze data [default: arpb]')
    parser.add_argument('-v', '--verbosity',
                        action='count',
                        default=0,
                        help='increase output verbosity')
    parser.add_argument('--verify',
                        action='store_true',
                        help='verify input files before use')
    parser.add_argument('--version',
                        action='store_true',
                        help='prints tool version and exits')
    args = parser.parse_args()

    if args.version:
        print(__version__)
    elif args.fastr is None and args.bam is None and args.blast is None:
        print(__doc__)
    else:
        if args.verify:

            # Verify BAM file
            if args.bam:
                output('Verifying {0}'.format(args.bam), args.verbosity, 1,
                       log_file=args.log_file)
                with open(args.bam, 'rU') as in_handle:
                    validBam = binary_verifier(in_handle)
                bamValidity = 'valid' if validBam else 'invalid'
                output('{0} is {1}'.format(args.bam, bamValidity),
                       args.verbosity, 1, log_file=args.log_file,
                       fatal=not validBam)

            # Verify BLAST file
            if args.blast:
                output('Verifying {0}'.format(args.blast), args.verbosity, 1,
                       log_file=args.log_file)
                with open(args.blast, 'rU') as in_handle:
                    validBlast = m8_verifier(in_handle)
                blastValidity = 'valid' if validBlast else 'invalid'
                output('(0} is {1}'.format(args.blast, blastValidity),
                       args.verbosity, 1, log_file=args.log_file,
                       fatal=not blastValidity)

            # Verify FASTR file
            if args.fastr:
                output('Verifying {0}'.format(args.fastr), args.verbosity,
                       1, log_file=args.log_file)
                with open(args.fasta, 'rU') as in_handle:
                    validFastr = fastr_verifier(in_handle)
                fastrValidity = 'valid' if validFastr else 'invalid'
                output('{0} is {1}'.format(args.fastr, fastrValidity),
                       args.verbosity, 1, log_file=args.log_file,
                       fatal=not validFastr)

            # Verify GFF3 file
            output('Verifying {0}'.format(args.gff3), args.verbosity, 1,
                   log_file=args.log_file)
            with open(args.gff3, 'rU') as in_handle:
                validGff3 = gff3_verifier(in_handle)
            gff3Validity = 'valid' if validGff3 else 'invalid'
            output('{0} is {1}'.format(args.gff3, gff3Validity),
                   args.verbosity, 1, log_file=args.log_file,
                   fatal=not validGff3)

        # Main portion of program
        # Write header to output
        with open(args.output, 'w') as out_handle:
            out_handle.write('Database_ID\tCoverage_{0}\n'.format(
                args.normalize))
        if args.bam:
            message = 'Computing gene abundances from BAM ' \
                      'file {0}'.format(args.bam)
            output(message, args.verbosity, 1, log_file=args.log_file)
            compute_gene_abundance_from_bam(args.bam,
                                            args.gff3,
                                            args.database,
                                            args.normalize,
                                            args.output)
        elif args.blast:
            message = 'Computing gene abundances from BLAST ' \
                      'file {0}'.format(args.blast)
            output(message, args.verbosity, 1, log_file=args.log_file)
            compute_gene_abundance_from_blast(args.blast,
                                              args.output)
        elif args.fastr:
            message = 'Computing gene abundances from FASTR ' \
                      'file {0}'.format(args.fastr)
            output(message, args.verbosity, 1, log_file=args.log_file)
            compute_gene_abundance_from_fastr(args.fastr,
                                              args.gff3,
                                              args.database,
                                              args.normalize,
                                              args.output)
        sys.exit(0)
