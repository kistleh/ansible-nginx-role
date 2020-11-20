"""Role testing files using testinfra."""

import os
import re
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_nginx_is_installed(host):
    nginx = host.package("nginx")

    assert nginx.is_installed


def test_nginx_is_running_and_enabled(host):
    nginx = host.service("nginx")

    assert nginx.is_running
    assert nginx.is_enabled


def test_nginx_configuration(host):
    dist = host.system_info.distribution
    nginx = host.file("/etc/nginx/nginx.conf")
    content = nginx.content_string

    assert nginx.exists
    assert nginx.is_file
    assert nginx.user == "root"
    assert nginx.group == "root"

    if dist == "centos":
        # String match
        assert nginx.contains("user nginx;")

        # Regular expression
        assert re.search(r'^user\s+nginx;$', content, re.MULTILINE)
        assert re.search(r'^include\s+/usr/share/nginx/modules/\*\.conf;$',
                         content, re.MULTILINE)
    elif dist == "ubuntu":
        # String match
        assert nginx.contains("user www-data;")

        # Regular expression
        assert re.search(r'^user\s+www-data;$', content, re.MULTILINE)
        assert re.search(r'^include\s+/etc/nginx/modules-enabled/\*\.conf;$',
                         content, re.MULTILINE)


def test_nginx_default_site(host):
    dist = host.system_info.distribution
    with host.sudo():
        nginx = host.file("/etc/nginx/conf.d/default.conf")
        content = nginx.content_string

    assert nginx.exists
    assert nginx.is_file
    assert nginx.mode == 0o640

    if dist == "centos":
        assert nginx.user == "nginx"
        assert nginx.group == "nginx"
    elif dist == "ubuntu":
        assert nginx.user == "www-data"
        assert nginx.group == "www-data"

    assert re.search(r'^\s+root\s+/var/www;$', content, re.MULTILINE)


def test_nginx_listens(host):
    request = host.ansible("uri",
                           "url=http://localhost:80 return_content=true",
                           check=False)

    assert host.socket("tcp://0.0.0.0:80").is_listening
    assert request["status"] == 200

    # The long way
    dist = host.system_info.distribution
    release = host.system_info.release

    if dist == "centos":
        assert re.search(r"CentOS\s+{}".format(release),
                         request["content"],
                         re.MULTILINE)
    elif dist == "ubuntu":
        assert re.search(r"Ubuntu\s+{}".format(release),
                         request["content"],
                         re.MULTILINE)

    # The short way
    facts = host.ansible("setup")["ansible_facts"]

    assert re.search(r"{}\s+{}".format(facts["ansible_distribution"],
                                       facts["ansible_distribution_version"]),
                     request["content"], re.MULTILINE)
