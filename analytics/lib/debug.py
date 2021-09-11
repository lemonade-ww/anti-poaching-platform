from typing import List

from analytics.lib.tree import NlpNode as Node


class SourcesDebugger:
    def __init__(self) -> None:
        self.resumed = False

    def pause(self, node: Node) -> None:
        if self.resumed:
            return

        p = lambda o: print(f"[adb] {o}")
        stack: List[Node] = list()
        p(f"Paused at {node}")
        while True:
            cmd = input("[adb] Please enter t (text), d (tree), f (full_text), n (next), c (children), s (sources), dfs (depth-first search), upN (go up in the tree where N is an optional number), b (back), q (quit) to proceed\n")
            if cmd == "n":
                break
            elif cmd == "d":
                p(node.tree_to_str())
            elif cmd == "f":
                p(node.full_text)
            elif cmd == "t":
                p(node.text)
            elif cmd == "c":
                print("\n".join([f"[{index}] {node}" for index, node in enumerate(node.children)]))
            elif cmd == "b":
                if len(stack) > 0:
                    node = stack.pop()
                else:
                    p("Cannot go back at this moment")
            elif cmd.isnumeric():
                stack.append(node)
                try:
                    node = node.children[int(cmd)]
                except IndexError:
                    p("The index exceeded the maximum number of children")
            elif cmd.startswith("dfs"):
                keywords = input("[adb] keywords:").strip()
                annotation = input("[adb] annotation:").strip()
                if len(cmd) > 3:
                    if cmd[3:].isnumeric():
                        nodes = node.dfs(text=keywords if keywords else None, annotation=annotation if annotation else None, count=int(cmd[3:]))
                        p(nodes)
                        if len(nodes) > 0:
                            stack.append(node)
                            node = nodes[0]
                    else:
                        print("The cound is invalid")
                else:
                    result = node.dfs_one(text=keywords if keywords else None, annotation=annotation if annotation else None)
                    p(node)
                    if result:
                        stack.append(node)
                        node = result
            elif cmd.startswith("up"):
                if len(cmd) == 2:
                    stack.append(node)
                    node = node.up(1)
                elif cmd[2:].isnumeric():
                    stack.append(node)
                    node = node.up(int(cmd[2:]))
                else:
                    p("The number is invalid")
            elif cmd == "q":
                self.resumed = True
                return
            else:
                p(f"Command \"{cmd}\" is invalid")
