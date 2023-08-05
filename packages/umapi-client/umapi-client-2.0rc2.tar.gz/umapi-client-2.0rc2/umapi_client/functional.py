# Copyright (c) 2016-2017 Adobe Systems Incorporated.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from enum import Enum

import six

from .api import Action, QuerySingle, QueryMultiple


class IdentityTypes(Enum):
    adobeID = 1
    enterpriseID = 2
    federatedID = 3


class GroupTypes(Enum):
    product = 1


class RoleTypes(Enum):
    admin = 1


class IfAlreadyExistsOptions(Enum):
    ignoreIfAlreadyExists = 1
    updateIfAlreadyExists = 2
    errorIfAlreadyExists = 3


class UserAction(Action):
    """
    A sequence of commands to perform on a single user.
    """

    def _validate(self, email=None, username=None, domain=None):
        local_regex = r"[a-zA-Z0-9!#$%&'*+/=?^_`{|}~;-]+([.][a-zA-Z0-9!#$%&'*+/=?^_`{|}~;-]+)*"
        dns_regex = r"[a-zA-Z0-9-]+([.][a-zA-Z0-9-]+)+"
        email_regex = r"^" + local_regex + r"@" + dns_regex + r"$"
        username_regex = r"^" + local_regex + r"$"
        domain_regex = r"^" + dns_regex + r"$"
        if email and not re.match(email_regex, email):
            raise ValueError("Illegal email format (must not be quoted or contain comments)")
        if domain and not re.match(domain_regex, domain):
            raise ValueError("Illegal domain format")
        if username and not re.match(username_regex, username):
            raise ValueError("Illegal username format: must be the unquoted local part of an email")

    def __init__(self, id_type=IdentityTypes.adobeID, email=None, username=None, domain=None, **kwargs):
        """
        Create an Action for a user identified either by email or by username and domain.
        There is never a reason to specify both email and username.
        :param id_type: IdentityTypes enum value (or the name of one), defaults to adobeID
        :param username: string, username in the Adobe domain (might be email)
        :param domain: string, required if the username is not an email address
        :param kwargs: other key/value pairs for the action, such as requestID
        """
        if str(id_type) in IdentityTypes.__members__:
            id_type = IdentityTypes[id_type]
        if id_type not in IdentityTypes:
            raise ValueError("Identity type ({}}) must be one of {}}".format(id_type, [i.name for i in IdentityTypes]))
        self.id_type = id_type
        self.email = None
        self.domain = None
        if username:
            if email and username.lower() == email.lower():
                # ignore the username if it's the same as the email (policy default)
                username = None
            elif id_type is not IdentityTypes.federatedID:
                raise ValueError("Username must match email except for Federated ID")
            else:
                self._validate(username=username)
                if domain:
                    self._validate(domain=domain)
                    self.domain = domain
        if email:
            self._validate(email=email)
            self.email = email
            if not self.domain:
                atpos = email.index('@')
                self.domain = email[atpos + 1:]
        elif not username:
            raise ValueError("No user identity specified.")
        elif not domain:
            raise ValueError("Both username and domain must be specified")
        if username:
            Action.__init__(self, user=username, domain=self.domain, **kwargs)
        else:
            Action.__init__(self, user=email, **kwargs)

    def create(self, first_name=None, last_name=None, country=None, email=None,
               on_conflict=IfAlreadyExistsOptions.errorIfAlreadyExists):
        """
        Create the user on the Adobe back end.
        :param first_name: (optional) user first name
        :param last_name: (optional) user last name
        :param country: (optional except for Federated ID) user 2-letter ISO country code
        :param email: user email, if not already specified at create time
        :param on_conflict: IfAlreadyExistsOption (or string name thereof) controlling creation of existing users
        :return: the User, so you can do User(...).create(...).add_group(...)
        """
        # all types handle email and on_conflict similarly
        create_params = {}
        if email is None:
            email = self.email
        elif self.email is None:
            self._validate(email=email)
            self.email = email
        elif self.email.lower() != email.lower():
            raise ValueError("Specified email ({}) doesn't match user's email({})", email, self.email)
        if str(on_conflict) in IfAlreadyExistsOptions.__members__:
            on_conflict = IfAlreadyExistsOptions[on_conflict]
        if on_conflict not in IfAlreadyExistsOptions:
            raise ValueError("on_conflict must be one of {}".format([o.name for o in IfAlreadyExistsOptions]))
        if on_conflict != IfAlreadyExistsOptions.errorIfAlreadyExists:
            create_params["option"] = on_conflict.name

        # each type handles the create differently
        if self.id_type == IdentityTypes.adobeID:
            # Adobe ID doesn't allow anything but email
            if first_name or last_name or country:
                raise ValueError("You cannot specify first or last name or country for an Adobe ID.")
            return self.insert(addAdobeID=dict(email=str(email), **create_params))
        else:
            # Federated and Enterprise allow specifying the name
            if first_name: create_params["firstName"] = str(first_name)
            if last_name: create_params["lastName"] = str(last_name)
            if self.id_type == IdentityTypes.enterpriseID:
                # Enterprise ID can default country, already has email on create
                create_params["country"] = str(country) if country else "UD"
                return self.insert(createEnterpriseID=dict(email=str(email), **create_params))
            else:
                # Federated ID must specify email if that wasn't done already
                if not email:
                    raise ValueError("You must specify email when creating a Federated ID")
                if not country:
                    raise ValueError("You must specify country when creating a Federated ID")
                return self.insert(createFederatedID=dict(email=str(email), country=str(country), **create_params))

    def update(self, email=None, username=None, first_name=None, last_name=None, country=None):
        """
        Update values on an existing user.  See the API docs for what kinds of update are possible.
        :param email: new email for this user
        :param username: new username for this user
        :param first_name: new first name for this user
        :param last_name: new last name for this user
        :param country: new country for this user
        :return: the User, so you can do User(...).update(...).add_group(...)
        """
        if self.id_type is IdentityTypes.adobeID:
            raise ValueError("You cannot update any attributes of an Adobe ID.")
        if email: self._validate(email=email)
        if username and self.id_type is IdentityTypes.enterpriseID:
            self._validate(email=username)
        updates = {}
        for k, v in six.iteritems(dict(email=email, username=username,
                                       firstName=first_name, lastName=last_name,
                                       country=country)):
            if v: updates[k] = str(v)
        return self.append(update=updates)

    def add_group(self, groups=None, group_type=GroupTypes.product):
        """
        Add user to some (typically PLC) groups.  Note that, if you add to no groups, the effect
        is simply to do an "add to organization Everybody group", so we let that be done.
        :param groups: list of group names the user should be added to
        :param group_type: the type of group (defaults to "product")
        :return: the User, so you can do User(...).add_group(...).add_role(...)
        """
        if group_type not in GroupTypes:
            raise ValueError("You must specify a GroupType value for argument group_type")
        glist = [str(group) for group in (groups if groups else [])]
        return self.append(add={group_type.name: glist})

    def remove_group(self, groups=None, all_groups=False, group_type=GroupTypes.product):
        """
        Remove user from some PLC groups, or all of them.
        :param groups: list of group names the user should be removed from
        :param all_groups: a boolean meaning remove from all (don't specify groups in this case)
        :param group_type: the type of group (defaults to "product")
        :return: the User, so you can do User(...).remove_group(...).add_role(...)
        """
        if group_type not in GroupTypes:
            raise ValueError("You must specify a GroupType value for argument group_type")
        if all_groups and groups:
            raise ValueError("When removing from all groups, do not specify specific groups")
        if all_groups:
            glist = "all"
        else:
            glist = [str(group) for group in (groups if groups else [])]
            if not glist:
                raise ValueError("You must specify groups from which to remove the user")
            glist = {group_type.name: glist}
        return self.append(remove=glist)

    def add_role(self, groups=None, role_type=RoleTypes.admin):
        """
        Make user have a role (typically PLC admin) with respect to some PLC groups.
        :param groups: list of group names the user should be an admin for
        :param role_type: the type of role (defaults to "admin")
        :return: the User, so you can do User(...).add_role(...).add_group(...)
        """
        if role_type not in RoleTypes:
            raise ValueError("You must specify a RoleType value for argument role_type")
        glist = [str(group) for group in (groups if groups else [])]
        if not glist:
            raise ValueError("You must specify groups for which the user should have a role_type")
        return self.append(addRoles={role_type.name: glist})

    def remove_role(self, groups=None, role_type=RoleTypes.admin):
        """
        Remove user from a role (typically admin) of some groups.
        :param groups: list of group names the user should NOT be an admin for
        :param role: the type of role (defaults to "admin")
        :return: the User, so you can do User(...).remove_role(...).remove_group(...)
        """
        if role_type not in RoleTypes:
            raise ValueError("You must specify a RoleType value for argument role_type")
        glist = [str(group) for group in (groups if groups else [])]
        if not glist:
            raise ValueError("You must specify groups for which the user should not have a role")
        return self.append(removeRoles={role_type.name: glist})

    def remove_from_organization(self, delete_account=False):
        """
        Remove a user from the organization's list of visible users.  Optionally. also delete the user's account.
        Deleting the user's account can only be done if the user's domain is controlled by the organization,
        and doing that will also remove the user from all other organizations with access to that domain.
        :param delete_account: whether to delete the user's account (default False)
        :return: None, because you cannot follow this command with another.
        """
        if delete_account:
            if self.id_type == IdentityTypes.adobeID:
                raise ValueError("You cannot delete an Adobe ID account.")
            arg = {"removedDomain": self.domain}
        else:
            arg = {}
        self.append(removeFromOrg=arg)
        return None

    def delete_account(self):
        """
        Delete a user's account.
        Deleting the user's account can only be done if the user's domain is controlled by the authorized organization,
        and removing the account will also remove the user from all organizations with access to that domain.
        :return: None, because you cannot follow this command with another.
        """
        if self.id_type == IdentityTypes.adobeID:
            raise ValueError("You cannot delete an Adobe ID account.")
        self.append(removeFromDomain={"domain": self.domain})
        return None


class UsersQuery(QueryMultiple):
    """
    Query for users meeting (optional) criteria
    """

    def __init__(self, connection, in_group="", in_domain="", identity_type=""):
        """
        Create a query for all users, or for those in a group or domain or both
        :param connection: Connection to run the query against
        :param in_group: (optional) name of the group to restrict the query to
        :param in_domain: (optional) name of the domain to restrict the query to
        """
        groups = [in_group] if in_group else []
        params = {}
        if in_domain: params["domain"] = str(in_domain)
        if identity_type: params["type"] = str(identity_type)
        QueryMultiple.__init__(self, connection=connection, object_type="user", url_params=groups, query_params=params)


class UserQuery(QuerySingle):
    """
    Query for a single user
    """

    def __init__(self, connection, email):
        """
        Create a query for the user with the given email
        :param connection: Connection to run the query against
        :param email: email of user to query for
        """
        QuerySingle.__init__(self, connection=connection, object_type="user", url_params=[str(email)])


class GroupsQuery(QueryMultiple):
    """
    Query for all groups
    """

    def __init__(self, connection):
        """
        Create a query for all groups
        :param connection: Connection to run the query against
        """
        QueryMultiple.__init__(self, connection=connection, object_type="group")
