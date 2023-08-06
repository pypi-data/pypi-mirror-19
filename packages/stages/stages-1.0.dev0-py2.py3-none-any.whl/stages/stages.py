#!/usr/bin/env/python
from __future__ import print_function
import sys
import configparser
from subprocess import call, Popen
from colorama import init as init_colorama, deinit as deinit_colorama, Fore
from colorama.ansi import clear_screen
from os import environ, getcwd, remove
from contextlib import contextmanager
from .compat import get_input
from .texts import _help


class Runner(object):
    def __init__(self, cfile, heading="", stdout_file="", stderr_file="", vars={}):
        self.CLS = clear_screen()
        self.vars = vars
        self.heading = heading
        self.progress_template = "     {stage:<69}    [{result}]\n"
        self.config = configparser.ConfigParser(allow_no_value=True
                                              , interpolation=configparser.ExtendedInterpolation()
                                              , defaults=vars)
        self.config.read(cfile)
        if stdout_file:
            self.stdout_file = stdout_file
        else:
            self.stdout_file = "stdout_output.txt"
        if stderr_file:
            self.stderr_file = stderr_file
        else:
            self.stderr_file = "stderr_output.txt"

    def _make_yellow(self, text):
        return (Fore.YELLOW + text + Fore.RESET)
        
    def _make_red(self, text):
        return (Fore.RED + text + Fore.RESET)
        
    def _make_green(self, text):
        return (Fore.GREEN + text + Fore.RESET)

    def _exec(self, cmds):
        returns = []
        if not isinstance(cmds, list):
            cmds = [cmds]
        with open(self.stdout_file, 'a') as fd_stdout:
            with open(self.stderr_file, 'a') as fd_stderr:
                for cmd in cmds:
                    ret = call(cmd, shell=True, stdout=fd_stdout , stderr=fd_stderr)
                    returns.append(ret)
        returns = map(lambda x: x==0, returns)
        return all(returns)

    def _format_progress(self, stage, result):
        if result == 'DONE':
            result = self._make_green(result)
        elif result == 'SKIP':
            result = self._make_yellow(result)
        else:
            result = self._make_red(result)
        return self.progress_template.format(stage=stage["short"], result=result)
        
    def _print_progress(self, progress, current, todo, message):
        print(self.CLS)
        status = ""
        if progress:
            status += progress
        if current:
            name = current["short"]
            status += " --> {:<75}\n".format(name)
        for item in todo:
            name = item["short"]
            status += "     {:<75}\n".format(name)
        print(status)
        # If the current stage hasn't completed, this message holds info for the user
        if message:
            print(message)
            
    def _query_input(self, current):
        action = get_input("[(R)un/(d)one/(f)ail/(i)nfo/(s)kip/(c)ancel/(o)pen/(h)elp]? ").upper()
        result = ()
        if action == "":
            action = "RUN"
        if action in ["D", "DONE"]:
            result = (True, self._format_progress(current, 'DONE'))
        elif action in ["F", "FAIL"]:
            result = (True, self._format_progress(current, 'FAIL'))
        elif action in ["R", "RUN"]:
            success = False
            cmd = current.get('run', None)
            if cmd:
                success = self._exec(cmd)
                if success:
                    result = (True, self._format_progress(current, 'DONE'))
                else:
                    result = (True, self._format_progress(current, 'FAIL'))
            else:
                result = (False, self._make_red("No run command found! Manual work necessary.\n"))
        elif action in ["I", "INFO"]:
            info = current.get('info', "No info available")
            result = (False, self._make_yellow('\n' + info + '\n'))
        elif action in ["C", "CANCEL"]:
            sys.exit(0)
        elif action in ["S", "SKIP"]:
            result = (True, self._format_progress(current, 'SKIP'))
        elif action in ["O", "OPEN"]:
            script = current.get('script', None)
            if script:
                editor = environ.get('EDITOR', None)
                if not editor:
                    result = (False, self._make_red("No editor could be found! Please provide the environment variable EDITOR.\n"))
                else:
                    Popen([editor, script]) # Use Popen to make the call non-blocking
                    result = (False, "")
            else:
                result = (False, self._make_red("No file associated with this stage!\n"))
        elif action in ["H", "HELP"]:
            result = (False, self._make_yellow(_help))
        else:
            result = (False, self._make_red("Unknown command!\n"))
        return result
        
    @contextmanager    
    def _colors(self):
        """
        Very simple context manager.
        Entry: initialize colorama -> wrapped stdout for colored output
        Exit: Revert stdout wrapping
        @contextmanager makes sure that deinit_colorama is called even if an exception is raised
        """
        init_colorama()
        yield
        deinit_colorama()

    def run(self):
        with self._colors():
            config = self.config
            try:
                stages = config['STAGES']
            except KeyError:
                print(self._make_red("No stage definitions found in config file! Aborting!"))
                sys.exit(1)

            # Local status tracking variables
            progress, current, message, todo = self._make_yellow(self.heading + "\n\n"), "", "", []

            for stage in stages.keys():
                if stage in self.vars:
                    break # we have reached the defaults dictionary
                try:
                    stage_data = config[stage]
                except KeyError:
                    stage_data = {}
                if not "short" in stage_data:
                    stage_data["short"] = stage # This will be the one line description displayed
                todo.append(stage_data)
            
            next = True
            while todo or current:
                if next:
                    current, todo = todo[0], todo[1:]
                self._print_progress(progress, current, todo, message)
                (next, result) = self._query_input(current)
                if next:
                    progress += result
                    current = None
                    message = ""
                else:
                    message = result
            self._print_progress(progress, "", todo, message)
            print(self._make_green("\nFinished all stages.\n"))
