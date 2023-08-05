from pyfunk.monads import Monad


class Const(Monad):

    def fmap(self, fn):
        '''
        Ignores the given function
        @sig fmap :: Functor f => _ -> f a
        '''
        return self

    def join(self):
        '''
        Returns itself
        @sig join :: Functor f => f (f a) -> f a
        '''
        return self
