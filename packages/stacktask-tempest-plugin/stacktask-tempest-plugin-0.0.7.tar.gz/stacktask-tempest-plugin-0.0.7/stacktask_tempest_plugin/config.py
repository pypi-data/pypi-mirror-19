# Copyright 2015 Catalyst IT Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from oslo_config import cfg

service_available_group = cfg.OptGroup(
    name="service_available",
    title="Available OpenStack Services"
)

ServiceAvailableGroup = [
    cfg.BoolOpt("stacktask", default=False,
                help="Whether or not Stacktask is expected to be available")
]

stacktask_group = cfg.OptGroup(
    name="stacktask",
    title="Stacktask Test Variables"
)

StacktaskGroup = [
    cfg.StrOpt("my_custom_variable", default="custom value",
               help="My custom variable.")
]
