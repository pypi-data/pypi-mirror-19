from pyfunk import collections as coll,  combinators as comb
from pyfunk.monads import Monad


class Task(Monad):

    def __init__(self, fn):
        """
        Create new Task
        @sig a -> Task a b
        """
        self.fork = fn

    @classmethod
    def of(cls, x):
        """
        Factory for creating new resolved task
        @sig of :: b -> Task _ b
        """
        return Task(lambda _, resolve: resolve(x))

    # @classmethod
    # def all(cls, tasks):
    #     """
    #     Creates a task that represents the full list
    #     of tasks. It is fail-fast i.e. once a task fails
    #     all tasks fail
    #     @sig all :: Task t => [t a b] -> t a [b]
    #     """
    #     tasks_copy = tasks.copy()
    #     results = []
    #     error = None

    #     def rres(x):
    #         results.append(x)

    #     def rrej(e):
    #         nonlocal error
    #         error = e

    #     def handle_all(rej, res):
    #         while tasks_copy and error is None:
    #             t = tasks_copy.pop()
    #             t.fork(rrej, rres)
    #         if error is not None:
    #             rej(error)
    #         else:
    #             res(results)

    #     return cls(handle_all)

    @classmethod
    def rejected(cls, x):
        """
        Factory for creating a rejected task
        @sig rejected :: a -> Task a _
        """
        return Task(lambda reject, _: reject(x))

    def fmap(self, fn):
        """
        Transforms the resolved value of the task using the given function
        @sig fmap :: Task a b => (b -> c) -> Task a c
        """
        return Task(lambda rej, res: self.fork(rej, comb.compose(res, fn)))

    def rejected_fmap(self, fn):
        """
        Transforms the rejected value of the task using the given function
        @sig rejected_fmap :: Task a b => (a -> c) -> Task c b
        """
        return Task(lambda rej, res: self.fork(comb.compose(rej, fn), res))

    def join(self):
        """
        Lifts a Task out of another
        @sig join :: Task a b => Task a Task a b -> Task a b
        """
        return Task(lambda rej, res: self.fork(rej,
                    lambda x: x.fork(rej, res)))

    def or_else(self, fn):
        """
        Transforms a failure value into a new `Task[α, β]`. Does nothing if the
        structure already contains a successful value.
        @sig or_else :: Task a b => (a -> Task c) -> Task c b
        """
        return Task(lambda rej, res: self.fork(lambda x:
                                               fn(x).fork(rej, res), res))
