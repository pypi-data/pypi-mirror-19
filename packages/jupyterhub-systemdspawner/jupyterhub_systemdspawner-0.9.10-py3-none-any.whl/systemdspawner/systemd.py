"""
Perform highly constrained systemd operations only
"""
import pwd
import shlex


class Executor:
    def is_unit_running(self, unit):
        pass

    def reset_unit(self, unit):
        pass

    def start_unit(self, **kwargs):
        pass


def is_unit_failed_cmd(unit):
    pass


def reset_failed_unit(unit):
    pass


def is_unit_running_cmd(unit):
    return [
        '/bin/systemctl',
        'is-active',
        unit
    ]


def stop_unit_cmd(unit):
    return [
        '/bin/systemctl',
        'stop',
        unit
    ]

def start_unit_cmd(
    unit_name,
    username,
    env,
    singleuser_cmd,
    singleuser_args,
    workingdir,
    private_tmp,
    private_devices,
    extra_paths,
    mem_limit,
    cpu_limit,
    no_new_privs,
    readonly_paths,
    readwrite_paths,
    shell,
):

    # Make a copy of env, so we can modify it later
    env = env.copy()

    cmd = [
        '/usr/bin/systemd-run',
        '--unit', unit_name,
    ]

    # If there is no user by this name, it'll raise a KeyError
    pwnam = pwd.getpwnam(username)
    cmd.extend(['--uid', str(pwnam.pw_uid), '--gid', str(pwnam.pw_gid)])

    if private_tmp:
        cmd.append('--property=PrivateTmp=yes')

    if private_devices:
        cmd.append('--property=PrivateDevices=yes')

    if extra_paths:
        env['PATH'] = ':'.join(extra_paths) + ':' + env['PATH']

    env['SHELL'] = shell

    for key, value in env.items():
        cmd.append('--setenv={key}={value}'.format(key=key, value=value))

    if mem_limit is not None:
        cmd.extend([
            '--property=MemoryAccounting=yes',
            '--property=MemoryLimit={mem}'.format(mem=mem_limit),
        ])

    if cpu_limit is not None:
        # FIXME: Detect & use proper properties for v1 vs v2 cgroups
        # FIXME: Make sure that the kernel supports CONFIG_CFS_BANDWIDTH
        #        otherwise this doesn't have any effect.
        cmd.extend([
            '--property=CPUAccounting=yes',
            '--property=CPUQuota={quota}%'.format(quota=cpu_limit * 100)
        ])


    if no_new_privs:
        cmd.append('--property=NoNewPrivileges=yes')

    if readonly_paths is not None:
        cmd.extend([
            '--property=ReadOnlyDirectories=-{path}'.format(path=path)
            for path in readonly_paths
        ])

    if readwrite_paths is not None:
        cmd.extend([
            '--property=ReadWriteDirectories={path}'.format(path=path)
            for path in readwrite_paths
        ])

    # We unfortunately have to resort to doing cd with bash, since WorkingDirectory property
    # of systemd units can't be set for transient units via systemd-run until systemd v227.
    # Centos 7 has systemd 219, and will probably never upgrade - so we need to support them.
    bash_cmd = [
        '/bin/bash',
        '-c',
        "cd {wd} && exec {cmd} {args}".format(
            wd=shlex.quote(workingdir),
            cmd=' '.join([shlex.quote(c) for c in singleuser_cmd]),
            args=' '.join([shlex.quote(a) for a in singleuser_args])
        )
    ]
    cmd.extend(bash_cmd)

    return cmd
