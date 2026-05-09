from concurrent.futures import ProcessPoolExecutor


def main():
    with ProcessPoolExecutor() as executor:
        future = executor.submit(pow, 2, 3)
        print(future.result())


if __name__ == '__main__':
    main()
