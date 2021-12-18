import os

from legym import LegymHacker


class LegymCLI(LegymHacker):
    def __init__(self) -> None:
        super().__init__()
        self.__show_welcome()

    def __show_welcome(self) -> None:
        """Show welcome to user at the beginning."""
        print("------ 欢迎使用乐健命令行 ------")
        print("如果您是初次使用该应用，可以输入 `help` 来查看各命令使用方法。")

    def __valid_input(self, prompt: str = ">>> ") -> str:
        """Get non-empty user input.

        Args:
            prompt: Hint user what to do, default to '>>> '.

        Returns:
            Non-empty user input.
        """
        user_input = ""
        while user_input == "":
            user_input = input(prompt)
        return user_input

    def run(self) -> None:
        """Run CLI application."""
        while True:
            commands = self.__valid_input().split()
            if commands[0] == "login":
                self.__parse_login(commands[1:])
            elif commands[0] == "reg":
                self.__parse_reg(commands[1:])
            elif commands[0] == "sign":
                self.__parse_sign(commands[1:])
            elif commands[0] == "act":
                self.__parse_act(commands[1:])
            elif commands[0] == "help":
                self.__parse_help(commands[1:])
            elif commands[0] == "quit":
                self.__parse_quit()
            else:
                print(f"不支持的命令：{commands[0]}")

    def __parse_login(self, args: list) -> None:
        """Parse login command.

        Args:
            args: List containing username and password.
        """
        if len(args) == 0:
            username = self.__valid_input("用户名：")
            password = self.__valid_input("密码：")
        elif len(args) == 1:
            username = args[0]
            password = self.__valid_input("密码：")
        else:
            username = args[0]
            password = args[1]

        name, school = self.login(username, password)
        print(f"{school}的{name}，欢迎回来！")

    def __parse_reg(self, args: list) -> None:
        """Parse help command.

        Args:
            args: List containing activity to register.
        """
        pass

    def __parse_sign(self, args: list) -> None:
        pass

    def __parse_act(self, args: list) -> None:
        pass

    def __parse_help(self, args: list) -> None:
        """Parse help command.

        Args:
            args: list containing the command to check out.
        """
        filename = "help" if len(args) == 0 else args[0]
        filepath = os.path.join("doc", f"{filename}.txt")
        try:
            with open(filepath, "r", encoding="utf-8") as fr:
                print(f"\n{fr.read()}\n")
        except FileNotFoundError:
            print(f"Document `{filename}` not found.")

    def __parse_quit(self) -> None:
        """Parse quit command."""
        print("------ 感谢支持 ------\n")
        exit(0)


if __name__ == "__main__":
    cli = LegymCLI()
    cli.run()
