from cmd import Cmd


class Prompt(Cmd):
	prompt = "guineapig>> "
	intro = "GUINEAPIG"

	def do_exit(self, inp):
		print("Bye")
		return True

	def do_quit(self, inp):
		return self.do_exit(inp)

	def help_exit(self):
		print("Exit from shell")

	def help_quit(self):
		self.help_exit()

	do_EOF = do_exit

