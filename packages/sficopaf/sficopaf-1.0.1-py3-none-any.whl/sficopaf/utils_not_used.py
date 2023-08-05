# class ThreadSafeMethodWrapper(MethodType):
#     """
#     Wrapper object for a method to be called. all calls will be synchronized on a single lock
#     """
#     def __init__( self, obj, func, name):
#         self.__lock = RLock()
#         self.obj, self.func, self.name = obj, func, name
#
#     def __call__( self, *args, **kwds ):
#         self.__lock.acquire()
#         try:
#             return self.obj._method_call(self.name, self.func, *args, **kwds)
#         finally:
#             self.__lock.release()
#
#
# class ThreadSafeObject(object):
#     """
#     A thread-safe object wrapper. All methods will be synchronized individually
#     """
#     def __init__(self, initial_object:dict = None):
#         """
#         Constructor, ith an optional initial dictionary implementation
#         :param initial_dict:
#         """
#         self.__inner_dict = initial_dict or {}
#         self.__lock = RLock()
#
#     # Delegate all calls to the implementation:
#     def __getattr__(self, name):
#         """
#         Return a proxy wrapper object if this is a method call.
#         """
#         if name.startswith('_'):
#             return object.__getattribute__(self, name)
#         else:
#             att = getattr(self._obj, name)
#             if type(att) is MethodType:
#                 return ThreadSafeMethodWrapper(self, att, name)
#             else:
#                 return att
