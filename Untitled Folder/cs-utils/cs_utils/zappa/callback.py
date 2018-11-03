import sys
import os
from subprocess import Popen, PIPE, STDOUT


def checkout_to_master():
    cmd = 'git checkout master'
    p = Popen(
        cmd,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        close_fds=True
    )
    p.wait()
    return p.stdout.read().decode('utf-8')


def check_virtualenv_name():
    cmd = 'which python'
    p = Popen(
        cmd,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        close_fds=True
    )
    p.wait()
    return p.stdout.read().decode('utf-8')


def check_develop_mode():
    cmd = 'pip freeze'
    p = Popen(
        cmd,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        close_fds=True
    )
    p.wait()
    return p.stdout.read().decode('utf-8')


def change_develop_mode(dir, venv):
    cs_utils_dir = dir
    result = check_cs_utils_venv(cs_utils_dir)
    if venv in result:
        cmd = 'python setup.py develop --uninstall;python setup.py install'
    else:
        cmd = 'source ~/.virtualenv/' + venv +'/bin/activate;python setup.py develop --uninstall;python setup.py install'
    p = Popen(
        cmd,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        close_fds=True,
        cwd=dir
    )
    p.wait()
    return p.stdout.read().decode('utf-8')


def check_install_mode(dir, venv):
    cs_utils_dir = dir
    result = check_cs_utils_venv(cs_utils_dir)
    if venv in result:
        cmd = 'pip freeze'
    else:
        cmd = 'source ~/.virtualenv/' + venv + '/bin/activate;pip freeze'
    p = Popen(
        cmd,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        close_fds=True,
        cwd=dir
    )
    p.wait()
    return p.stdout.read().decode('utf-8')


def check_cs_utils_venv(dir):
    cmd = 'which python'
    p = Popen(
        cmd,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        close_fds=True,
        cwd=dir
    )
    p.wait()
    return p.stdout.read().decode('utf-8')


def get_cs_utils_dir():
    # cmd = "find ~/ -not -path '*/\.*' -type d -name cs-utils"
    cmd = 'cd ..;cd cs-utils/;pwd'
    p = Popen(
        cmd,
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        close_fds=True
    )
    p.wait()
    return p.stdout.read().decode('utf-8')


def settings_callback(self):
    zappa_command = self.command
    if (zappa_command in ['update', 'dev'] and
            not os.environ.get('CODEBUILD_BUILD_IMAGE')):
        output = check_virtualenv_name()
        current_venv = self.zappa.get_current_venv()

        project_name = self.stage_config.get('project_name')
        venv_name = project_name + '-service'
        if current_venv in output and venv_name in current_venv and venv_name in output :
            print('********** virtualenv: CORRECT VIRTUALENV  **********')
        else:
            print('**** error: CHECK YOUR VIRTUALENV NAME OR SETTINGS ****')
            sys.exit(1)
        cs_utils_directory = get_cs_utils_dir()
        dir_name = cs_utils_directory[:cs_utils_directory.find("\n")]
        if '/cs-utils' in dir_name:
            install_mode = check_install_mode(dir_name, current_venv)
            if 'cs-utils==0.1' in install_mode:
                print('***** SUCCESS: ALREADY IN INSTALL MODE  ******')
            else:
                mode_output = check_develop_mode()
                mode_check = 'egg=cs_utils'
                if mode_check in mode_output:
                    print('**** WAIT: removing the develop mode for cs-utils ****')
                    undevep_result = change_develop_mode(dir_name, current_venv)
                    check_develop = 'Removing cs-utils'
                    if check_develop in undevep_result:
                        print('****** SUCCESS: REMOVED DEVELOP MODE  ******')
                    else:
                        print('**** error: PLEASE CHECK MANUALLY  ****')
                        sys.exit(1)
                else:
                    print('**** error: PLEASE CHECK MANUALLY  ****')
                    sys.exit(1)
        else:
            print('**** ERROR: cs_utils DIR AND YOUR PROJECT DIRECTORY SHOULD BE AT SAME LEVEL  ****')
            sys.exit(1)

        result = checkout_to_master()
        output1 = "Switched to branch 'master'"
        output2 = "Already on 'master'"
        if output1 in result:
            print('********** Git branch: ' + output1 + ' **********')
        elif output2 in result:
            print('********** Git branch: ' + output2 + ' **********')
        else:
            print('********** error: BRANCH IS NOT UPDATED **********')
            sys.exit(1)
