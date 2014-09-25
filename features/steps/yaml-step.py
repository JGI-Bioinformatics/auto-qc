import behave                         as bh
import behave_command_line.assertions as asrt
import yaml                           as yml

@bh.then(u'the YAML-format standard {stream} should equal')
def step_impl(context, stream):

    def refmt(t):
        return yml.dump(yml.load(s))

    if   stream == 'out':
        s = context.output.stdout
    elif stream == 'error':
        s = context.output.stderr
    else:
        raise RuntimeError('Unknown stream "{}"'.format(stream))
    asrt.assert_diff(refmt(context.text), refmt(s))
