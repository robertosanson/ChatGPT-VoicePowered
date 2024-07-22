import traceback

def log_error(e):
    with open("error_log.txt", "a") as log_file:
        log_file.write(traceback.format_exc())
        log_file.write("\n")
