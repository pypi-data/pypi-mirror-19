from intmaniac import tools

import docker

from re import compile as recomp


def get_client():
    """
    Simple wrapper for mocking later, returns a docker Client object bound
    to the local docker socker under /var/run/docker.sock.
    :return: The docker Client instance
    """
    return docker.DockerClient(base_url='unix://var/run/docker.sock', version='auto')


def create_container(image, command=None, environment={}, **kwargs):
    """
    Creates a new test container instance with the command given. Must be
    called for each command, because we can't change the command once
    it's set.
    :param image: The docker image to use
    :param command: The command to execute with the container, can be <None>
    :param environment: The environment to use in the container
    :param kwargs: keyword-arguments passed to docker.client.containers.create()
    :return: a container-object
    """
    logger = tools.get_logger(__name__+".create_container")
    dc = get_client()
    container = dc.containers.create(image,
                                     command=command,
                                     environment=environment,
                                     **kwargs)
    container_id = container.id
    logger.debug("Container id {} created (image: {}, command: {}, env: {})"
                 .format(
                         container_id[:8], image,
                         command if isinstance(command, str) else str(command),
                         str(environment)
                        )
                 )
    return container


class Compose(object):
    def __init__(self, template, project_name=None, sudo=False,
                 run_args=[], run_kwargs={}):
        project_str = " -p {}".format(project_name) if project_name else ""
        sudo_str = "sudo " if sudo else ""
        self.base_command = "{}docker-compose -f {}{}".format(
            sudo_str, template, project_str
        ).split()
        self.project_name = project_name
        self.template = template
        self.run_args = tuple(run_args)
        self.run_kwargs = run_kwargs

    def run(self, run_args, **kwargs):
        use_command = run_args \
            if isinstance(run_args, list) \
            else run_args.split(" ")
        full_command = self.base_command + use_command
        # call(*a1, *a2) seems only to work on python 3.5+
        return tools.run_command(full_command,
                                 **tools.deep_merge(self.run_kwargs, kwargs))

    def up(self, detach=True, **kwargs):
        run_args = ["up"]
        if detach:
            run_args.append("-d")
        rv = self.run(run_args, **kwargs)
        # TODO - use docker api to extract container names
        # first, set up "container_name -> service_name" tuples
        return self._extract_container_names_from(rv[3])

    def stop(self, **kwargs):
        run_args = ["stop"]
        return self.run(run_args, **kwargs)

    def kill(self, signal=None, **kwargs):
        run_args = ["kill"]
        if signal:
            run_args += ["-s", signal]
        return self.run(run_args, **kwargs)

    def rm(self, force=True, all=False, **kwargs):
        run_args = ["rm"]
        if force:
            run_args.append("-f")
        if all:
            run_args.append("--all")
        return self.run(run_args, **kwargs)

    def pull(self, ignorefailures=True, **kwargs):
        run_args = ["pull"]
        if ignorefailures:
            run_args.append("--ignore-pull-failures")
        return self.run(run_args, **kwargs)

    def _extract_container_names_from(self, outtext):
        use_prj_name = self.project_name \
            if self.project_name \
            else '[A-Za-z0-9]+'
        matcher = recomp('({}_(.+)_[0-9]+)'.format(use_prj_name))
        lines = list(map(lambda x: x.strip(), outtext.split("\n")))
        lines = list(filter(lambda x: matcher.search(x) is not None, lines))
        run_containers = []
        for line in lines:
            match = matcher.search(line)
            run_containers.append((match.groups()[0], match.groups()[1]))
        return run_containers
