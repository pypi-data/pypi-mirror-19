========
Overview
========



Python package integrating with Litmos User and Teams API

* Free software: BSD license

Installation
============

::

    pip install litmos-api


Getting started
=============

::

    from litmos import Litmos 
    litmos = Litmos({apikey}, {source})

    # --- User ---
    # retrieve users
    all_users = litmos.User.all()

    #find user by Id
    user = litmos.User.find('rnjx2WaQOa11')

    # search for user by username
    user = litmos.User.search('beelzebub@pieshop.net')

    # update JobTitle & City fields
    user.JobTitle = 'Pie eater'
    user.City = 'Pieland'

    # save user
    user.save()

    # deactivate user
    user.deactivate()

    # create user
    user = litmos.User.create({
            'UserName': 'jobaba72@pieshop.net',
            'FirstName': 'Jo',
            'LastName': 'Baba72',
            'Email': 'jobaba72@pieshop.net'
        })

    # remove all teams from user
    user.remove_teams()

    # delete user
    # with Id
    litmos.User.delete('YmrD112qlm41')

    # instance
    user.destroy()

    # --- Team ---
    # get all teams
    all_teams = litmos.Team.all()

    # find team by Id
    team = litmos.Team.find('rnjx2WaQOa11')

    # get team members
    users = team.users()

    # get team leaders
    leaders = team.leaders()

    # create team (at root level)
    team = litmos.Team.create({'Name': 'A-Team','Description': 'I pity the fool!'})

    # add sub-team
    sub_team = litmos.Team()
    sub_team.Name = 'B-Team'
    sub_team.Description = 'Woohoo'

    sub_team_id = team.add_sub_team(sub_team)

    # --- Team members ---

    # add users to team
    user1 = litmos.User.find('rnjx2WaQOa11')
    user2 = litmos.User.find('rnjx2WaQOa12')
    team.add_users([user1, user2])

    # remove users from team
    team.remove_user(user2)

    # --- Team leaders ---
    # promote user
    team.promote_team_leader(user1)

    # demote user
    team.demote_team_leader(user1)


Documentation
=============

https://python-litmos-api.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0 (2016-12-07)
-----------------------------------------

* First release on PyPI.


