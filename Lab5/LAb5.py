from collections import deque


def build_tree_iterative(height=3, root=16, l_b=lambda x: x // 2, r_b=lambda x: x * 2) -> dict:
    """Нерекурсивная генерация бинарного дерева в формате вложенных словарей."""

    tree = {str(root): []}  # Корень дерева
    queue = deque([(str(root), tree[str(root)])])  # Очередь для BFS

    current_height = 0

    while queue and current_height < height - 1:
        level_size = len(queue)

        for _ in range(level_size):
            current_key, children_list = queue.popleft()

            # Преобразуем ключ обратно в число для вычислений
            current_value = float(current_key) if '.' in current_key else int(current_key)

            # Вычисляем потомков
            left_val = l_b(current_value)
            right_val = r_b(current_value)

            # Создаем узлы-потомки
            left_node = {str(left_val): []}
            right_node = {str(right_val): []}

            # Добавляем потомков в текущий узел
            children_list.extend([left_node, right_node])

            # Добавляем потомков в очередь для дальнейшей обработки
            if current_height + 1 < height - 1:
                queue.append((str(left_val), left_node[str(left_val)]))
                queue.append((str(right_val), right_node[str(right_val)]))

        current_height += 1

    return tree


# Тестируем
print(build_tree_iterative(height=3, root=16))








