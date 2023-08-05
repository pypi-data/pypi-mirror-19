"""Tools for interacting with Boolean expressions."""

import re

from ..definitions import (CONSTANT_VALUES, DELIMITERS, OPERATOR_MAPPING,
                           TT_NOT_OP)
from ..errors import (BadParenPositionError, EmptyExpressionError,
                      ExpressionOrderError, UnbalancedParenError)
from ..trees import BooleanExpressionTree
from ..utils import (assert_all_valid_keys,
                     assert_iterable_contains_all_expr_symbols)


class BooleanExpression(object):

    """A class for parsing and holding information about a Boolean expression.

    Attributes:
        raw_expr (str): The raw string expression, to be parsed upon
            initialization.
        symbols (List[str]): The list of unique symbols present in
            this expression, in the order of their first appearance in the
            expression.
        tokens (List[str]): A list of strings, each element indicating
                     a different token of the parsed expression.
        postfix_tokens (List[str]): A list of strings, representing the
            ``tokens`` list converted to postfix form.
        tree (tt.trees.BooleanExpressionTree): The expression tree
            representing the expression wrapped in this class, derived from
            the tokens parsed by this class.

    """

    def __init__(self, raw_expr):
        self.raw_expr = raw_expr

        self.symbols = []
        self._symbol_set = set()

        self.tokens = []
        self.postfix_tokens = []

        self._tokenize()
        self._to_postfix()

        self.tree = BooleanExpressionTree(self.postfix_tokens)

    def evaluate(self, **kwargs):
        """Evaluate the Boolean expression for the passed keyword arguments.

        This is a checked wrapper around the ``evaluate_unchecked`` function.

        Args:
            kwargs: Keys are names of symbols in this expression; the specified
                value for each of these keys will be substituted into the
                expression for evaluation.

        Returns:
            bool: The Boolean result of evaluating the expression.

        Raises:
            ExtraSymbolError
            InvalidBooleanValueError
            MissingSymbolError

        Note:
            See ``tt.utils.assertions.assert_all_valid_keys`` and
            ``tt.utils.assertions.assert_iterable_contains_all_expr_symbols``
            for more information about the exceptions raised by this method.

        """
        assert_all_valid_keys(kwargs, self._symbol_set)
        assert_iterable_contains_all_expr_symbols(kwargs.keys(),
                                                  self._symbol_set)

        return self.evaluate_unchecked(**kwargs)

    def evaluate_unchecked(self, **kwargs):
        """Evaluate the Boolean expression without checking the input.

        Args:
            kwargs: Keys are names of symbols in this expression; the specified
                value for each of these keys will be substituted into the
                expression for evaluation.

        Returns:
            bool: The Boolean result of evaluating the expression.

        """
        truthy = self.tree.evaluate(kwargs)
        return bool(truthy)

    def _tokenize(self):
        """Make the first pass through the expression, tokenizing it.

        This method will populate the ``symbols`` and ``tokens`` attributes,
        and is the first step in the expression-processing pipeline.

        Raises:
            GrammarError: If a malformed expression is received.

        """
        operator_strs = [k for k in OPERATOR_MAPPING.keys()]
        is_symbolic = {op: not op[0].isalpha() for op in operator_strs}
        operator_search_list = sorted(operator_strs, key=len, reverse=True)
        delimiters = DELIMITERS | set(k[0] for k, v in is_symbolic.items()
                                      if v)
        EXPECTING_OPERAND = 1
        EXPECTING_OPERATOR = 2
        grammar_state = EXPECTING_OPERAND

        idx = 0
        open_paren_count = 0
        num_chars = len(self.raw_expr)

        while idx < num_chars:
            c = self.raw_expr[idx].strip()

            if not c:
                # do nothing
                idx += 1
            elif c == '(':
                if grammar_state != EXPECTING_OPERAND:
                    raise BadParenPositionError('Unexpected parenthesis',
                                                self.raw_expr, idx)

                open_paren_count += 1
                self.tokens.append(c)
                idx += 1
            elif c == ')':
                if grammar_state != EXPECTING_OPERATOR:
                    raise BadParenPositionError('Unexpected parenthesis',
                                                self.raw_expr, idx)
                elif not open_paren_count:
                    raise UnbalancedParenError('Unbalanced parenthesis',
                                               self.raw_expr, idx)

                open_paren_count -= 1
                self.tokens.append(c)
                idx += 1
            else:
                is_operator = False
                num_chars_remaining = num_chars - idx

                matching_operators = [
                    operator for operator in operator_search_list
                    if len(operator) <= num_chars_remaining and
                    self.raw_expr[idx:(idx+len(operator))] == operator]

                if matching_operators:
                    match = matching_operators[0]
                    match_length = len(match)
                    next_c_pos = idx + match_length
                    next_c = (None if next_c_pos >= num_chars else
                              self.raw_expr[idx + match_length])

                    if next_c is None:
                        # trailing operator
                        raise ExpressionOrderError(
                            'Unexpected operator "{}"'.format(match),
                            self.raw_expr, idx)

                    if next_c in delimiters or is_symbolic[match]:
                        if OPERATOR_MAPPING[match] == TT_NOT_OP:
                            if grammar_state != EXPECTING_OPERAND:
                                raise ExpressionOrderError(
                                    'Unexpected unary operator "{}"'.format(
                                        match), self.raw_expr, idx)
                        else:
                            if grammar_state != EXPECTING_OPERATOR:
                                raise ExpressionOrderError(
                                    'Unexpected binary operator "{}"'.format(
                                        match), self.raw_expr, idx)
                            grammar_state = EXPECTING_OPERAND

                        is_operator = True
                        self.tokens.append(match)
                        idx += match_length

                if not is_operator:
                    if grammar_state != EXPECTING_OPERAND:
                        raise ExpressionOrderError('Unexpected operand',
                                                   self.raw_expr, idx)

                    operand_end_idx = idx + 1
                    while (operand_end_idx < num_chars and
                           self.raw_expr[operand_end_idx] not in delimiters):
                        operand_end_idx += 1

                    operand = self.raw_expr[idx:operand_end_idx]
                    self.tokens.append(operand)
                    if operand not in (self._symbol_set | CONSTANT_VALUES):
                        self.symbols.append(operand)
                        self._symbol_set.add(operand)

                    idx = operand_end_idx
                    grammar_state = EXPECTING_OPERATOR

        if open_paren_count:
            left_paren_positions = [m.start() for m in
                                    re.finditer(r'\(', self.raw_expr)]
            raise UnbalancedParenError(
                'Unbalanced left parenthesis', self.raw_expr,
                left_paren_positions[open_paren_count-1])

        if not self.tokens:
            raise EmptyExpressionError('Empty expression is invalid')

    def _to_postfix(self):
        """Populate the ``postfix_tokens`` attribute."""
        operand_set = self._symbol_set | CONSTANT_VALUES
        stack = []

        for token in self.tokens:
            if token in operand_set:
                self.postfix_tokens.append(token)
            elif token == '(':
                stack.append(token)
            elif token in OPERATOR_MAPPING.keys():
                if not stack:
                    stack.append(token)
                else:
                    while (stack and stack[-1] != '(' and
                            OPERATOR_MAPPING[stack[-1]].precedence >
                            OPERATOR_MAPPING[token].precedence):
                        self.postfix_tokens.append(stack.pop())
                    stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    self.postfix_tokens.append(stack.pop())
                stack.pop()

        for token in reversed(stack):
            self.postfix_tokens.append(token)
