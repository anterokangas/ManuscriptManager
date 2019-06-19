from manuscript.tools.subclasses import get_all_subclasses




def test_get_all_subclasses():
    class A:
        pass

    class B(A):
        pass

    class C:
        pass

    class D(B, C):
        pass

    assert get_all_subclasses(A) == (B, D)
    assert get_all_subclasses(A, include_itself=True) == (A, B, D)
    assert get_all_subclasses(B) == (D,)
    assert get_all_subclasses(B, include_itself=True) == (B, D)
    assert get_all_subclasses(C) == (D,)
    assert get_all_subclasses(C, include_itself=True) == (C, D)
    assert get_all_subclasses(D) == tuple()
    assert get_all_subclasses(D, include_itself=True) == (D,)


if __name__ == "__main__":
    test_get_all_subclasses()
