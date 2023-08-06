import os
from invoke import task
from invoke.exceptions import Exit
import pip

from spynl.main.version import __version__ as spynl_version
from spynl.main.pkg_utils import  get_config_package, get_dev_config 
from cli.utils import resolve_repo_names, repo, chdir


repos_help = "Affected repos, e.g. spynl,spynl.auth. "\
             "Defaults to all installed."


@task(help={'repos': repos_help,
            'developing': 'If True (default), python setup.py develop is '
                          'used, otherwise install',
            'revision': 'Which revision to update to (default: do not update)',
            'fallbackrevision': 'Use this revision if the repository does not '
                                ' have the target revision.',
            'install-deps': 'If True (default), pre-install dependencies '
                            '(eg. via apt-get).',
            'src_path': 'Desired installation path. Defaults to '
                        '$VIRTUAL_ENV/src directory.'})
def install(ctx, repos='_all', developing=True, revision=None,
            fallbackrevision=None, install_deps=True, src_path=None):
    '''Get code and install repos in the current virtual environment.'''
    ctx.run('pip install --upgrade setuptools')  # make sure we have the latest
    src_path = src_path or os.environ['VIRTUAL_ENV'] + '/src'
    config_package = get_config_package()
    if config_package is None:
        raise Exit("No config package with ini files found.")
    config = get_dev_config() 
    if fallbackrevision is None:
        fallbackrevision = 'master' 
        if config.get('spynl.ops.scm_type', '') == 'hg':
            fallbackrevision = 'default' 
    if not os.path.exists(src_path):
        os.mkdir(src_path)
    for repo_name in resolve_repo_names(repos, complain_not_installed=False):
        repo_path = src_path + '/' + repo_name
        if not os.path.exists(repo_path):
            clone_url = 'ssh://%s@%s/%s' % (config.get('spynl.ops.scm_type'),
                                            config.get('spynl.ops.scm_team'),
                                            repo_name)
            with chdir(src_path):
                print("[spynl dev.install] CLONING from %s" % clone_url)
                ctx.run('hg clone %s' % clone_url)
        else:
            print("[spynl dev.install] UPDATING {}".format(repo_name))
            with chdir(repo_path):
                ctx.run('hg pull --update')
        with chdir(repo_path):
            if revision is not None:
                print('[spynl dev.install] Updating to revision %s ...' % revision)
                if not ctx.run('hg update {}'.format(revision), warn=True):
                    print('[spynl dev.install] Updating to fallback revision %s ...'
                          % fallbackrevision)
                    ctx.run('hg update {}'.format(fallbackrevision))
            if os.path.isfile('./setup.sh'):
                pre_cmd = './setup.sh --pre-install '\
                          '--virtualenv=%s' % os.environ['VIRTUAL_ENV']
                if install_deps:
                    pre_cmd += ' --install-dependencies'
                ctx.run(pre_cmd)
            if developing:
                print("[spynl dev.install] DEVELOPING {}".format(repo_name))
                ctx.run('python setup.py develop')
            else:
                print("[spynl dev.install] INSTALLING {}".format(repo_name))
                ctx.run('python setup.py install')
            translations(ctx, repos=repo_name, action='compile')
            if os.path.isfile('./setup.sh'):
                ctx.run('./setup.sh --post-install')


@task
def serve(ctx):
    '''Run local dev server'''
    config_package = get_config_package()
    if config_package is None:
        raise Exit("No spynl-plugin found with .ini files. Exiting ...")
    with repo('spynl'):
        ctx.run('pserve %s/development.ini --reload'
                % config_package.location, pty=True)


@task(aliases=('tests',),
      help={'repos': repos_help,
            'called-standalone': 'If False, this task is a pre-task and the '
                                 'user gets to cancel the task flow when '
                                 'tests fail.',
            'reports': 'If True, Junit and Coverage reports will be made '
                       '(requires a few extra packages, '
                       'e.g. for pycoverage).'})
def test(ctx, repos='_all', called_standalone=True, reports=False):
    '''
    Perfom tests in one or more spynl plugins.
    '''
    for repo_name in resolve_repo_names(repos):
        print("[spynl dev.test] Testing repo: {}".format(repo_name))
        with repo(repo_name):
            if not reports:
                result = ctx.run('py.test', warn=True)
            else:
                result = ctx.run('py.test --junit-xml=pytests.xml --cov %s '
                                 ' --cov-report xml --cov-append' % repo_name)
            if not result.ok and called_standalone is False\
               and input("[spynl dev.test] Tests failed. Continue anyway? Y/n") not in ('y', 'Y'):
                raise Exit("[spynl dev.test] Aborting at user request.")


@task(help={'repos': repos_help,
            'languages': 'An iterable of language codes. Defaults to ("nl",).',
            'action': 'Either "compile" (compile selected languages) or '
                      '"refresh" (extract messages from the source code '
                      'and update the .po files for the selected languages). '
                      'Defaults to compile.'})
def translations(ctx, repos='_all', languages=('nl',), action='compile'):
    '''
    Ensure that translations files are up-to-date w.r.t. to the code. If action
    is set to compile (default), this will compile the catalogs for all selected
    languages. If action is set to refresh, this will extract messages from the
    source code and update the .po files for the selected languages (will
    initialize if necessary).
    '''
    if action == 'compile':
        refresh = False
    elif action == 'refresh':
        refresh = True
    else:
        raise Exit("[spynl dev.translations] action should be 'compile' or "
                   "'refresh'.")

    for repo_name in resolve_repo_names(repos):
        with repo(repo_name):
            if repo_name == 'spynl':
                repo_name = 'spynl.main'
            print("[spynl dev.translations] Repo: %s ..." % repo_name)
            repo_path = repo_name.replace('.', '/')
            # make locale folder if it doesn't exist already:
            if not os.path.exists('%s/locale' % repo_path):
                os.mkdir('./%s/locale' % repo_path)
            if refresh:
                # Extract messages from source:
                ctx.run('python setup.py extract_messages '
                        '--output-file {rp}/locale/messages.pot --no-wrap '
                        '--sort-by-file --input-dirs {rp} --project {project} '
                        '--copyright-holder "Softwear BV" --version {v}'
                        .format(rp=repo_path, project=repo_name,
                                v=spynl_version))
            for lang in languages:
                path2po = '%s/locale/%s/LC_MESSAGES/%s.po' % (repo_path, lang,
                                                              repo_name)
                # update if refresh
                if refresh:
                    # init if needed:
                    if not os.path.exists(path2po):
                        print('[spynl dev.translations] File %s does not exist.'
                              ' Initializing.' % path2po)
                        ctx.run('python setup.py init_catalog -l {lang} '
                                '-i {rp}/locale/messages.pot '
                                '-d {rp}/locale -D {rn}'
                                .format(rp=repo_path, rn=repo_name, lang=lang))
                    # update if not init
                    else:
                        print('[spynl dev.translations] update the %s catalog'
                              % lang)
                        ctx.run('python setup.py update_catalog -N --no-wrap '
                                '-l {lang} -i {rp}/locale/messages.pot '
                                '-d {rp}/locale -D {rn}'
                                .format(rp=repo_path, rn=repo_name, lang=lang))
                # if not refresh, compile
                elif os.path.exists(path2po):
                    ctx.run('python setup.py compile_catalog --domain {rn} '
                            '--directory {rp}/locale --domain {rn} '
                            '--locale {lang}'
                            .format(rp=repo_path, rn=repo_name, lang=lang))
                else:
                    print('[spynl dev.translations] File %s does not exist.'
                          ' Update the repo first.' % path2po)

                print("[spynl dev.translations] Done with language %s." % lang)
                print("--------------------------------------------------")
