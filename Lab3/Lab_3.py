
def gen_bin_tree(height: int = 0, root: int = 3, l_b = lambda x: x, r_b=lambda y:y):
    if height != int(height):
        raise TypeError('hight должна быть целым числом')
    if height <= 1:
        return {str(root): []}
    return {str(root): [gen_bin_tree(height - 1, l_b(root), l_b, r_b),
                            gen_bin_tree(height - 1, r_b(root), l_b, r_b)]}


def main():
    print(gen_bin_tree(3, 16, lambda x: x-1, lambda y:y**2))


if __name__ == "__main__":
    main()