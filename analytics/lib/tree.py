import re
from typing import (
    Callable,
    Container,
    Dict,
    Generator,
    Iterable,
    List,
    Mapping,
    Optional,
    Set,
    TypedDict,
    TypeVar,
    Union,
)

QueryT = Optional[Union[str, Container[str]]]
_T = TypeVar("_T")


class Length(TypedDict):
    min_length: int
    max_length: int


class NlpNode:
    @classmethod
    def _traverser(
        cls,
        tree_dict: Mapping[str, List["NlpNode"]],
        keywords: Iterable[str],
        get_identifier: Callable[["NlpNode"], _T],
        repeat: bool = False,
    ):
        visited: Set[_T] = set()
        for keyword in keywords:
            for node in tree_dict.get(keyword, []):
                if repeat:
                    yield node
                else:
                    identifier = get_identifier(node)
                    if identifier not in visited:
                        visited.add(identifier)
                        yield node

    @classmethod
    def traverser(
        cls,
        tree_dict: Mapping[str, List["NlpNode"]],
        keywords: Iterable[str],
        repeat: bool = False,
    ) -> Generator["NlpNode", None, None]:
        return cls._traverser(tree_dict, keywords, lambda n: n, repeat)

    @classmethod
    def text_traverser(
        cls,
        tree_dict: Mapping[str, List["NlpNode"]],
        keywords: Iterable[str],
        repeat: bool = False,
    ) -> Generator["NlpNode", None, None]:
        return cls._traverser(tree_dict, keywords, lambda n: n.text, repeat)

    def __init__(
        self,
        parent: Optional["NlpNode"],
        text: str,
        tree_dict: Optional[Dict[str, List["NlpNode"]]] = None,
    ):
        self.parent: Optional[NlpNode] = parent
        self.children: List[NlpNode] = []
        self.annotation: str = "UD"
        self.tree_dict: Dict[str, List[NlpNode]] = (
            tree_dict if tree_dict is not None else {}
        )

        # Build a tree with nodes from the phrase-structure tree of the text
        left_stack = []
        for i in range(len(text)):
            if text[i] == "(":
                left_stack.append(i)

            if text[i] == ")":
                left_index = left_stack.pop()

                if len(left_stack) == 0:
                    result = re.search(
                        r"\(([A-Z]+) ((?!\().+?)?[\(\)]", text[left_index : i + 1]
                    )
                    self.full_text = text
                    assert result is not None
                    self.annotation = result.group(1)
                    try:
                        self.text = result.group(2)
                        if self.tree_dict.get(self.text) is None:
                            self.tree_dict[self.text] = []
                        self.tree_dict[self.text].append(self)
                    except:
                        pass

                if len(left_stack) == 1:
                    self.children.append(
                        NlpNode(self, text[left_index : i + 1], self.tree_dict)
                    )

        if self.text is None:
            prepared_text = []
            for child in self.children:
                prepared_text.append(child.text)
            self.text = "".join(prepared_text)

    def match(
        self,
        text: QueryT = None,
        annotation: QueryT = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ) -> bool:
        """A helper funtion to see if the current NlpNode match the given conditionals
        When both text and annotation are None, this function always returns True"""
        length = len(self.text)
        if (min_length is not None and length < min_length) or (
            max_length is not None and length > max_length
        ):
            return False
        target_text = {text} if isinstance(text, str) else text
        target_annotation = {annotation} if isinstance(annotation, str) else annotation
        return (target_text is None or self.text in target_text) and (
            target_annotation is None or self.annotation in target_annotation
        )

    def tree_to_str(self, highlights: Optional[Set["NlpNode"]] = None) -> str:
        stack = [(0, self)]
        result = []

        def space(level: int) -> str:
            return "".join(["  " for _ in range(level)])

        while len(stack) > 0:
            level, cur_node = stack.pop()
            s = "*" if highlights and cur_node in highlights else ""
            cur_text = f"{space(level)}{s}{cur_node.annotation}{f' {cur_node.text}' if len(cur_node.children) == 0 else ''}{s}"
            if len(cur_node.children) == 1:
                stack.append((0, cur_node.children[0]))
                result.append(f"{cur_text} ")
            else:
                for child in reversed(cur_node.children):
                    stack.append((level + 1, child))
                result.append(f"{cur_text}\n")

        return "".join(result)

    def __repr__(self) -> str:
        return f"NlpNode {self.annotation} \"{self.text[:20]}{'...' if len(self.text) > 20 else ''}\""

    def __str__(self) -> str:
        return f"({self.annotation}{f' {self.text}' if self.text else ''})"

    def up(self, level: int) -> "NlpNode":
        """Trace upwards to a parent of the current NlpNode.
        When level=0, return the NlpNode itself"""
        assert level >= 0
        cur_node = self
        while level > 0:
            if not cur_node.parent:
                return cur_node
            cur_node = cur_node.parent
            level -= 1
        return cur_node

    def dfs_one(
        self,
        *,
        text: QueryT = None,
        annotation: QueryT = None,
        before: Optional["NlpNode"] = None,
        after: Optional["NlpNode"] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ) -> Optional["NlpNode"]:
        """A helper function to look up only one NlpNode"""
        result = self.dfs(
            text=text,
            annotation=annotation,
            before=before,
            after=after,
            min_length=min_length,
            max_length=max_length,
        )
        return result[0] if len(result) > 0 else None

    def dfs(
        self,
        *,
        text: QueryT = None,
        annotation: QueryT = None,
        count: int = 1,
        before: Optional["NlpNode"] = None,
        after: Optional["NlpNode"] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ) -> List["NlpNode"]:
        """Conduct a depth first search for the first nth children matching the given conditionals"""
        stack: List["NlpNode"] = [self]
        result: List["NlpNode"] = []
        is_after = after is None

        def loop(cur_node: "NlpNode") -> bool:
            """A helper function to help us conveniently break the outer while loop"""
            for NlpNode in cur_node.children:
                if NlpNode.match(text, annotation, min_length, max_length):
                    result.append(NlpNode)
                    return False
                if len(result) >= count:
                    return False
            return True

        while len(stack) > 0:
            cur_node = stack.pop()

            if cur_node is before:
                return result

            if is_after and not loop(cur_node):
                break

            if cur_node is after:
                is_after = True

            for NlpNode in reversed(cur_node.children):
                stack.append(NlpNode)

        return result
