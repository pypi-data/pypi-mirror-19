# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import time

from datetime import datetime, timedelta
from cement.utils.misc import minimal_logger
from ebcli.core import io
from ebcli.lib import elasticbeanstalk, codebuild
from ebcli.objects.exceptions import ServiceError, ValidationError
from ebcli.resources.strings import strings

LOG = minimal_logger(__name__)

# TODO: Write unit tests for these.
def stream_build_configuration_app_version_creation(app_name, app_version_label):
    # Get the cloudwatch logs link
    successfully_generated = wait_for_app_version_attribute(app_name, [app_version_label], 'BuildArn')
    app_version_response = elasticbeanstalk.get_application_versions(app_name, version_labels=[app_version_label])

    build_response = codebuild.batch_get_builds([app_version_response[0]['BuildArn']]) \
        if successfully_generated else None

    if build_response is not None and 'logs' in build_response['builds'][0]:
        log_link_text = "You can find logs for the CodeBuild build here: {0}".format(build_response['builds'][0]['logs']['deepLink'])
        io.echo(log_link_text)
    else:
        io.log_warning("Could not retrieve CloudWatch link for CodeBuild logs")

    # Wait for the success events
    try:
        from ebcli.operations import commonops
        commonops.wait_for_success_events(None, timeout_in_minutes=5,
                                      can_abort=False, version_label=app_version_label)
    except ServiceError as ex:
        LOG.debug("Caught service error while creating application version '{0}' "
                  "deleting the created applicaiton version as it is useless now.")
        elasticbeanstalk.delete_application_version(app_name, app_version_label)
        raise ex


def validate_build_config(build_config):
    if build_config.service_role is not None:
        # Verify that the service role exists in the customers account
        from ebcli.lib.iam import get_roles
        role = build_config.service_role
        validated_role = None
        existing_roles = get_roles()
        for existing_role in existing_roles:
            if role == existing_role['Arn'] or role == existing_role['RoleName']:
                validated_role = existing_role['Arn']

        if validated_role is None:
            LOG.debug("Role '{0}' not found in retrieved list of roles".format(role))
            raise ValidationError("Role '{0}' does not exist.".format(role))
        build_config.service_role = validated_role
    else:
        io.log_warning("To learn more about creating a service role for CodeBuild, see Docs:"
                       " https://docs-aws.amazon.com/codebuild/latest/userguide/setting-up.html#setting-up-service-role")
        raise ValidationError("No service role specified in buildspec; this is a required argument.")
        # Fail because the service role is required
    if build_config.image is None:
        #  Fail because the image is required
        raise ValidationError("No image specified in buildspec; this is a required argument.")


def wait_for_app_version_attribute(app_name, version_labels, attribute, timeout=5):
    versions_to_check = list(version_labels)
    found = {}
    failed = {}
    io.echo('--- Waiting for Application Versions to populate attributes ---')
    for version in version_labels:
        found[version] = False
        failed[version] = False
    start_time = datetime.utcnow()
    while not all([(found[version] or failed[version]) for version in versions_to_check]):
        if datetime.utcnow() - start_time >= timedelta(minutes=timeout):
            io.log_error(strings['appversion.attributefailed'])
            return False
        io.LOG.debug('Retrieving app versions.')
        app_versions = elasticbeanstalk.get_application_versions(app_name, versions_to_check)

        for v in app_versions:
            if attribute in v:
                if v[attribute] is not None:
                    found[v['VersionLabel']] = True
                    io.echo('Found needed attributes for application version {}'
                            .format(v['VersionLabel']))
                    versions_to_check.remove(v['VersionLabel'])
            elif 'Status' in v and (v['Status'] == 'FAILED' or v['Status'] == 'FAILED'):
                failed[v['VersionLabel']] = True
                io.log_error(strings['appversion.attributefailed'].replace('{app_version}',
                                                                         v['VersionLabel']))
                versions_to_check.remove(v['VersionLabel'])

        if all(found.values()):
            return True

        time.sleep(4)

    if any(failed.values()):
        return False

    return True
