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

from responsebot.common.exceptions import UserHandlerError
from responsebot.handlers.event import BaseEventHandler
from responsebot.models import TweetFilter


class BaseTweetHandler(object):
    """
    An abstract base tweet handler class for the user to subclass.
    """
    event_handler_class = None

    def __init__(self, client=None, *args, **kwargs):
        """
        Init a handler, try to create event handler if appropriate.

        :param client: Some Twitter API client for authentication. E.g. :class:`~responsebot.tweet_client.TweetClient`
        """
        self.catch_self_tweets = False
        self.client = client
        self.filter = self.get_filter()

        self._init_event_handler()

    def _init_event_handler(self):
        self.event_handler = None

        if self.client.config.get('user_stream') and\
                self.event_handler_class and\
                issubclass(self.event_handler_class, BaseEventHandler):
            try:
                self.event_handler = self.event_handler_class(self.client)
            except Exception as e:
                raise UserHandlerError(e)

    def get_filter(self):
        """
        Override this method for custom filter. By default returns a filter with the bot's authenticated user ID in the
        follow list.

        Example:

        .. code-block:: python

           return TweetFilter(track=['hello'], follow=['<some_user_id>'])`
        """
        return TweetFilter(follow=[str(self.client.get_current_user().id)])

    def on_tweet(self, tweet):
        """
        Callback for when a tweet appears in user timeline

        :param tweet: The incoming tweet
        :type tweet: :class:`~responsebot.models.Tweet`
        """
        pass

    def on_event(self, event):
        """
        Callback for when a non-tweet event is sent.
        By default, this will call an event handler passed by `event_handler_class`

        :param event: The received event
        """
        if self.event_handler:
            self.event_handler.handle(event)
