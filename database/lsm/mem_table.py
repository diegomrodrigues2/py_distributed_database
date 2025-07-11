from ..utils.vector_clock import VectorClock


class RBNode:
    """Nó de uma Red‑Black Tree (Árvore Rubro‑Negra)."""
    __slots__ = ("key", "value", "left", "right", "parent", "red")

    def __init__(self, key=None, value=None, left=None, right=None, parent=None, red=True):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.red = red  # True = RED, False = BLACK

class RBTree:
    """Implementação minimalista de Red‑Black Tree para chave‑valor."""

    def __init__(self):
        self.NIL = RBNode(red=False)  # Sentinela preta para folhas / raiz‑pai
        self.root = self.NIL
        self._size = 0

    # —— Rotações básicas ——
    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    # —— Inserção ——
    def insert(self, key, value):
        """Insere ou atualiza (key, value) em O(log n)."""
        z = RBNode(key, value, left=self.NIL, right=self.NIL, red=True)
        y = self.NIL
        x = self.root
        while x != self.NIL:
            y = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:  # Atualização de valor existente
                x.value = value
                return
        z.parent = y
        if y == self.NIL:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self._size += 1
        self._insert_fix(z)

    # —— Correção de cores após inserção ——
    def _insert_fix(self, z):
        while z.parent.red:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # Tio
                if y.red:  # Caso 1
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z == z.parent.right:  # Caso 2
                        z = z.parent
                        self._left_rotate(z)
                    # Caso 3
                    z.parent.red = False
                    z.parent.parent.red = True
                    self._right_rotate(z.parent.parent)
            else:  # Espelhado
                y = z.parent.parent.left
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self._left_rotate(z.parent.parent)
        self.root.red = False

    # —— Busca ——
    def search(self, key):
        """Busca chave e retorna valor."""
        x = self.root
        while x != self.NIL:
            if key == x.key:
                return x.value
            x = x.left if key < x.key else x.right
        return None

    # —— Traversal ordenado ——
    def _inorder(self, node, acc):
        """Percorre em ordem recursivamente."""
        if node != self.NIL:
            self._inorder(node.left, acc)
            acc.append((node.key, node.value))
            self._inorder(node.right, acc)

    def inorder(self):
        """Retorna itens em ordem de chave."""
        acc = []
        self._inorder(self.root, acc)
        return acc

    # —— Utilidades ——
    def __len__(self):
        """Retorna o número de nós na árvore."""
        return self._size


class MemTable:
    """MemTable baseada em Red‑Black Tree (substitui o dicionário anterior)."""

    def __init__(self, max_size: int) -> None:
        """Cria a estrutura em memória."""
        self._tree = RBTree()
        self.max_size = max_size
        print(f"MemTable (RBTree) inicializado — capacidade máxima {self.max_size} itens.")

    # API pública compatível
    def put(self, key, value):
        """Insere ou atualiza entradas ``(valor, vector_clock, created_txid, deleted_txid)``.

        Pode existir mais de uma versão por chave caso os vetores sejam
        concorrentes. Quando uma nova versão domina outra existente, esta é
        descartada. Se for dominada, a nova é ignorada.
        """
        val = value[0]
        vc = value[1]
        created = value[2] if len(value) > 2 else None
        deleted = value[3] if len(value) > 3 else None
        current = self._tree.search(key)
        if current is None:
            self._tree.insert(key, [(val, vc, created, deleted)])
            return

        new_list = []
        add_new = True
        for cur in current:
            cur_val, cur_vc = cur[0], cur[1]
            cur_created = cur[2] if len(cur) > 2 else None
            cur_deleted = cur[3] if len(cur) > 3 else None
            cmp = vc.compare(cur_vc)
            if cmp == ">":
                # nova versão é mais recente, descarta a antiga
                continue
            if cmp == "<":
                # existente é mais recente
                add_new = False
                new_list.append((cur_val, cur_vc, cur_created, cur_deleted))
                continue
            # concorrentes ou iguais
            if (
                vc.clock == cur_vc.clock
                and val == cur_val
                and created == cur_created
                and deleted == cur_deleted
            ):
                add_new = False
            new_list.append((cur_val, cur_vc, cur_created, cur_deleted))

        if add_new:
            new_list.append((val, vc, created, deleted))

        self._tree.insert(key, new_list)

    def set_versions(self, key, versions):
        """Replace versions list for ``key`` without merging."""
        self._tree.insert(key, versions)

    def get(self, key):
        """Retorna lista de ``(valor, vector_clock)`` para a chave."""
        return self._tree.search(key)

    def is_full(self):
        """Indica se atingiu a capacidade máxima."""
        return len(self._tree) >= self.max_size

    def clear(self):
        """Remove todos os itens."""
        self._tree = RBTree()
        print("MemTable: Limpo.")

    def get_sorted_items(self):
        """Retorna todos os pares ordenados por chave."""
        return self._tree.inorder()

    def __len__(self):
        """Quantidade de itens armazenados."""
        return len(self._tree)
