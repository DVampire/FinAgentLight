from typing import Any

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

MESSAGE_SEPARATOR = '\n\n----------\n\n'

from finagentlight.logger import logger

__all__ = ['RetryMixin', 'DebugMixin']


class RetryMixin:
    """Mixin class for retry logic."""

    def retry_decorator(self, **kwargs):
        """Create a LLM retry decorator with customizable parameters. This is used for 429 errors, and a few other exceptions in LLM classes.

        Args:
            **kwargs: Keyword arguments to override default retry behavior.
                      Keys: num_retries, retry_exceptions, retry_min_wait, retry_max_wait, retry_multiplier

        Returns:
            A retry decorator with the parameters customizable in configuration.
        """
        num_retries = kwargs.get('num_retries')
        retry_exceptions = kwargs.get('retry_exceptions')
        retry_min_wait = kwargs.get('retry_min_wait')
        retry_max_wait = kwargs.get('retry_max_wait')
        retry_multiplier = kwargs.get('retry_multiplier')

        return retry(
            before_sleep=self.log_retry_attempt,
            stop=stop_after_attempt(num_retries),
            reraise=True,
            retry=(retry_if_exception_type(retry_exceptions)),
            wait=wait_exponential(
                multiplier=retry_multiplier,
                min=retry_min_wait,
                max=retry_max_wait,
            ),
        )

    def log_retry_attempt(self, retry_state):
        """Log retry attempts."""
        exception = retry_state.outcome.exception()
        logger.error(
            f'{exception}. Attempt #{retry_state.attempt_number} | You can customize retry values in the configuration.',
            exc_info=False,
        )


class DebugMixin:
    def log_prompt(self, messages: list[dict[str, Any]] | dict[str, Any]):
        if not messages:
            logger.debug('No completion messages!')
            return

        messages = messages if isinstance(messages, list) else [messages]
        debug_message = MESSAGE_SEPARATOR.join(
            self._format_message_content(msg)
            for msg in messages
            if msg.get('content', None)
        )

        if debug_message:
            logger.debug(debug_message)
        else:
            logger.debug('No completion messages!')

    def log_response(self, message_back: str):
        if message_back:
            logger.debug(message_back)

    def _format_message_content(self, message: dict[str, Any]):
        content = message['content']
        if isinstance(content, list):
            return '\n'.join(
                self._format_content_element(element) for element in content
            )
        return str(content)

    def _format_content_element(self, element: dict[str, Any]):
        if isinstance(element, dict):
            if 'text' in element:
                return element['text']
            if (
                self.vision_is_active()
                and 'image_url' in element
                and 'url' in element['image_url']
            ):
                return element['image_url']['url']
        return str(element)

    # This method should be implemented in the class that uses DebugMixin
    def vision_is_active(self):
        raise NotImplementedError
