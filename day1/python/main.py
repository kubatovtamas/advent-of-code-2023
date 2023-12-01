def create_two_digit_num(*nums: int):
    return nums[0] * 10 + nums[-1]


def main():
    line_nums = []
    with open("../input/full", "r") as f:
        while line := f.readline().rstrip():
            local_line_nums = [int(ch) for ch in line if ch.isdigit()]
            line_nums.append(local_line_nums)

    res = sum(create_two_digit_num(*nums) for nums in line_nums)
    print(res)


if __name__ == "__main__":
    main()
