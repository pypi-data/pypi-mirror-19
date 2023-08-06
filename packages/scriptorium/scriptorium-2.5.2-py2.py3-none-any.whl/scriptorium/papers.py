#!/usr/bin/env python
"""Paper oriented operations."""

import glob
import subprocess
import re
import os
import shutil
import platform
import tempfile
import mmap

import pymmd

import scriptorium

def _list_files(dname):
    """Builds list of all files which could be converted via MultiMarkdown."""
    fexts = ['mmd', 'md', 'txt']
    return [ii for jj in fexts for ii in glob.glob(os.path.join(dname, '*.' + jj))]

def paper_root(dname):
    """Given a directory, finds the root document for the paper."""
    root_doc = None

    for fname in _list_files(dname):
        #Template metadata only exists in root
        if get_template(fname):
            root_doc = fname
            break

    return os.path.basename(root_doc) if root_doc else None

def _get_template(txt):
    """Extract template name from string containing document text"""
    template = pymmd.value(txt, 'latexfooter', pymmd.COMPLETE)
    template_re = re.compile(r'(?P<template>[a-zA-Z0-9._]*)\/footer.tex')

    match = template_re.search(template)

    return match.group('template') if match else None

def get_template(fname):
    """Attempts to find the template of a paper in a given file."""
    with open(fname, 'Ur') as mmd_fp:
        mm = mmap.mmap(mmd_fp.fileno(), 0, prot=mmap.PROT_READ)
        blank_line = '\n\n'
        idx = mm.find(bytearray(blank_line, 'utf-8'))
        if idx == -1:
            return None
        mm.seek(0)
        frontmatter = mm.read(idx).decode('utf-8')
        return _get_template(frontmatter)

def to_pdf(paper_dir, template_dir=None, use_shell_escape=False, flatten=False):
    """Build paper in the given directory, returning the PDF filename if successful."""
    template_dir = template_dir or scriptorium.CONFIG['TEMPLATE_DIR']

    paper_dir = os.path.abspath(paper_dir)
    if os.path.isdir(paper_dir):
        fname = paper_root(paper_dir)
    elif os.path.isfile(paper_dir):
        fname = paper_dir
        paper_dir = os.path.dirname(paper_dir)
    else:
        raise IOError("{0} is not a valid directory".format(paper_dir))

    old_cwd = os.getcwd()
    if old_cwd != paper_dir:
        os.chdir(paper_dir)

    if not fname:
        raise IOError("{0} has no obvious root.".format(paper_dir))

    #Convert all auxillary MMD files to LaTeX
    for mmd in _list_files(paper_dir):
        bname = os.path.basename(mmd).split('.')[0]
        tname = '{0}.tex'.format(bname)
        with open(mmd, 'Ur') as mmd_fp, open(tname, 'w') as tex_fp:
            txt = pymmd.convert(mmd_fp.read(), fmt=pymmd.LATEX, dname=mmd, ext=pymmd.SMART)
            tex_fp.write(txt)

    bname = os.path.basename(fname).split('.')[0]
    tname = '{0}.tex'.format(bname)

    template = get_template(fname)
    if not template:
        raise IOError('{0} does not appear to have lines necessary to load a template.'.format(fname))

    template_loc = scriptorium.find_template(template, template_dir)

    if not template_loc:
        raise IOError('{0} template not installed in {1}'.format(template, template_dir))

    template_loc = os.path.abspath(os.path.join(template_loc, '..'))

    #Need to set up environment here
    new_env = dict(os.environ)
    old_inputs = new_env.get('TEXINPUTS')
    texinputs = './:{0}:{1}'.format(template_loc + '/.//', old_inputs + ':' if old_inputs else '')
    new_env['TEXINPUTS'] = texinputs

    if flatten:
        with tempfile.NamedTemporaryFile() as tmp:
            subprocess.check_call(['latexpand', '-o', tmp.name, tname], env=new_env)
            shutil.copyfile(tmp.name, tname)

    pdf_cmd = [scriptorium.CONFIG['LATEX_CMD'], '-halt-on-error', '-interaction=nonstopmode', tname]

    if platform.system() == 'Windows':
        pdf_cmd.insert(-2, '-include-directory={0}'.format(template_loc))

    if use_shell_escape:
        pdf_cmd.insert(1, '-shell-escape')
    try:
        subprocess.check_output(pdf_cmd, env=new_env, universal_newlines=True).encode('utf-8')
    except subprocess.CalledProcessError as exc:
        raise IOError(exc.output)

    try:
        auxname = '{0}.aux'.format(bname)
        #Check if bibtex is defined in the frontmatter
        bibtex_re = re.compile(r'^bibtex:', re.MULTILINE)
        with open(fname, 'Ur') as paper_fp:
            if bibtex_re.search(paper_fp.read()):
                biber_re = re.compile(r'\\bibdata', re.MULTILINE)
                full = open(auxname, 'Ur').read()
                if biber_re.search(full):
                    subprocess.check_output(['bibtex', auxname], universal_newlines=True)
                else:
                    subprocess.check_output(['biber', bname], universal_newlines=True)

                subprocess.check_output(pdf_cmd, env=new_env, universal_newlines=True)
                subprocess.check_output(pdf_cmd, env=new_env, universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        raise IOError(exc.output)

    # Revert working directory
    if os.getcwd() != old_cwd:
        os.chdir(old_cwd)

    return os.path.join(paper_dir, '{0}.pdf'.format(bname))

def create(paper_dir, template, force=False, use_git=True, config=None):
    """Create folder with paper skeleton.
    Returns a list of unpopulated variables if successfully created.
    """
    if os.path.exists(paper_dir) and not force:
        raise IOError('{0} exists'.format(paper_dir))

    template_dir = scriptorium.find_template(template, scriptorium.CONFIG['TEMPLATE_DIR'])

    os.makedirs(paper_dir)
    if use_git and not os.path.exists(os.path.join(paper_dir, '.gitignore')):
        shutil.copyfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data',
                                     'gitignore'),
                        os.path.join(paper_dir, '.gitignore'))

    files = scriptorium.get_manifest(template)
    texts = {}
    for ofile, ifile in files.items():
        ifile = os.path.join(template_dir, ifile)
        try:
            with open(ifile, 'Ur') as ifp:
                texts[ofile] = ifp.read()
        except IOError:
            texts[ofile] = ''

    #Inject template as macro argument
    config['TEMPLATE'] = template
    full_config = scriptorium.get_default_config(template)
    full_config.update(config)
    #One line regex thanks to http://stackoverflow.com/a/6117124/59184
    for ofile, text in texts.items():
        texts[ofile] = re.sub("|".join([r'\${0}'.format(ii) for ii in full_config]),
                              lambda m: full_config[m.group(0)[1:]], text)

    #Regex to find variable names
    var_re = re.compile(r'\$[A-Z0-9_\.\-]+')
    unset_vars = set()
    for ofile, text in texts.items():
        unset_vars |= set([ii.group(0) for ii in var_re.finditer(text)])
        with open(os.path.join(paper_dir, ofile), 'w') as ofp:
            ofp.write(text)

    return unset_vars
