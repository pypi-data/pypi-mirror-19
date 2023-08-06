# -*- coding: utf-8 -*-
from listmatch.util import pairwise


class State:
    def __init__(self):
        self.epsilon = []  # epsilon-closure
        self.matcher = lambda x: False
        self.next_state = None
        self.is_end = False


class StateSet(object):
    def __init__(self, states):
        self.states = set()
        for state in states:
            self.add_state(state)

    def add_state(self, state):
        if state in self.states:
            return
        self.states.add(state)
        for eps in state.epsilon:
            self.add_state(eps)

    def __iter__(self):
        return iter(self.states)


def maybe_convert_to_nfa(arg):
    if isinstance(arg, NFA):
        return arg
    if callable(arg):
        return atom(arg)
    return atom(lambda x: x == arg)


class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        end.is_end = True

    def match(self, target):
        states = StateSet([self.start])

        for elem in target:
            states = StateSet(
                state.next_state
                for state in states
                if state.matcher(elem)
            )

        for s in states:
            if s.is_end:
                return True
        return False

    def __repr__(self):
        return self.repr

    def __add__(self, other):
        return concat(self, maybe_convert_to_nfa(other))

    def __radd__(self, other):
        return concat(maybe_convert_to_nfa(other), self)

    def __or__(self, other):
        return options(self, maybe_convert_to_nfa(other))

    def __ror__(self, other):
        return options(maybe_convert_to_nfa(other), self)


class atom(NFA):
    def __init__(self, arg):
        if not callable(arg):
            def matcher(x):
                return x == arg
        else:
            matcher = arg
        start, end = State(), State()
        start.matcher = matcher
        start.next_state = end
        self.repr = 'atom({})'.format(repr(arg))
        super().__init__(start, end)


class concat(NFA):
    def __init__(self, *args):
        nfas = [maybe_convert_to_nfa(arg) for arg in args]
        if len(nfas) == 0:
            state = State()
            super().__init__(state, state)
        elif len(nfas) == 1:
            super().__init__(nfas[0].start, nfas[0].end)
        else:
            for nfa1, nfa2 in pairwise(nfas):
                nfa1.end.is_end = False
                nfa1.end.epsilon.append(nfa2.start)
            super().__init__(nfas[0].start, nfas[-1].end)
        self.repr = 'concat({})'.format(
            ', '.join(
                repr(arg)
                for arg in args
            )
        )


class options(NFA):
    def __init__(self, *args):
        nfas = [maybe_convert_to_nfa(arg) for arg in args]
        start, end = State(), State()
        start.epsilon = [nfa.start for nfa in nfas]
        for nfa in nfas:
            nfa.end.epsilon.append(end)
            nfa.end.is_end = False
        super().__init__(start, end)
        self.repr = 'options({})'.format(
            ', '.join(
                repr(arg)
                for arg in args
            )
        )


def _rep(nfa, at_least_once):
    start, end = State(), State()
    start.epsilon = [nfa.start]
    if not at_least_once:
        start.epsilon.append(end)
    nfa.end.epsilon.extend([end, nfa.start])
    nfa.end.is_end = False
    return (start, end)


class zero_or_more(NFA):
    def __init__(self, arg):
        nfa = maybe_convert_to_nfa(arg)
        start, end = _rep(nfa, at_least_once=False)
        super().__init__(start, end)
        self.repr = 'zero_or_more({})'.format(repr(arg))


class one_or_more(NFA):
    def __init__(self, arg):
        nfa = maybe_convert_to_nfa(arg)
        start, end = _rep(nfa, at_least_once=True)
        super().__init__(start, end)
        self.repr = 'one_or_more({})'.format(repr(arg))


class maybe(NFA):
    def __init__(self, arg):
        nfa = maybe_convert_to_nfa(arg)
        nfa.start.epsilon.append(nfa.end)
        super().__init__(nfa.start, nfa.end)
        self.repr = 'maybe({})'.format(repr(arg))
