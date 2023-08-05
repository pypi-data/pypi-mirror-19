# Copyright 2016 Invisible Institute
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

from datetime import datetime


def tweepy_list_to_json(tweepy_list):
    json = dict(tweepy_list.__dict__)

    json.pop('_api')
    # Set default timezone to +0000 here since datetime does not contain tz info
    json['created_at'] = datetime.strftime(json['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    json['user'] = json['user']._json

    return json
