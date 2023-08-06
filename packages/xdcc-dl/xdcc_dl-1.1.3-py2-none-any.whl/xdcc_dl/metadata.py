u"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via the XDCC
    protocol via file serving bots on IRC networks.

    xdcc_dl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    xdcc_dl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with xdcc_dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

from __future__ import absolute_import
u"""
The metadata is stored here. It can be used by any other module in this project this way, most
notably by the setup.py file
"""


class GitRepository(object):  # pragma: no cover
    u"""
    Class that stores information about the git repository sites used by this project
    """

    repository_name = u"xdcc-downloader"
    u"""
    The name of the repository
    """

    github_owner = u"namboy94"
    u"""
    The owner's Github username
    """

    gitlab_owner = u"namboy94"
    u"""
    The project's owner's username on Gitlab
    """

    gitlab_site_url = u"https://gitlab.namibsun.net/"
    u"""
    The address of the Gitlab instance
    """

    github_url = u"https://github.com/" + github_owner + u"/" + repository_name
    u"""
    The Github site URL
    """

    gitlab_url = gitlab_site_url + gitlab_owner + u"/" + repository_name
    u"""
    The Gitlab Project URL
    """


class General(object):  # pragma: no cover
    u"""
    Class that stores general information about a project
    """

    project_description = u"An XDCC Downloader"
    u"""
    A short description of the project
    """

    version_number = u"1.1.3"
    u"""
    The current version of the program.
    """

    author_names = u"Hermann Krumrey"
    u"""
    The name(s) of the project author(s)
    """

    author_emails = u"hermann@krumreyh.com"
    u"""
    The email address(es) of the project author(s)
    """

    license_type = u"GNU GPL3"
    u"""
    The project's license type
    """

    project_name = GitRepository.repository_name
    u"""
    The name of the project
    """

    download_master_zip = GitRepository.gitlab_url + u"/repository/archive.zip?ref=master"
    u"""
    A URL linking to the current source zip file of the master branch.
    """


class PypiVariables(object):  # pragma: no cover
    u"""
    Variables used for distributing with setuptools to the python package index
    """

    classifiers = [

        u"Environment :: Console",
        u"Natural Language :: English",
        u"Intended Audience :: Developers",
        u"Development Status :: 1 - Planning",
        u"Operating System :: OS Independent",
        u"Programming Language :: Python :: 3",
        u"Programming Language :: Python :: 2",
        u"Topic :: Communications :: File Sharing",
        u"License :: OSI Approved :: GNU General Public License v3 (GPLv3)"

    ]
    u"""
    The list trove classifiers applicable to this project
    """

    install_requires = [u"raven", u"irc", u"bs4", u"requests", u"cfscrape", u"urwid", u"typing"]
    u"""
    Python Packaging Index dependencies
    """

    name = u"xdcc_dl"
    u"""
    The name of the project on Pypi
    """

    version = General.version_number
    u"""
    The version of the project on pypi
    """

    description = General.project_description
    u"""
    The short description of the project on pypi
    """

    url = GitRepository.gitlab_url
    u"""
    A URL linking to the home page of the project, in this case a
    self-hosted Gitlab page
    """

    download_url = General.download_master_zip
    u"""
    A link to the current source zip of the project
    """

    author = General.author_names
    u"""
    The author(s) of this project
    """

    author_email = General.author_emails
    u"""
    The email adress(es) of the author(s)
    """

    license = General.license_type
    u"""
    The License used in this project
    """


class SentryLogger(object):  # pragma: no cover
    u"""
    Class that handles the sentry logger initialization
    """

    sentry_dsn = u"https://3f4217fbc10a48bf8bb119c1782d8b03:58b2a299d71d4c36a277df9add7b38c3@sentry.io/110685"
    u"""
    The DSN associated with this project
    """

    sentry = None
    u"""
    The sentry client
    """

    # Create the Sentry client to log bugs
    try:
        from raven import Client
        sentry = Client(dsn=sentry_dsn, release=General.version_number)
    except ImportError:
        Client = None
