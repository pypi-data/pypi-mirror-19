_help = """
COMMAND REFERENCE

List of all available commands:

    run, done, fail, info, skip, cancel, open, help

A command can be started by either typing the full word or the first letter.
Input is case in-sensitive. The 'run' command is the default if no text is entered.

run: If the current stage has an associated run command this command will be executed.
     Stdout and stderr will be redirected to log files which will be included in the
     final summary report.
done: Manually set this stage to done. This means that whoever run the delivery script
      ensures that this stage was done.
fail: Manually set this stage to failed. This means that whoever run the delivery script
      thinks that this script was not correctly done.
info: If the current stage has an associated help message this help message will be
      displayed to give further information about the current stage.
skip: Manually decide that this stage should be skipped.
cancel: Cancels the execution of the whole delivery script. Log files that have been
        Written until then will not be deleted.
open: If the current stage has an associated script parameter this command will open
      this script in notepad. The shall easy the process of having a quick look at
      the script that is actually doing the work.
help: Print this message.
"""
