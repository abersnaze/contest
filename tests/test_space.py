from src.common.space import Matrix3, Space, line


def test_space():
    # Create a 2D space with a default value of "."
    space = Space(default=".", to_str=lambda x: x)

    # Set a few points in the space
    space[(0, 0)] = "A"
    space[(1, 1)] = "B"
    space[(2, 2)] = "C"

    # Print the space
    assert str(space) == "A..\n.B.\n..C\n"

    # Get the value at a point
    assert space[(0, 0)] == "A"

    # Set the value at a point
    space[(0, 0)] = "X"
    assert space[(0, 0)] == "X"

    # Get the value at a point that hasn't been set
    assert space[(3, 3)] == "."

    # Set the value at a point that hasn't been set
    space[(3, 3)] = "Y"
    assert space[(3, 3)] == "Y"


def test_matrix():
    transpose = Matrix3(((0, 1, 0), (1, 0, 0), (0, 0, 1)))
    assert transpose * (1, 2) == (2, 1)
    
    rotate = Matrix3(((0, -1, 0), (1, 0, 0), (0, 0, 1)))
    assert rotate * (1, 2) == (-2, 1)
    assert rotate * (-2, 1) == (-1, -2)
    assert rotate * (-1, -2) == (2, -1)
    assert rotate * (2, -1) == (1, 2)

    assert (rotate * rotate * rotate * rotate) * (1, 2) == (1, 2)
    assert rotate.inverse() * (1, 2) == (2, -1)

    assert Matrix3.rotate45degrees() * (1, 0) == (1, -1)
    
    
def test_line():
    assert list(line((0, 0), (5, 3))) == [(0, 0), (1, 1), (2, 1), (3, 2), (4, 2), (5, 3)]
    assert list(line((0, 0), (3, 5))) == [(0, 0), (1, 1), (1, 2), (2, 3), (2, 4), (3, 5)]
    assert list(line((0, 0), (5, -3))) == [(0, 0), (1, -1), (2, -1), (3, -2), (4, -2), (5, -3)]
    assert list(line((0, 0), (3, -5))) == [(0, 0), (1, -1), (1, -2), (2, -3), (2, -4), (3, -5)]
    assert list(line((0, 0), (-5, 3))) == [(0, 0), (-1, 1), (-2, 1), (-3, 2), (-4, 2), (-5, 3)]
    assert list(line((0, 0), (-3, 5))) == [(0, 0), (-1, 1), (-1, 2), (-2, 3), (-2, 4), (-3, 5)]
    assert list(line((0, 0), (-5, -3))) == [(0, 0), (-1, -1), (-2, -1), (-3, -2), (-4, -2), (-5, -3)]
    assert list(line((0, 0), (-3, -5))) == [(0, 0), (-1, -1), (-1, -2), (-2, -3), (-2, -4), (-3, -5)]