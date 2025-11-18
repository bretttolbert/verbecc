import jsbeautifier

from verbecc.src.utils.jsbeautifier_opts import JSBeautifierOpts


class JSBeautifier:

    @classmethod
    def beautify(cls, s: str) -> str:
        ret = jsbeautifier.beautify(s, JSBeautifierOpts.get_opts())
        return ret
