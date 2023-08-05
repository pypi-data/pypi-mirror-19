import argparse
import os
import sys

import pystache

from .parse_fchk import alpha_electrons_number, beta_electrons_number

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('fchk')
    parser.add_argument('window', help='How many orbitals to explore below HOMO')
    parser.add_argument('-p', '--points', default=60, help='how many points along each direction for the cube file')
    args = parser.parse_args()

    alpha_homo_n = alpha_electrons_number(args.fchk)
    beta_homo_n = beta_electrons_number(args.fchk)

    if int(args.window) >= alpha_homo_n:
        raise Exception('You requested to generate cube files down to level HOMO-{} for alpha MOs, but the lowest'
                        ' alpha orbital is HOMO-{}'.format(args.window, alpha_homo_n-1))
        sys.exit(1)

    if int(args.window) >= beta_homo_n:
        raise Exception('You requested to generate cube files down to level HOMO-{} for beta MOs, but the lowest'
                        ' beta orbital is HOMO-{}'.format(args.window, beta_homo_n-1))
        sys.exit(1)

    alpha = {'spin': 'alpha', 'spin_abbreviation': 'a', 'points': args.points, 'fchk': args.fchk,
             'template': 'job-template-alpha.txt', 'homo_n': alpha_homo_n, 'window': int(args.window)}
    beta = {'spin': 'beta', 'spin_abbreviation': 'b', 'points': args.points, 'fchk': args.fchk,
            'template': 'job-template-beta.txt', 'homo_n': beta_homo_n, 'window': int(args.window)}

    create_jobs(alpha)
    create_jobs(beta)
    # submit-all.sh created by create_jobs

def create_jobs(orbitals_info):
    here_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here_dir, 'job-header.txt'), 'rt') as f:
        header = f.read()
    with open(os.path.join(here_dir, 'submit-template.txt'), 'rt') as f:
        submit_template = f.read()
    with open(os.path.join(os.getcwd(), 'submit-all.sh'), 'at') as submit_f:
        for i in range(0, orbitals_info['window']+1):
            orbital_n = window_to_orbital_number(i, orbitals_info['homo_n'])
            cube_fname = cube_filename(orbitals_info['spin'], i)

            config = {'cube_filename': cube_fname, 'orbital_n': orbital_n, 'header': header}
            config.update(orbitals_info)

            job_text = render_template(os.path.join(here_dir, orbitals_info['template']), config)
            job_fname = job_filename(orbitals_info['spin'], i)

            with open(os.path.join(os.getcwd(), job_fname), 'wt') as f:
                f.write(job_text)

            submit_line = pystache.render(submit_template,
                                          {'homo_distance': i,
                                           'spin_abbreviation': orbitals_info['spin_abbreviation'],
                                           'job': job_fname
                                           })
            submit_f.write(submit_line)
            submit_f.write('\n')


def job_filename(spin, homo_distance):
    return "job-{}-homo-{}.sh".format(spin, homo_distance)

def cube_filename(spin, homo_distance):
    """Return the filename for the job

    Args:
        spin (str): alpha or beta
        homo_distance (int)

    """
    if homo_distance == 0:
        return "homo.{}.cube".format(spin)
    return "homo-{}.{}.cube".format(homo_distance, spin)


def window_to_orbital_number(window, homo):
    """

    Args:
        window (int): how many levels below HOMO
        homo (int): the number of HOMO

    Returns:
        orbital_number (int): the absolute number of orbital HOMO-window
    """
    return homo - window


def render_template(template_path, args):
    """Return str of rendered template"""
    with open(template_path, 'rt') as f:
        text = f.read()
    return pystache.render(text, context=args)