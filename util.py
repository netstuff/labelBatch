import os


DEFAULT_PREFIX = '_result'


def get_output(cli_args: object, default=None) -> str:
    """Get output location."""
    default = default or os.path.splitext(cli_args.input)[0] + DEFAULT_PREFIX
    output = cli_args.output or os.path.join(
        os.path.dirname(cli_args.input),
        default
    )

    name, ext = os.path.splitext(output)

    if not ext and not os.path.exists(output):
        os.mkdir(output)

    return output
