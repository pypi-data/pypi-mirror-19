# -*- coding: utf-8 -*-

# Copyright 2016,  Digital Reasoning
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""
Loads a stack-specific pillar file. stack_pillar_file must be set in the grains
or this module will not be available to pillar.
"""

import logging
import yaml

# Set up logging
logger = logging.getLogger(__name__)


def __virtual__():
    return True


def ext_pillar(minion_id, pillar, *args, **kwargs):
    """
    Basically, we need to provide additional pillar data to our states
    but only the pillar data defined for a stack. The user should have
    the ability to do this from the UI and the pillar file used will
    be located in the grains.
    """

    # If the file isn't specified in the grains, just return an empty pillar
    if 'stack_pillar_file' not in __grains__:
        return {}

    # load the stack_pillar_file, rendered as yaml, and return it
    try:
        with open(__grains__['stack_pillar_file'], 'r') as f:  # NOQA
            d = yaml.safe_load(f)
            d['stack_pillar_available'] = True
            return d
    except Exception as e:
        logger.exception(e)
        logger.critical('Unable to load/render stack_pillar_file. Is the YAML '
                        'properly formatted?')
    return {}
