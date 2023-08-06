from . import tokenize_fork as tokenize
import logging

logger = logging.getLogger(__name__)


class TokenTypes(dict):

    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.by_name = {}
        for tok_id, tok_name in tokenize.tok_name.items():
            self.register(TokenType(tok_id, tok_name))

        self.register(DefaultTokenType())

    def register(self, token_type):
        if isinstance(token_type, TokenType):
            replacing = False
        else:
            token_class = token_type
            token_type = self[token_class.name]
            token_type = token_class(token_type.id, token_type.name)
            replacing = True

        for key in token_type.get_keys():
            assert replacing or key not in self
            self[key] = token_type

    def __repr__(self):
        def is_int(v):
            return isinstance(v, int)

        return repr(dict((k, v) for k, v in self.items() if is_int(k)))

    def __getattr__(self, key):
        if key in self:
            return self[key]


class TokenType(object):

    def __init__(self, id_, name):
        self.logger = logger.getChild(self.__class__.__name__)
        self.id, self.name = id_, name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s[%d] %s>' % (
            self.__class__.__name__,
            hash(self),
            self,
        )

    def __hash__(self):
        return self.id

    def get_keys(self):
        yield self.id
        yield self.name
        yield self

    def preprocess(self, token):
        '''Preprocess the token, this can do pretty much anything including
        changing the column'''
        return token


class CommentTokenType(TokenType):
    name = 'COMMENT'

    def preprocess(self, token):
        string = token.token
        string = string.strip()
        if string.startswith('#') and not string[1:].startswith(' '):
            string = '# %s' % string[1:]

        token.token = string
        return token


class IndentTokenType(TokenType):
    name = 'INDENT'

    def preprocess(self, token):
        '''Replace tabs with spaces as pep8 dictates'''
        # token.token = token.token.replace('\t', 4 * ' ')
        # token.end_col = len(token.token)
        return token


class StringTokenType(TokenType):
    name = 'STRING'

    def preprocess(self, token):
        '''Preprocess the token

        This automatically replaces strings with " to ' if possible
        '''
        string = token.token
        # Strip """
        if string.startswith('"""') and string.endswith('"""'):
            new_string = string[3:-3]
        # Strip '''
        elif string.startswith("'''") and string.endswith("'''"):
            new_string = string[3: -3]
        # Strip "
        elif string.startswith('"') and string.endswith('"'):
            new_string = string[1:-1]
        # Strip '
        elif string.startswith("'") and string.endswith("'"):
            new_string = string[1:-1]
        elif not string:
            new_string = string
        else:  # pragma: no cover
            raise RuntimeError('Strings should be surrounded with quotes',
                               token, token.token)

        # Multiline strings or strings with single quotes
        if '\n' in new_string or "'" in new_string:
            if "'''" in token.token:
                token.token = "'''%s'''" % new_string.replace("'''", r"\'\'\'")
            else:
                token.token = "'''%s'''" % new_string
        # Single line strings without quotes
        else:
            token.token = "'%s'" % new_string
        return token


class DefaultTokenType(TokenType):

    def __init__(self):
        TokenType.__init__(self, -1, 'DEFAULT')


def get_token_types():
    token_types = TokenTypes()
    token_types.register(CommentTokenType)
    token_types.register(StringTokenType)
    token_types.register(IndentTokenType)
    return token_types

TOKEN_TYPES = get_token_types()
