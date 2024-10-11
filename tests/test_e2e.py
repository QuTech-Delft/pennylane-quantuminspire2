import pennylane_quantuminspire2  # noqa: F401


def main(name: str) -> None:
    _get_auth_tokens()
    _run_e2e_tests(name=name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E2E test on a backend.")
    parser.add_argument(
        "name",
        type=str,
        help="Name of the backend where the E2E tests will run.",
    )

    args = parser.parse_args()
    main(args.name)
