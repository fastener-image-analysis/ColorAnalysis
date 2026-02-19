import multi_file_cli
import single_file_cli

def main():
    print("Select mode:")
    print("1. Single File Analysis")
    print("2. Multi File Analysis")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == '1':
        single_file_cli.main()
    elif choice == '2':
        multi_file_cli.main()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == '__main__':
    main()
