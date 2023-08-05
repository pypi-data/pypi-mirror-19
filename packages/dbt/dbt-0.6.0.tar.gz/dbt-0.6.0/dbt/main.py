
from dbt.logger import getLogger

import argparse
import os.path
import sys
import re

import dbt.version
import dbt.project as project
import dbt.task.run as run_task
import dbt.task.compile as compile_task
import dbt.task.debug as debug_task
import dbt.task.clean as clean_task
import dbt.task.deps as deps_task
import dbt.task.init as init_task
import dbt.task.seed as seed_task
import dbt.task.test as test_task
import dbt.task.archive as archive_task
import dbt.tracking


def is_opted_out(profiles_dir):
    profiles = project.read_profiles(profiles_dir)

    if profiles is None or profiles.get("config") is None:
        return False
    elif profiles['config'].get("send_anonymous_usage_stats") == False:
        return True
    else:
        return False

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    try:
        return handle(args)

    except RuntimeError as e:
        print("Encountered an error:")
        print(str(e))
        sys.exit(1)

def handle(args):
    parsed = parse_args(args)

    # this needs to happen after args are parsed so we can determine the correct profiles.yml file
    if is_opted_out(parsed.profiles_dir):
        dbt.tracking.do_not_track()

    res = run_from_args(parsed)
    dbt.tracking.flush()

    return res

def get_nearest_project_dir():
    root_path = os.path.abspath(os.sep)
    cwd = os.getcwd()

    while cwd != root_path:
        project_file = os.path.join(cwd, "dbt_project.yml")
        if os.path.exists(project_file):
            return cwd
        cwd = os.path.dirname(cwd)

    return None

def run_from_args(parsed):
    task = None
    proj = None

    if parsed.which == 'init':
        # bypass looking for a project file if we're running `dbt init`
        task = parsed.cls(args=parsed)
    else:

        nearest_project_dir = get_nearest_project_dir()

        if nearest_project_dir is None:
            raise RuntimeError("fatal: Not a dbt project (or any of the parent directories). Missing dbt_project.yml file")

        os.chdir(nearest_project_dir)

        res = invoke_dbt(parsed)
        if res is None:
            raise RuntimeError("Could not run dbt")
        else:
            task, proj = res

    dbt.tracking.track_invocation_start(project=proj, args=parsed)
    try:
        return task.run()
        dbt.tracking.track_invocation_end(project=proj, args=parsed, result_type="ok", result=None)
    except Exception as e:
        dbt.tracking.track_invocation_end(project=proj, args=parsed, result_type="error", result=str(e))
        raise

def invoke_dbt(parsed):
    task = None
    proj = None

    try:
        proj = project.read_project('dbt_project.yml', parsed.profiles_dir, validate=False, profile_to_load=parsed.profile)
        proj.validate()
    except project.DbtProjectError as e:
        print("Encountered an error while reading the project:")
        print("  ERROR {}".format(str(e)))
        print("Did you set the correct --profile? Using: {}".format(parsed.profile))
        all_profiles = project.read_profiles(parsed.profiles_dir).keys()
        profiles_string = "\n".join([" - " + key for key in all_profiles])
        print("Valid profiles:\n{}".format(profiles_string))
        dbt.tracking.track_invalid_invocation(project=proj, args=parsed, result_type="invalid_profile", result=str(e))
        return None

    if parsed.target is not None:
        targets = proj.cfg.get('outputs', {}).keys()
        if parsed.target in targets:
            proj.cfg['target'] = parsed.target
        else:
            print("Encountered an error while reading the project:")
            print("  ERROR Specified target {} is not a valid option for profile {}".format(parsed.target, proj.profile_to_load))
            print("Valid targets are: {}".format(targets))
            dbt.tracking.track_invalid_invocation(project=proj, args=parsed, result_type="invalid_target", result="target not found")
            return None

    log_dir = proj.get('log-path', 'logs')
    logger = getLogger(log_dir, __name__)

    logger.info("running dbt with arguments %s", parsed)

    task = parsed.cls(args=parsed, project=proj)

    return task, proj

def parse_args(args):
    p = argparse.ArgumentParser(prog='dbt: data build tool', formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('--version', action='version', version=dbt.version.get_version_information(), help="Show version information")
    subs = p.add_subparsers()

    base_subparser = argparse.ArgumentParser(add_help=False)
    base_subparser.add_argument('--profiles-dir', default=project.default_profiles_dir, type=str, help='Which dir to look in for the profiles.yml file. Default = {}'.format(project.default_profiles_dir))
    base_subparser.add_argument('--profile', required=False, type=str, help='Which profile to load (overrides profile setting in dbt_project.yml file)')
    base_subparser.add_argument('--target', default=None, type=str, help='Which target to load for the given profile')

    sub = subs.add_parser('init', parents=[base_subparser])
    sub.add_argument('project_name', type=str, help='Name of the new project')
    sub.set_defaults(cls=init_task.InitTask, which='init')

    sub = subs.add_parser('clean', parents=[base_subparser])
    sub.set_defaults(cls=clean_task.CleanTask, which='clean')

    sub = subs.add_parser('compile', parents=[base_subparser])
    sub.add_argument('--dry', action='store_true', help="Compile 'dry run' models")
    sub.add_argument('--non-destructive', action='store_true', help="If specified, DBT will not drop views. Tables will be truncated instead of dropped. ")
    sub.add_argument('--full-refresh', action='store_true', help="If specified, DBT will drop incremental models and fully-recalculate the incremental table from the model definition.")
    sub.set_defaults(cls=compile_task.CompileTask, which='compile')

    sub = subs.add_parser('debug', parents=[base_subparser])
    sub.set_defaults(cls=debug_task.DebugTask, which='debug')

    sub = subs.add_parser('deps', parents=[base_subparser])
    sub.set_defaults(cls=deps_task.DepsTask, which='deps')

    sub = subs.add_parser('archive', parents=[base_subparser])
    sub.add_argument('--threads', type=int, required=False, help="Specify number of threads to use while archiving tables. Overrides settings in profiles.yml")
    sub.set_defaults(cls=archive_task.ArchiveTask, which='archive')

    sub = subs.add_parser('run', parents=[base_subparser])
    sub.add_argument('--dry', action='store_true', help="'dry run' models")
    sub.add_argument('--models', required=False, nargs='+', help="Specify the models to run. All models depending on these models will also be run")
    sub.add_argument('--threads', type=int, required=False, help="Specify number of threads to use while executing models. Overrides settings in profiles.yml")
    sub.add_argument('--non-destructive', action='store_true', help="If specified, DBT will not drop views. Tables will be truncated instead of dropped. ")
    sub.add_argument('--full-refresh', action='store_true', help="If specified, DBT will drop incremental models and fully-recalculate the incremental table from the model definition.")
    sub.set_defaults(cls=run_task.RunTask, which='run')

    sub = subs.add_parser('seed', parents=[base_subparser])
    sub.add_argument('--drop-existing', action='store_true', help="Drop existing seed tables and recreate them")
    sub.set_defaults(cls=seed_task.SeedTask, which='seed')

    sub = subs.add_parser('test', parents=[base_subparser])
    sub.add_argument('--data', action='store_true', help='Run data tests defined in "tests" directory')
    sub.add_argument('--schema', action='store_true', help='Run constraint validations from schema.yml files')
    sub.add_argument('--threads', type=int, required=False, help="Specify number of threads to use while executing tests. Overrides settings in profiles.yml")
    sub.set_defaults(cls=test_task.TestTask, which='test')

    if len(args) == 0: return p.print_help()

    parsed = p.parse_args(args)
    return parsed
