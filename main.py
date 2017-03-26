import read
import solve


def to_string(cube):
    return ''


if __name__ == '__main__':
    cube = read.video_main()
    cube_str = to_string(cube)                      # TODO
    solution = solve.thistlethwaite(cube_str)       # TODO
    print(solution)
