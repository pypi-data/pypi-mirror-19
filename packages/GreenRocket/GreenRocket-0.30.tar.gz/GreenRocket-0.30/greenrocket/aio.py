import asyncio


@asyncio.coroutine
def afire(self):
    """ Fire signal asynchronously """
    self.logger.debug('Fired %r', self)
    for cls in self.__class__.__mro__:
        if hasattr(cls, '__handlers__'):
            self.logger.debug('Propagate on %r', cls)
            for handler in cls.__handlers__:
                try:
                    self.logger.debug('Call %r', handler)
                    result = handler(self)
                    if asyncio.iscoroutine(result):
                        yield from result
                except:
                    self.logger.error('Failed on processing %r by %r',
                                      self, handler, exc_info=True)
