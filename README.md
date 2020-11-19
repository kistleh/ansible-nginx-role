# Ansible Nginx Role

This role has been created to be used as a base for learning
[Molecule](https://molecule.readthedocs.io/en/stable/) and is meant to cover
the following:

* Install role using either GitHub or Ansible Galaxy
* Initialize a new scenario and create/converge instance on Docker
* Update role to work on both CentOS and Ubuntu platforms
* Verify role idempotency
* Write Testinfra and/or Ansible tests to confirm role tasks
* Initialize new scenario for Docker
* Run code syntax/lint tests

## Requirements

*No extra requirements*

## Role Variables

### defaults

These variables are considered low-risk and can be safely changed to modify the
behaviour of the role.

* `nginx_index_title`
  * Title for index.html page. Defaults to `Hello, World`.
* `nginx_web_root`
  * Web content root directory. Defaults to `/var/www`.
* `nginx_worker_connections`
  * Number of Nginx worker connections. Defaults to `1024`.

### vars

These variables are considered high-risk and may impact the behaviour of the
role. Only change if you know what you're doing.

* `nginx_conf`
  * Nginx configuration file. Defaults to `/etc/nginx/nginx.conf`.
* `nginx_conf_dir`
  * Nginx configuration directory. Defaults to `/etc/nginx/conf.d`.
* `nginx_group`
  * Nginx group. Defaults to `www-data`.
* `nginx_user`
  * Nginx user. Defaults to `www-data`.

## Dependencies

*No extra dependencies*

## Example Playbook

```yaml
---
- hosts: servers
  roles:
    - role: kistleh.nginx
```

## License

[GPL-3.0-only](https://spdx.org/licenses/GPL-3.0-only.html)

## Author Information

Kim Hallen @ Catalyst IT, 2020
