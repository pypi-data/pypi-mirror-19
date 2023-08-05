import time
import logging

_enabled = False
traces = None
levels = []


logger = logging.getLogger(__name__)


class ExpressionTrace(object):
  def __init__(self):
    self.succeeded_parsing = 0.0
    self.failed_parsing = 0.0

  @property
  def total_time(self):
    return self.succeeded_parsing + self.failed_parsing


def enable(do_trace=True):
  global _enabled, traces
  _enabled = do_trace
  import collections
  traces = collections.defaultdict(ExpressionTrace)


def debugStart( instring, loc, expr ):
  levels.append((str(expr), time.time()))
  prefix = '  ' * len(levels)
  # logger.debug('%s{{{ %r trying %s', prefix, snippet(instring, loc), expr)


def debugSuccess( instring, startloc, endloc, expr, toks ):
  prefix = '  ' * len(levels)

  name, start_time = levels.pop()
  assert name == str(expr)
  delta = time.time() - start_time
  traces[str(expr)].succeeded_parsing += delta
  # logger.debug('%s}}} %r success matching %s => %r, time=%s', prefix, snippet(instring, startloc), expr, toks, delta)


def debugException( instring, loc, expr, exc ):
  prefix = '  ' * len(levels)

  name, start_time = levels.pop()
  assert name == str(expr)
  delta = time.time() - start_time
  traces[str(expr)].failed_parsing += delta
  # logger.debug('%s}}} %r error %s, time=%s', prefix, snippet(instring, loc), expr, delta)


def maybe_trace(expr):
  if _enabled:
    expr.setDebugActions(debugStart, debugSuccess, debugException)


def print_traces():
  lines = list(traces.items())
  lines.sort(key=lambda t: t[1].total_time, reverse=True)

  fmt1 = '%-20s  %8.3f  %8.3f'
  fmt2 = '%-20s  %8s  %8s'

  print fmt2 % ('Name', 'Success', 'Failed')
  print fmt2 % ('---------', '-------', '------')

  for name, trace in lines:
    print fmt1 % (name, trace.succeeded_parsing, trace.failed_parsing)


def snippet(s, loc):
    return s[loc:loc+5] + '...'

