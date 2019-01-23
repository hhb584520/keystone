# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_log import versionutils
from oslo_policy import policy

from keystone.common.policies import base

deprecated_get_idp = policy.DeprecatedRule(
    name=base.IDENTITY % 'get_identity_providers',
    check_str=base.RULE_ADMIN_REQUIRED
)
deprecated_list_idp = policy.DeprecatedRule(
    name=base.IDENTITY % 'list_identity_providers',
    check_str=base.RULE_ADMIN_REQUIRED
)

DEPRECATED_REASON = """
As of the Stein release, the identity provider API now understands default
roles and system-scoped tokens, making the API more granular by default without
compromising security. The new policy defaults account for these changes
automatically. Be sure to take these new defaults into consideration if you are
relying on overrides in your deployment for the identity provider API.
"""

identity_provider_policies = [
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'create_identity_provider',
        check_str=base.RULE_ADMIN_REQUIRED,
        # FIXME(lbragstad): All `scope_types` for identity provider policies
        # should be updated to include project scope if, or when, it becomes
        # possible to manage federated identity providers without modifying
        # configurations outside of keystone (Apache). It makes sense to
        # associate system scope to identity provider management since it
        # requires modifying configuration files.
        scope_types=['system'],
        description='Create identity provider.',
        operations=[{'path': '/v3/OS-FEDERATION/identity_providers/{idp_id}',
                     'method': 'PUT'}]),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'list_identity_providers',
        check_str=base.SYSTEM_READER,
        scope_types=['system'],
        description='List identity providers.',
        operations=[
            {
                'path': '/v3/OS-FEDERATION/identity_providers',
                'method': 'GET'
            },
            {
                'path': '/v3/OS-FEDERATION/identity_providers',
                'method': 'HEAD'
            }
        ],
        deprecated_rule=deprecated_list_idp,
        deprecated_reason=DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.STEIN
    ),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'get_identity_provider',
        check_str=base.SYSTEM_READER,
        scope_types=['system'],
        description='Get identity provider.',
        operations=[
            {
                'path': '/v3/OS-FEDERATION/identity_providers/{idp_id}',
                'method': 'GET'
            },
            {
                'path': '/v3/OS-FEDERATION/identity_providers/{idp_id}',
                'method': 'HEAD'
            }
        ],
        deprecated_rule=deprecated_get_idp,
        deprecated_reason=DEPRECATED_REASON,
        deprecated_since=versionutils.deprecated.STEIN
    ),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'update_identity_provider',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system'],
        description='Update identity provider.',
        operations=[{'path': '/v3/OS-FEDERATION/identity_providers/{idp_id}',
                     'method': 'PATCH'}]),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'delete_identity_provider',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system'],
        description='Delete identity provider.',
        operations=[{'path': '/v3/OS-FEDERATION/identity_providers/{idp_id}',
                     'method': 'DELETE'}])
]


def list_rules():
    return identity_provider_policies
